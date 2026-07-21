#!/usr/bin/env python3
"""
설교 요약 헤드리스 파이프라인 (GitHub Actions / 클라우드 실행용)

로컬 앱 pipeline.py 의 프롬프트·구조·접두어 규칙을 그대로 재사용하되,
전사만 로컬 Whisper 대신 OpenRouter Whisper 엔드포인트로 처리한다.

흐름:
  1) yt-dlp 로 유튜브 오디오 다운로드            (pipeline.download_youtube_audio)
  2) ffmpeg 로 mp3 청크 분할 → OpenRouter Whisper 전사   (이 파일)
  3) AI 전사 교정                                 (pipeline.correct_transcript)
  4) 요약 HTML 생성(성경 본문 DB 주입·검증 포함)   (pipeline.generate_html)
  5) {접두어}{YYMMDD}.html 을 접두어별 폴더에 저장 후 git commit & push

입력은 모두 환경변수로 받는다(워크플로우가 채워 넣음):
  YT_URL            (필수) 유튜브 링크
  SERMON_TYPE       설교 종류 한글명(매일성경/주일오전교육/주일설교/주일오후설교/기타)
  CUSTOM_PREFIX     '기타'일 때 직접 지정할 접두어(2글자 권장)
  DATE_YYMMDD       날짜 6자리(비우면 영상 메타 → 없으면 오늘)
  PREACHER SCRIPTURE TITLE   비우면 유튜브 메타데이터에서 자동 추출
  CHURCH            교회명(기본: 나그네교회 온라인선교)
  DEFAULT_PREACHER  메타에서 설교자 못 찾을 때 폴백

  OPENROUTER_API_KEY (필수) 시크릿
  LLM_MODEL   교정·요약 모델 (기본 anthropic/claude-sonnet-5)
  STT_MODEL   전사 모델      (기본 openai/whisper-1)
  CHUNK_SEC   오디오 청크 길이 초 (기본 300; 60초 업스트림 타임아웃 대비 분할)
  GITHUB_WORKSPACE  체크아웃된 bible71 repo 경로 (Actions가 자동 설정)
"""
import os
import sys
import json
import base64
import shutil
import tempfile
import subprocess
import datetime as dt
import urllib.request
import urllib.error

SELF_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SELF_DIR)
import pipeline  # noqa: E402  (BASE_DIR = SELF_DIR 이므로 bible.db/style_template.html 이 옆에 있어야 함)


def log(msg):
    print(msg, flush=True)


def die(msg, code=1):
    log("::error::" + msg)
    sys.exit(code)


# ---------------------------------------------------------------------------
# OpenRouter 키: 로컬 앱은 파일에서 읽지만, CI 에서는 환경변수(시크릿)로 주입한다.
# pipeline.read_openrouter_key 를 교체하면 _auth_headers/_lm_chat 가 그대로 동작한다.
# ---------------------------------------------------------------------------
OR_KEY = (os.environ.get("OPENROUTER_API_KEY") or "").strip()
if not OR_KEY:
    die("OPENROUTER_API_KEY 시크릿이 설정되지 않았습니다.")
pipeline.read_openrouter_key = lambda *a, **k: OR_KEY

OR_BASE = pipeline.OPENROUTER_BASE_URL  # https://openrouter.ai/api/v1
LLM_MODEL = os.environ.get("LLM_MODEL", "anthropic/claude-sonnet-5").strip()
STT_MODEL = os.environ.get("STT_MODEL", "openai/whisper-1").strip()
CHUNK_SEC = int(os.environ.get("CHUNK_SEC", "300") or "300")


# ---------------------------------------------------------------------------
# 전사: ffmpeg 로 mono 16kHz mp3 청크로 나눈 뒤 OpenRouter STT 로 순차 전사
#   (업스트림 provider 타임아웃 60초 → 긴 오디오는 반드시 분할)
# ---------------------------------------------------------------------------
def _ffmpeg():
    ff = shutil.which("ffmpeg")
    if not ff:
        die("ffmpeg 를 찾을 수 없습니다. 워크플로우에서 'apt-get install -y ffmpeg' 단계를 확인하세요.")
    return ff


def transcribe_openrouter(audio_path):
    ff = _ffmpeg()
    tmp = tempfile.mkdtemp(prefix="stt_")
    seg_tmpl = os.path.join(tmp, "seg_%04d.mp3")
    # 압축(mono/16k/64k)으로 페이로드를 줄이고 segment 로 시간 분할
    cmd = [ff, "-hide_banner", "-loglevel", "error", "-y", "-i", audio_path,
           "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k",
           "-f", "segment", "-segment_time", str(CHUNK_SEC), "-reset_timestamps", "1",
           seg_tmpl]
    log(f"[STT] ffmpeg 로 {CHUNK_SEC}s 단위 mp3 청크 분할 중...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        die(f"ffmpeg 분할 실패: {r.stderr.strip()[:500]}")

    segs = sorted(f for f in os.listdir(tmp) if f.startswith("seg_") and f.endswith(".mp3"))
    if not segs:
        die("오디오 청크를 만들지 못했습니다(빈 오디오?).")
    log(f"[STT] 청크 {len(segs)}개 — OpenRouter '{STT_MODEL}' 로 전사 시작")

    parts = []
    for i, fn in enumerate(segs, 1):
        with open(os.path.join(tmp, fn), "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode("ascii")
        payload = {
            "model": STT_MODEL,
            "input_audio": {"data": b64, "format": "mp3"},
            "language": "ko",
        }
        req = urllib.request.Request(
            OR_BASE + "/audio/transcriptions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OR_KEY}",
                "HTTP-Referer": "https://github.com/KBD71/bible71",
                "X-Title": "Sermon App CI",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            die(f"OpenRouter STT 오류(HTTP {e.code}) 청크 {i}: {body[:400]}")
        except urllib.error.URLError as e:
            die(f"OpenRouter STT 연결 실패 청크 {i}: {e.reason}")
        txt = (data.get("text") or "").strip()
        parts.append(txt)
        log(f"[STT] 청크 {i}/{len(segs)} 완료 ({len(txt)}자)")

    shutil.rmtree(tmp, ignore_errors=True)
    full = "\n".join(p for p in parts if p).strip()
    if not full:
        die("전사 결과가 비어 있습니다.")
    log(f"[STT] 전사 완료 — 총 {len(full)}자")
    return full


# ---------------------------------------------------------------------------
# git: 방금 만든 HTML 파일 하나만 스테이징 → 커밋 → 푸시 (repo 잡동사니 커밋 방지)
# ---------------------------------------------------------------------------
def _git(repo, *args, check=True):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, env=env)
    if r.stdout.strip():
        log(r.stdout.strip())
    if check and r.returncode != 0:
        die(f"git {' '.join(args)} 실패: {r.stderr.strip()[:500]}")
    return r


def commit_and_push(repo, file_path, filename):
    # Actions 봇 신원(없을 때만)
    if not _git(repo, "config", "user.email", check=False).stdout.strip():
        _git(repo, "config", "user.email", "actions@github.com", check=False)
        _git(repo, "config", "user.name", "github-actions[bot]", check=False)
    _git(repo, "add", "--", file_path)
    status = _git(repo, "status", "--porcelain", "--", file_path)
    if not status.stdout.strip():
        # 파일 내용이 이전과 동일 → 밀 것 없으면 종료
        ahead = _git(repo, "rev-list", "--count", "@{u}..HEAD", check=False)
        if ahead.stdout.strip() in ("", "0"):
            log("[git] 변경 없음 — 커밋/푸시 생략 ✅")
            return
    else:
        _git(repo, "commit", "-m", f"Add sermon summary {filename}")
    # 원격 변경과 겹치면 rebase 후 재시도
    push = _git(repo, "push", check=False)
    if push.returncode != 0:
        log("[git] push 거부 → pull --rebase 후 재시도")
        _git(repo, "pull", "--rebase")
        _git(repo, "push")
    log("[git] 커밋 및 푸시 완료 ✅")


# ---------------------------------------------------------------------------
def main():
    url = (os.environ.get("YT_URL") or "").strip()
    if not url:
        die("YT_URL(유튜브 링크)이 비어 있습니다.")

    st = (os.environ.get("SERMON_TYPE") or "").strip()
    custom = (os.environ.get("CUSTOM_PREFIX") or "").strip()
    if st in pipeline.SERMON_TYPES:
        info, prefix = pipeline.resolve_prefix(st, custom)
        type_name = st
    else:
        # 종류명이 아니면 '기타' + 직접 접두어(넘어온 값 자체를 접두어로도 허용)
        info, prefix = pipeline.resolve_prefix("기타", custom or st)
        type_name = "기타"
    if not prefix:
        die("접두어를 정할 수 없습니다. SERMON_TYPE(종류명) 또는 CUSTOM_PREFIX 를 지정하세요.")

    log(f"=== 입력: type={type_name} prefix={prefix} url={url[:60]}... ===")

    # --- 메타데이터(설교자/본문/날짜/제목) 자동 추출 + 환경변수 override ---
    try:
        meta_yt = pipeline.fetch_youtube_metadata(url)
    except Exception as e:
        log(f"[메타] 유튜브 메타데이터 추출 실패(계속 진행): {e}")
        meta_yt = {"preacher": "", "scripture": "", "date_yymmdd": "", "title": ""}

    default_preacher = (os.environ.get("DEFAULT_PREACHER") or "").strip()
    date6 = ((os.environ.get("DATE_YYMMDD") or "").strip()
             or meta_yt.get("date_yymmdd", "")
             or dt.datetime.now().strftime("%y%m%d"))
    if not (date6.isdigit() and len(date6) == 6):
        die(f"날짜(YYMMDD)가 올바르지 않습니다: {date6!r}")
    preacher = ((os.environ.get("PREACHER") or "").strip()
                or meta_yt.get("preacher", "") or default_preacher)
    scripture = (os.environ.get("SCRIPTURE") or "").strip() or meta_yt.get("scripture", "")
    title = (os.environ.get("TITLE") or "").strip() or meta_yt.get("title", "")
    church = (os.environ.get("CHURCH") or "").strip() or "나그네교회 온라인선교"

    yy, mm, dd = date6[0:2], date6[2:4], date6[4:6]
    date_kr = f"20{yy}년 {int(mm)}월 {int(dd)}일 {info['service']}".strip()

    work = tempfile.mkdtemp(prefix="ytwork_")

    # --- 1) 오디오 다운로드 ---
    log("=== 1/4 오디오 다운로드 ===")
    audio = pipeline.download_youtube_audio(url, work, log)

    # --- 2) 전사(OpenRouter Whisper) → AI 교정 ---
    log("=== 2/4 전사 + 교정 ===")
    transcript = transcribe_openrouter(audio)
    transcript = pipeline.correct_transcript(transcript, OR_BASE, LLM_MODEL, log)

    # --- 3) 요약 HTML 생성 (성경 본문 DB 주입·검증은 pipeline 이 내부 처리) ---
    log("=== 3/4 요약 HTML 생성 ===")
    meta = {
        "preacher": preacher, "type_name": type_name,
        "service": info["service"], "date_kr": date_kr,
        "scripture": scripture, "title": title,
        "church": church, "youtube": url,
        "theme": info.get("theme"),
    }
    html = pipeline.generate_html(transcript, meta, OR_BASE, LLM_MODEL, log)

    # --- 4) 저장 + git push ---
    log("=== 4/4 저장 및 git push ===")
    repo = os.environ.get("GITHUB_WORKSPACE") or os.getcwd()
    subdir = info.get("subdir", "")
    filename = pipeline.make_filename(prefix, date6)
    dest_dir = os.path.join(repo, subdir) if subdir else repo
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, filename)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    rel = os.path.relpath(dest, repo)
    log(f"[저장] {rel} ({len(html)}자)")

    if os.path.isdir(os.path.join(repo, ".git")):
        commit_and_push(repo, dest, filename)
    else:
        log(f"[git] {repo} 가 git 저장소가 아니어서 push 생략(파일만 저장).")

    shutil.rmtree(work, ignore_errors=True)
    # 워크플로우 요약에 노출
    summ = os.environ.get("GITHUB_STEP_SUMMARY")
    if summ:
        with open(summ, "a", encoding="utf-8") as f:
            f.write(f"### 설교 요약 생성 완료 ✅\n\n"
                    f"- 파일: `{rel}`\n- 설교자: {preacher or '(미상)'}\n"
                    f"- 본문: {scripture or '(자동추정)'}\n- 제목: {title or '(없음)'}\n")
    log("=== 완료 ===")


if __name__ == "__main__":
    main()
