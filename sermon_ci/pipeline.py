"""
설교 요약 자동화 파이프라인
1) 유튜브 링크 또는 미디어 파일 -> 텍스트 전사 (yt-dlp + Whisper)
2) 전사 텍스트 -> LM Studio(로컬 LLM)로 설교 요약 HTML 생성
3) HTML을 기존 git repo에 저장하고 커밋/푸시
"""
import os
import re
import json
import shutil
import sqlite3
import subprocess
import datetime as dt

# ---- 설교 종류 -> 파일 접두어 / 예배명 매핑 -------------------------------
SERMON_TYPES = {
    "매일성경": {
        "prefix": "db", "service": "새벽기도회", "subdir": "dailybible",
        "theme": {"grad": "from-blue-900 to-indigo-900",
                  "eyebrow": "text-indigo-300", "accent": "text-indigo-400",
                  "swatch": "#4f46e5", "name": "인디고(남색)"},
    },
    "주일오전교육": {
        "prefix": "ae", "service": "주일 오전 교육", "subdir": "sermon",
        "theme": {"grad": "from-emerald-900 to-teal-900",
                  "eyebrow": "text-emerald-300", "accent": "text-emerald-400",
                  "swatch": "#059669", "name": "에메랄드(초록)"},
    },
    "주일설교": {
        "prefix": "ms", "service": "주일 오전예배", "subdir": "sermon",
        "theme": {"grad": "from-rose-900 to-red-900",
                  "eyebrow": "text-rose-300", "accent": "text-rose-400",
                  "swatch": "#e11d48", "name": "로즈(붉은색)"},
    },
    "주일오후설교": {
        "prefix": "as", "service": "주일 오후예배", "subdir": "sermon",
        "theme": {"grad": "from-violet-900 to-purple-900",
                  "eyebrow": "text-violet-300", "accent": "text-violet-400",
                  "swatch": "#7c3aed", "name": "바이올렛(보라)"},
    },
    "기타": {
        "prefix": "", "service": "", "subdir": "sermon",
        "theme": {"grad": "from-slate-800 to-gray-900",
                  "eyebrow": "text-slate-300", "accent": "text-slate-400",
                  "swatch": "#475569", "name": "슬레이트(회색)"},
    },
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIBLE_DB_PATH = os.path.join(BASE_DIR, "bible.db")


def find_ffmpeg():
    """PATH에 없어도 homebrew 등 흔한 설치 위치에서 ffmpeg를 찾는다.
    (Finder/GUI로 실행되면 PATH에 /opt/homebrew/bin 이 없는 경우가 많음)"""
    p = shutil.which("ffmpeg")
    if p:
        return p
    for c in ("/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg", "/opt/local/bin/ffmpeg"):
        if os.path.exists(c):
            return c
    return None


def resolve_prefix(sermon_type, custom_prefix=""):
    """설교 종류 -> (info, 파일 접두어). '기타'는 직접 입력한 접두어 사용."""
    info = SERMON_TYPES.get(sermon_type, SERMON_TYPES["기타"])
    prefix = custom_prefix.strip() if sermon_type == "기타" else info["prefix"]
    return info, prefix


# ==========================================================================
# 유튜브 메타데이터 분석 -> 설교자 / 날짜 / 본문 자동 추출
# ==========================================================================
BIBLE_BOOKS = [
    "창세기","출애굽기","레위기","민수기","신명기","여호수아","사사기","룻기",
    "사무엘상","사무엘하","열왕기상","열왕기하","역대상","역대하","에스라","느헤미야",
    "에스더","욥기","시편","잠언","전도서","아가","이사야","예레미야애가","예레미야",
    "에스겔","다니엘","호세아","요엘","아모스","오바댜","요나","미가","나훔","하박국",
    "스바냐","학개","스가랴","말라기","마태복음","마가복음","누가복음","요한복음",
    "사도행전","로마서","고린도전서","고린도후서","갈라디아서","에베소서","빌립보서",
    "골로새서","데살로니가전서","데살로니가후서","디모데전서","디모데후서","디도서",
    "빌레몬서","히브리서","야고보서","베드로전서","베드로후서","요한일서","요한이서",
    "요한삼서","유다서","요한계시록",
]
_BOOK_ALT = "(?:" + "|".join(sorted((re.escape(b) for b in BIBLE_BOOKS), key=len, reverse=True)) + ")"

# 관례적 약칭 -> 정식 책이름 (예: '사3:1-12' -> '이사야 3:1-12')
BIBLE_ABBR = {
    "창": "창세기", "출": "출애굽기", "레": "레위기", "민": "민수기", "신": "신명기",
    "수": "여호수아", "삿": "사사기", "룻": "룻기", "삼상": "사무엘상", "삼하": "사무엘하",
    "왕상": "열왕기상", "왕하": "열왕기하", "대상": "역대상", "대하": "역대하",
    "스": "에스라", "느": "느헤미야", "에": "에스더", "욥": "욥기", "시": "시편",
    "잠": "잠언", "전": "전도서", "아": "아가", "사": "이사야", "렘": "예레미야",
    "애": "예레미야애가", "겔": "에스겔", "단": "다니엘", "호": "호세아", "욜": "요엘",
    "암": "아모스", "옵": "오바댜", "욘": "요나", "미": "미가", "나": "나훔",
    "합": "하박국", "습": "스바냐", "학": "학개", "슥": "스가랴", "말": "말라기",
    "마": "마태복음", "막": "마가복음", "눅": "누가복음", "요": "요한복음",
    "행": "사도행전", "롬": "로마서", "고전": "고린도전서", "고후": "고린도후서",
    "갈": "갈라디아서", "엡": "에베소서", "빌": "빌립보서", "골": "골로새서",
    "살전": "데살로니가전서", "살후": "데살로니가후서", "딤전": "디모데전서",
    "딤후": "디모데후서", "딛": "디도서", "몬": "빌레몬서", "히": "히브리서",
    "약": "야고보서", "벧전": "베드로전서", "벧후": "베드로후서",
    "요일": "요한일서", "요이": "요한이서", "요삼": "요한삼서", "유": "유다서",
    "계": "요한계시록",
}
# 약칭은 앞에 한글이 붙어 있으면 제외(예: '이사야'의 '사' 오인 방지)
_ABBR_ALT = r"(?<![가-힣])(?:" + "|".join(
    sorted((re.escape(a) for a in BIBLE_ABBR), key=len, reverse=True)) + ")"


def find_scripture(text):
    """본문 성구 추출. 범위 표기를 우선 매칭:
    '이사야 3:1-12', '사3:1-12', '요 3:16-4:2', '창세기 1장 1-10절', '요한복음 3:16' 등."""
    if not text:
        return ""
    ref_xchap = r"\s*\d+\s*[:：]\s*\d+\s*[-~]\s*\d+\s*[:：]\s*\d+"   # 3:1-4:6
    ref_range = r"\s*\d+\s*[:：]\s*\d+\s*[-~]\s*\d+"                 # 3:1-12
    ref_one = r"\s*\d+\s*[:：]\s*\d+"                                # 3:16
    jang_range = r"\s*\d+\s*장\s*\d+\s*[-~]\s*\d+\s*절"              # 1장 1-10절
    jang = r"\s*\d+\s*장(?:\s*\d+\s*절)?"
    chap = r"\s*\d+"
    # (책이름 패턴, 성구 패턴) — 범위가 넓고 명확한 표기부터 시도
    patterns = [
        (_BOOK_ALT, ref_xchap), (_ABBR_ALT, ref_xchap),
        (_BOOK_ALT, ref_range), (_ABBR_ALT, ref_range),
        (_BOOK_ALT, jang_range),
        (_BOOK_ALT, ref_one), (_ABBR_ALT, ref_one),
        (_BOOK_ALT, jang),
        (_BOOK_ALT, chap),
    ]
    for book_alt, ref in patterns:
        m = re.search("(" + book_alt + ")(" + ref + ")", text)
        if m:
            book = BIBLE_ABBR.get(m.group(1), m.group(1))
            rest = m.group(2).strip()
            rest = re.sub(r"\s*[:：]\s*", ":", rest)
            rest = re.sub(r"\s*[-~]\s*", "-", rest)
            rest = re.sub(r"\s+", " ", rest)
            return f"{book} {rest}"
    return ""


def detect_main_passage(transcript):
    """본문란이 비었을 때, 전사에서 가장 많이 언급된 '책+장'을 본문으로 추정해 '책 N장'을 반환한다.
    지엽적으로 한 번 인용된 구절이 아니라 설교가 반복해 다룬 장을 고른다. 못 찾으면 ''."""
    if not transcript:
        return ""
    pat = re.compile("(" + _BOOK_ALT + "|" + _ABBR_ALT + r")\s*(\d+)\s*(?:장|[:：])")
    counts = {}
    for m in pat.finditer(transcript):
        book = BIBLE_ABBR.get(m.group(1), m.group(1))
        key = (book, int(m.group(2)))
        counts[key] = counts.get(key, 0) + 1
    if not counts:
        return ""
    book, chap = max(counts, key=lambda k: counts[k])   # 동점이면 먼저 등장한 장
    return f"{book} {chap}장"


def find_date(text, upload_date=""):
    """제목/설명에서 날짜를 찾아 YYMMDD 반환. 없으면 업로드 날짜 사용."""
    if text:
        m = re.search(r"20(\d{2})\s*[.\-/년]\s*(\d{1,2})\s*[.\-/월]\s*(\d{1,2})", text)
        if m:
            yy, mm, dd = m.group(1), int(m.group(2)), int(m.group(3))
            return f"{yy}{mm:02d}{dd:02d}"
    if len(upload_date) == 8 and upload_date.isdigit():
        return upload_date[2:]
    return ""


def find_preacher(text):
    """'홍길동 목사' 형태에서 설교자 추출."""
    if not text:
        return ""
    m = re.search(r"([가-힣]{2,4})\s*(목사님|목사|전도사|강도사|담임)", text)
    if m:
        title = "목사" if m.group(2) in ("목사님", "목사", "담임") else m.group(2)
        return f"{m.group(1)} {title}"
    return ""


def find_title(text, preacher="", scripture="", uploader=""):
    """유튜브 제목에서 날짜·설교자·본문·예배구분·채널 같은 잡음을 걷어내 '설교 제목'만 추린다.
    깔끔하게 남는 게 없으면 원제목(첫 줄)을 그대로 반환한다."""
    if not text:
        return ""
    raw = text.splitlines()[0].strip()
    t = raw
    t = re.sub(r"[\[\【(（][^\]\】)）]*[\]\】)）]", " ", t)          # [주일설교] 【…】 (…) 제거
    t = re.sub(r"20\d{2}\s*[.\-/년]\s*\d{1,2}\s*[.\-/월]\s*\d{1,2}\s*일?", " ", t)  # 날짜
    t = re.sub(r"\b\d{6,8}\b", " ", t)
    if scripture:
        t = t.replace(scripture, " ")
    t = re.sub("(" + _BOOK_ALT + "|" + _ABBR_ALT + r")\s*\d+(?:\s*[:：장]\s*\d+)?"
               r"(?:\s*[-~]\s*\d+(?:\s*[:：]\s*\d+)?)?\s*절?", " ", t)              # 성구 표기
    if preacher:
        t = t.replace(preacher, " ")
        t = re.sub(re.escape(preacher.split()[0]) + r"\s*(목사님|목사|전도사|강도사|담임)?", " ", t)
    else:
        t = re.sub(r"[가-힣]{2,4}\s*(목사님|목사|전도사|강도사|담임)", " ", t)
    if uploader:
        t = t.replace(uploader, " ")
    t = re.sub(r"(주일\s*오전|주일\s*오후|주일|오전|오후|새벽|수요|금요|저녁|온라인)?\s*"
               r"(예배|기도회)", " ", t)                                            # 예배 구분
    t = re.sub(r"[|·ㅣ┃/│]+", " ", t)                                             # 구분자
    t = re.sub(r"\s+", " ", t).strip(" -–—:·|")
    return t if len(t) >= 2 else raw


def fetch_youtube_metadata(url):
    """유튜브 링크 메타데이터에서 설교자/날짜/본문 등을 파싱해 반환."""
    import yt_dlp
    base = {"quiet": True, "no_warnings": True, "skip_download": True, "noplaylist": True}
    info = None
    last_err = None
    for clients in (None, ["tv"], ["ios"], ["android"], ["web_safari"]):
        opts = dict(base)
        if clients:
            opts["extractor_args"] = {"youtube": {"player_client": clients}}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            break
        except Exception as e:
            last_err = e
            continue
    if info is None:
        raise RuntimeError(str(last_err))
    title = info.get("title") or ""
    desc = info.get("description") or ""
    upload = info.get("upload_date") or ""
    uploader = info.get("uploader") or info.get("channel") or ""
    text = title + "\n" + desc
    preacher = find_preacher(text)
    scripture = find_scripture(text)
    return {
        "video_title": title,
        "uploader": uploader,
        "preacher": preacher,
        "scripture": scripture,
        "date_yymmdd": find_date(text, upload),
        "title": find_title(title, preacher, scripture, uploader),
        "title_guess": title.strip(),
    }



# ==========================================================================
# 성경 본문 조회 (bible.db · 개역개정) — LLM 재현 대신 DB에서 정확히 추출
# ==========================================================================
_BOOK_NO_CACHE = None


def _book_number(book_name):
    """책 이름(정식)을 bible.db의 book 번호로 변환한다. 번호는 DB에서 직접 읽어 캐시하므로
    코드의 책 순서/표기(예: '요한일서' vs DB '요한1서')와 어긋나도 정확하다."""
    global _BOOK_NO_CACHE
    if _BOOK_NO_CACHE is None:
        _BOOK_NO_CACHE = {}
        try:
            con = sqlite3.connect(BIBLE_DB_PATH)
            for lbl, bno in con.execute("SELECT DISTINCT long_label, book FROM bible2"):
                _BOOK_NO_CACHE[lbl] = bno
            con.close()
        except sqlite3.Error:
            _BOOK_NO_CACHE = {}
    if book_name in _BOOK_NO_CACHE:
        return _BOOK_NO_CACHE[book_name]
    # 표기 차이 보정: 요한일서<->요한1서, 요한이서<->요한2서, 요한삼서<->요한3서
    alt = book_name.replace("일서", "1서").replace("이서", "2서").replace("삼서", "3서")
    return _BOOK_NO_CACHE.get(alt)


def parse_scripture_ref(scripture):
    """'이사야 3:1-12', '요한복음 3:16', '사 3:1-4:2', '창세기 1장 1-10절', '시편 23편' 등을
    (book, c1, v1, c2, v2)로 파싱한다. 장 전체면 v1/v2=None. 실패 시 None."""
    if not scripture:
        return None
    s = re.sub(r"\s+", " ", scripture).strip()
    book = after = None
    m = re.search("(" + _BOOK_ALT + ")", s)          # 정식 이름 우선
    if m:
        book, after = m.group(1), s[m.end():]
    else:
        m = re.search(_ABBR_ALT, s)                   # 약칭
        if m:
            book, after = BIBLE_ABBR.get(m.group(0), m.group(0)), s[m.end():]
    if not book:
        return None
    ref = after.translate(str.maketrans("０１２３４５６７８９", "0123456789"))  # 전각 숫자
    ref = ref.replace("장", ":").replace("절", "").replace("편", "")
    ref = ref.replace("：", ":").replace(".", ":")     # 전각 콜론, '3.16' 형태
    ref = re.sub(r"[‐-―−－~∼〜～]", "-", ref)           # 각종 하이픈·물결표(전각 포함) → '-'
    ref = re.sub(r"[^0-9:\-]", "", ref)               # 숫자/콜론/하이픈만 남김
    ref = re.sub(r"-{2,}", "-", ref).strip("-:")       # 중복 구분자 정리
    m = re.match(r"(\d+):(\d+)-(\d+):(\d+)", ref)      # c:v - c:v
    if m:
        c1, v1, c2, v2 = map(int, m.groups()); return (book, c1, v1, c2, v2)
    m = re.match(r"(\d+):(\d+)-(\d+)", ref)            # c:v - v
    if m:
        c1, v1, v2 = map(int, m.groups()); return (book, c1, v1, c1, v2)
    m = re.match(r"(\d+):(\d+)", ref)                  # c:v
    if m:
        c1, v1 = map(int, m.groups()); return (book, c1, v1, c1, v1)
    m = re.match(r"(\d+)-(\d+)$", ref)                 # 장 범위(장 전체)
    if m:
        c1, c2 = map(int, m.groups()); return (book, c1, None, c2, None)
    m = re.match(r"(\d+)", ref)                        # 장 전체
    if m:
        c1 = int(m.group(1)); return (book, c1, None, c1, None)
    return None


def fetch_bible_passage(scripture):
    """scripture 표기를 파싱해 bible.db에서 해당 절들을 추출한다.
    반환: [{'chapter':3,'verse':1,'text':'보라 주...','heading':'예루살렘의 멸망' 또는 None}, ...]
    파싱/조회 실패 시 빈 리스트."""
    parsed = parse_scripture_ref(scripture)
    if not parsed or not os.path.exists(BIBLE_DB_PATH):
        return []
    book, c1, v1, c2, v2 = parsed
    bno = _book_number(book)
    if not bno:
        return []
    try:
        con = sqlite3.connect(BIBLE_DB_PATH)
        cur = con.cursor()
        if v1 is None:                                # 장 전체(들)
            rows = cur.execute(
                "SELECT chapter,paragraph,sentence FROM bible2 "
                "WHERE book=? AND chapter BETWEEN ? AND ? ORDER BY chapter,paragraph",
                (bno, c1, c2)).fetchall()
        elif c1 == c2:                                # 한 장 안의 절 범위
            rows = cur.execute(
                "SELECT chapter,paragraph,sentence FROM bible2 "
                "WHERE book=? AND chapter=? AND paragraph BETWEEN ? AND ? "
                "ORDER BY paragraph", (bno, c1, v1, v2)).fetchall()
        else:                                         # 장을 넘는 범위 c1:v1 ~ c2:v2
            rows = cur.execute(
                "SELECT chapter,paragraph,sentence FROM bible2 WHERE book=? AND ("
                "(chapter=? AND paragraph>=?) OR (chapter>? AND chapter<?) "
                "OR (chapter=? AND paragraph<=?)) ORDER BY chapter,paragraph",
                (bno, c1, v1, c1, c2, c2, v2)).fetchall()
        con.close()
    except sqlite3.Error:
        return []
    passage = []
    for ch, vs, sent in rows:
        heading = None
        mt = re.match(r"\s*<([^>]+)>\s*(.*)", sent, re.S)   # <소제목> 분리
        if mt:
            heading, sent = mt.group(1).strip(), mt.group(2).strip()
        passage.append({"chapter": ch, "verse": vs,
                        "text": sent.strip(), "heading": heading})
    return passage


def _esc(s):
    """HTML 특수문자 최소 이스케이프."""
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_scripture_prompt_block(passage, multi_chapter):
    """LLM에게 '정답 본문'으로 제공할 절 목록 텍스트(라벨 + 절)를 만든다."""
    lines = []
    for v in passage:
        label = f"{v['chapter']}:{v['verse']}" if multi_chapter else str(v["verse"])
        lines.append(f"{label} {v['text']}")
    return "\n".join(lines)


def _inject_scripture_section(html, passage, multi_chapter):
    """생성된 HTML의 scripture-text-section 내부를 DB에서 뽑은 정확한 본문으로 교체한다.
    (LLM이 기억으로 재현하며 생기는 오류를 원천 차단)."""
    if not passage:
        return html
    lines = []
    for v in passage:
        if v["heading"]:
            lines.append(f'<p class="font-semibold text-gray-900 mt-3">〈{_esc(v["heading"])}〉</p>')
        label = f'{v["chapter"]}:{v["verse"]}' if multi_chapter else str(v["verse"])
        lines.append(f'<p><strong>{label}</strong> {_esc(v["text"])}</p>')
    inner = "\n".join(lines)
    pat = re.compile(r'(<div class="scripture-text-section[^"]*"[^>]*>).*?(</div>)', re.S)
    if pat.search(html):
        return pat.sub(lambda m: m.group(1) + "\n" + inner + "\n" + m.group(2),
                       html, count=1)
    return html


# ==========================================================================
# 1. 전사 (Transcription)
# ==========================================================================
def _run(cmd, log, env=None):
    log(f"$ {' '.join(cmd)}")
    run_env = None
    if env:
        run_env = dict(os.environ)
        run_env.update(env)
    p = subprocess.run(cmd, capture_output=True, text=True, env=run_env)
    if p.stdout:
        log(p.stdout.strip())
    if p.returncode != 0:
        log(p.stderr.strip())
        raise RuntimeError(f"명령 실패({p.returncode}): {' '.join(cmd)}\n{p.stderr}")
    return p.stdout


def _vtt_to_text(vtt):
    """YouTube 자막(VTT)을 평문으로. 자동생성 자막의 롤링 중복을 제거한다."""
    import html as _html
    lines = []
    for raw in vtt.splitlines():
        l = raw.strip()
        if not l:
            continue
        if l.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        if "-->" in l:
            continue
        if re.match(r"^\d+$", l):
            continue
        l = re.sub(r"<[^>]+>", "", l)          # <c>, 타임스탬프 태그 제거
        l = _html.unescape(l).strip()
        if not l:
            continue
        if lines and lines[-1] == l:            # 연속 중복 제거(롤링 자막)
            continue
        lines.append(l)
    text = " ".join(lines)
    return re.sub(r"\s+", " ", text).strip()


def download_youtube_captions(url, work_dir, log, progress=None, langs=("ko", "ko-KR", "ko-orig")):
    """유튜브 (자동생성 포함) 한국어 자막을 받아 평문으로 반환. 없으면 None."""
    prog = progress or (lambda *a, **k: None)
    try:
        import yt_dlp
    except ImportError:
        return None
    os.makedirs(work_dir, exist_ok=True)
    for f in os.listdir(work_dir):                # 이전 자막 정리
        if f.startswith("sub.") and f.endswith(".vtt"):
            try:
                os.remove(os.path.join(work_dir, f))
            except OSError:
                pass
    prog(None, "자막 가져오기")
    log("[자막] 유튜브 자막(자동생성 포함) 확인 중...")
    opts = {
        "skip_download": True,
        "writeautomaticsub": True,
        "writesubtitles": True,
        "subtitleslangs": list(langs),
        "subtitlesformat": "vtt",
        "outtmpl": os.path.join(work_dir, "sub.%(ext)s"),
        "quiet": True, "no_warnings": True, "noplaylist": True,
        "extractor_args": {"youtube": {"player_client": ["default", "ios", "android"]}},
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as e:
        log(f"[자막] 가져오기 실패: {str(e).splitlines()[-1] if str(e) else e}")
        return None
    vtts = [f for f in os.listdir(work_dir) if f.startswith("sub.") and f.endswith(".vtt")]
    if not vtts:
        log("[자막] 한국어 자막이 없습니다 → Whisper 전사로 진행합니다.")
        return None
    vtts.sort()  # sub.ko.vtt 우선
    with open(os.path.join(work_dir, vtts[0]), encoding="utf-8") as f:
        text = _vtt_to_text(f.read())
    if len(text) < 50:
        log("[자막] 자막 내용이 너무 짧습니다 → Whisper 전사로 진행합니다.")
        return None
    log(f"[자막] 자막 사용 ({len(text)}자) — Whisper 전사를 건너뜁니다. ⚡")
    prog(100, "자막 가져오기")
    return text


def download_youtube_audio(url, work_dir, log, progress=None):
    """yt-dlp(파이썬 모듈)로 최적 오디오를 내려받아 파일 경로 반환.
    YouTube 플레이어 변경으로 실패하면 여러 player_client 로 순차 재시도한다."""
    os.makedirs(work_dir, exist_ok=True)
    outtmpl = os.path.join(work_dir, "audio.%(ext)s")
    prog = progress or (lambda *a, **k: None)

    def _hook(d):
        if d.get("status") == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            if total:
                prog(min(99.0, d.get("downloaded_bytes", 0) / total * 100.0), "오디오 다운로드")
        elif d.get("status") == "finished":
            prog(100, "오디오 다운로드")

    def _find_audio():
        for f in sorted(os.listdir(work_dir)):
            if f.startswith("audio."):
                return os.path.join(work_dir, f)
        return None

    def _clear():
        for f in os.listdir(work_dir):
            if f.startswith("audio."):
                try:
                    os.remove(os.path.join(work_dir, f))
                except OSError:
                    pass

    try:
        import yt_dlp
    except ImportError:
        yt_dlp = None

    if yt_dlp is not None:
        base = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [_hook],
        }
        # 기본 -> 여러 클라이언트 순차 폴백 (YouTube 차단/플레이어 변경 대응)
        attempts = [None, ["tv"], ["ios"], ["android"], ["mweb"], ["web_safari"]]
        last_err = None
        for clients in attempts:
            _clear()
            opts = dict(base)
            if clients:
                opts["extractor_args"] = {"youtube": {"player_client": clients}}
                log(f"[yt-dlp] player_client={clients} 로 재시도...")
            else:
                log("[yt-dlp] 오디오 다운로드 중...")
            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    path = ydl.prepare_filename(info)
                if not os.path.exists(path):
                    path = _find_audio()
                if path and os.path.exists(path):
                    log(f"[yt-dlp] 다운로드 완료: {os.path.basename(path)}")
                    return path
                last_err = "다운로드 파일을 찾지 못함"
            except Exception as e:
                last_err = str(e).splitlines()[-1] if str(e) else repr(e)
                continue
        raise RuntimeError(
            "유튜브 다운로드에 실패했습니다: " + str(last_err) + "\n"
            "  대부분 yt-dlp 버전이 오래되어 생기는 문제입니다. 터미널에서 아래를 실행해\n"
            "  yt-dlp를 최신으로 올린 뒤 다시 시도하세요:\n"
            "    ~/Desktop/설교요약/sermon-app/.venv/bin/pip install -U yt-dlp\n"
            "  그래도 안 되면 미디어 파일을 직접 내려받아 '미디어 파일'로 요약하세요."
        )

    # yt-dlp 모듈이 아예 없을 때
    raise RuntimeError(
        "yt-dlp 가 설치되어 있지 않습니다.\n"
        "  해결: run_mac.command 로 실행하거나  pip3 install yt-dlp faster-whisper  를 실행하세요."
    )


def _transcribe_mlx(audio_path, whisper_model, log, prog, language="ko"):
    """Apple Silicon 이면 mlx-whisper(Apple GPU)로 전사 시도. 불가하면 None."""
    import sys
    import platform
    if sys.platform != "darwin" or platform.machine() != "arm64":
        return None
    try:
        import mlx_whisper
    except ImportError:
        return None
    repo = f"mlx-community/whisper-{whisper_model}-mlx"
    log(f"[Whisper] Apple GPU(MLX) 전사 시도: {repo}")
    prog(None, "전사 (Apple GPU)")
    try:
        result = mlx_whisper.transcribe(audio_path, path_or_hf_repo=repo,
                                        language=language)
        text = (result.get("text") or "").strip()
        if len(text) > 20:
            prog(100, "전사")
            log(f"[Whisper] MLX 전사 완료 ({len(text)}자) ⚡")
            return text
        log("[Whisper] MLX 결과가 비정상적으로 짧음 → faster-whisper로 진행")
    except Exception as e:
        log(f"[Whisper] MLX 실패 → faster-whisper로 진행: {str(e).splitlines()[-1] if str(e) else e}")
    return None


def transcribe(audio_path, whisper_model, log, progress=None, language="ko"):
    """mlx-whisper(Apple GPU) -> faster-whisper -> openai-whisper 순으로 전사.
    progress(pct, phase) 로 단계/진행률을 보고한다."""
    prog = progress or (lambda *a, **k: None)
    log(f"[Whisper] 모델='{whisper_model}' 준비 (파일: {os.path.basename(audio_path)})")
    # --- mlx-whisper (Apple Silicon GPU, 설치돼 있으면 가장 빠름) ---
    text = _transcribe_mlx(audio_path, whisper_model, log, prog, language)
    if text:
        return text
    # --- faster-whisper ---
    try:
        from faster_whisper import WhisperModel
        log("[Whisper] 모델 로딩 중... (처음이면 모델 다운로드로 수 분 걸릴 수 있어요)")
        prog(None, "모델 로딩/캐시")
        model = WhisperModel(whisper_model, device="auto", compute_type="int8")
        log("[Whisper] 모델 로딩 완료. 전사를 시작합니다.")
        segments, info = model.transcribe(audio_path, language=language, vad_filter=True)
        total = getattr(info, "duration", 0) or 0
        parts = []
        last_report = -5.0
        for seg in segments:
            parts.append(seg.text.strip())
            if total:
                pct = min(99.0, seg.end / total * 100.0)
                prog(pct, "전사")
                if seg.end - last_report >= max(total * 0.05, 15):  # 로그는 드문드문
                    log(f"[Whisper] 전사 {pct:4.0f}%  ({int(seg.end//60)}:{int(seg.end%60):02d} / {int(total//60)}:{int(total%60):02d})")
                    last_report = seg.end
        prog(100, "전사")
        text = " ".join(parts).strip()
        log(f"[Whisper] 전사 완료 ({len(text)}자)")
        return text
    except ImportError:
        log("[Whisper] faster-whisper 미설치 -> openai-whisper 시도")
    # --- openai-whisper (ffmpeg CLI 필요) ---
    try:
        import whisper
    except ImportError:
        raise RuntimeError(
            "Whisper 가 설치되어 있지 않습니다.\n"
            "  해결: run_mac.command 로 실행하거나,\n"
            "  터미널에서  pip3 install faster-whisper  를 실행하세요."
        )
    log("[Whisper] 모델 로딩 중...")
    prog(None, "모델 로딩/캐시")
    model = whisper.load_model(whisper_model)
    prog(None, "전사")
    result = model.transcribe(audio_path, language=language)
    text = result.get("text", "").strip()
    prog(100, "전사")
    log(f"[Whisper] 전사 완료 ({len(text)}자)")
    return text


def get_transcript(source, is_youtube, whisper_model, work_dir, log, progress=None,
                   prefer_captions=True):
    if is_youtube:
        if prefer_captions:
            cap = download_youtube_captions(source, work_dir, log, progress)
            if cap:
                return cap
        audio = download_youtube_audio(source, work_dir, log, progress)
    else:
        if not os.path.exists(source):
            raise RuntimeError(f"미디어 파일을 찾을 수 없습니다: {source}")
        audio = source
    return transcribe(audio, whisper_model, log, progress)


# ==========================================================================
# 2. LLM 요약 -> HTML 생성 (LM Studio, OpenAI 호환 API)
# ==========================================================================
def list_lm_models(base_url):
    """LM Studio에 로드된 모델 목록 반환."""
    import urllib.request
    url = base_url.rstrip("/") + "/v1/models"
    with urllib.request.urlopen(url, timeout=5) as r:
        data = json.loads(r.read().decode())
    return [m["id"] for m in data.get("data", [])]


# ==========================================================================
# OpenRouter(클라우드 LLM) 연동
# ==========================================================================
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_OPENROUTER_KEY_PATH = "/Users/kbd/Desktop/mathDB/api/openrouter_api.txt"

# 설교 요약(긴 한국어 텍스트 · 깊이 있는 신학적 분석)에 강한 것으로 알려진 벤더를 우선순위에 둔다.
_OR_PREFERRED_VENDORS = (
    "anthropic", "openai", "google", "deepseek", "qwen",
    "meta-llama", "mistralai", "x-ai", "cohere", "moonshotai", "z-ai", "minimax",
)
# 요약/채팅에 부적합한(임베딩·음성·조정 전용 등) 모델은 목록에서 제외한다.
_OR_EXCLUDE_SUBSTR = ("embed", "whisper", "tts", "moderation", "rerank", "guard",
                      "-stt", "speech", "vision-only")


def read_openrouter_key(key_path=None):
    """OpenRouter API 키 파일을 읽어 반환(공백 제거). 없으면 빈 문자열."""
    path = key_path or DEFAULT_OPENROUTER_KEY_PATH
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def _auth_headers(base_url, key_path=None):
    """OpenRouter 요청에만 Authorization/식별 헤더를 추가한다(LM Studio 등 로컬 서버는 그대로)."""
    if "openrouter.ai" not in (base_url or ""):
        return {}
    headers = {"HTTP-Referer": "https://github.com/local/sermon-app",
               "X-Title": "Sermon App"}
    key = read_openrouter_key(key_path)
    if key:
        headers["Authorization"] = f"Bearer {key}"
    return headers


def list_openrouter_models(key_path=None, limit=150):
    """OpenRouter 전체 모델 카탈로그에서 설교 요약(긴 한국어 텍스트·깊이 있는 분석)에
    적합한 모델을 추려 추천순으로 정렬해 반환한다.
    반환: [{"id": "anthropic/claude-3.7-sonnet", "label": "anthropic/claude-3.7-sonnet · 200K ctx"}, ...]"""
    import urllib.request
    import urllib.error
    req = urllib.request.Request(OPENROUTER_BASE_URL + "/models")
    key = read_openrouter_key(key_path)
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"OpenRouter 모델 목록 조회 실패(HTTP {e.code}). "
                           f"API 키 파일을 확인하세요: {key_path or DEFAULT_OPENROUTER_KEY_PATH}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"OpenRouter에 연결할 수 없습니다({e.reason}).")

    scored = []
    for m in data.get("data", []):
        mid = m.get("id") or ""
        if not mid or any(x in mid.lower() for x in _OR_EXCLUDE_SUBSTR):
            continue
        ctx = m.get("context_length") or (m.get("top_provider") or {}).get("context_length") or 0
        if ctx and ctx < 8000:
            continue
        vendor = mid.split("/")[0] if "/" in mid else ""
        is_free = mid.endswith(":free")
        # 낮을수록 우선: (선호 벤더+유료=0, 그 외=1, 선호벤더+무료=1, 그 외+무료=2)
        tier = (0 if (vendor in _OR_PREFERRED_VENDORS and not is_free) else
               (2 if is_free and vendor not in _OR_PREFERRED_VENDORS else 1))
        name = m.get("name") or mid
        ctx_label = f" · {ctx // 1000}K ctx" if ctx else ""
        scored.append((tier, -ctx, mid, {
            "id": mid,
            "label": f"{mid}{ctx_label}",
            "name": name,
            "context_length": ctx,
        }))
    if not scored:
        raise RuntimeError("OpenRouter에서 사용 가능한 모델을 찾지 못했습니다.")
    scored.sort(key=lambda t: (t[0], t[1], t[2]))
    return [s[3] for s in scored[:limit]]


def _load_style_template():
    path = os.path.join(BASE_DIR, "style_template.html")
    with open(path, encoding="utf-8") as f:
        return f.read()


def build_prompt(transcript, meta, style_template, passage_text=""):
    th = meta.get("theme") or {"grad": "from-blue-900 to-indigo-900",
                               "eyebrow": "text-indigo-300", "accent": "text-indigo-400"}
    # 본문 섹션 출처: bible.db에서 추출한 정확한 본문이 있으면 그것을, 없으면 기존처럼 표준 본문 재현
    if passage_text:
        src_desc = ("아래 '# 정확한 성경 본문(bible.db 제공)' 블록에 실린 절 텍스트를 그대로 복사해")
        passage_section = (
            "\n# 정확한 성경 본문(bible.db 제공 — 이 텍스트만 사용)\n"
            "아래는 이 설교 본문의 개역개정 표준 성경 본문을 데이터베이스에서 정확히 추출한 것입니다.\n"
            "'오늘의 성경 본문' 섹션과 카드 안 모든 <blockquote> 인용은 반드시 아래 절 텍스트를 '글자 그대로'\n"
            "복사해 사용하고, 절대 기억으로 재구성하거나 임의로 다듬지 마세요. (각 줄: 절번호 뒤에 본문)\n"
            + passage_text + "\n")
    else:
        src_desc = "개역개정 표준 성경 본문을 정확히 찾아"
        passage_section = ""
    system = (
        "당신은 개혁주의 언약신학 관점의 설교 요약 전문가이자 프론트엔드 개발자입니다. "
        "설교 전사를 깊이 있게 분석해, 주어진 HTML 스타일 템플릿과 완전히 동일한 디자인 시스템"
        "(Noto Sans KR, 색상 카드, keyword 형광펜, blockquote+cite 인용)으로 설교의 핵심을 "
        "'간결하면서도 충실하게' 담은 설교 요약 HTML 한 페이지를 만듭니다. 이 문서는 한눈에 보는 "
        "인포그래픽이되, 뼈대만 남긴 개조식이 아니라 각 요점에 이해를 돕는 적절한 설명이 곁들여진 형태입니다 — "
        "설교의 모든 핵심(논지·적용·결론)을 빠짐없이 담고, 군더더기와 반복은 덜어내되 내용의 알맹이와 "
        "필요한 설명은 살립니다. 한두 줄로 끝내는 빈약한 요약도, 끝없이 늘어지는 장황한 요약도 만들지 않으며, "
        "깊이는 '길이'가 아니라 '설교의 핵심을 정확히, 충분한 설명과 함께 짚었는가'로 확보합니다. "
        "문서 전체는 \"~입니다/~습니다\" 체의 "
        "정중한 경어체로, 설교를 바깥에서 전달하는 관찰자 시점이 아니라 성도에게 직접 선포하는 "
        "현장의 목소리로 씁니다. "
        "가장 중요한 원칙은 '충실성'입니다: 요약은 설교자가 실제로 선포한 논지·강조점·적용 대상·결론을 "
        "그대로 재현해야 하며, 전사에 없는 일반적인 신학 지식이나 상투적 메시지로 대체하는 것을 금지합니다. "
        "설교를 들은 성도가 요약을 읽고 '오늘 선포된 말씀이 바로 이것'이라고 알아볼 수 있어야 합니다. "
        "입력 전사는 자동 음성인식(ASR) 결과라 오탈자와 동음이의 오류가 있을 수 있으므로, "
        "문맥에 맞게 교정하고 특히 성경 용어·책이름·인명·지명은 개역개정 표준 표기로 반드시 재검증합니다. "
        "설명 없이 오직 HTML 문서만 출력하세요."
    )
    user = f"""# 작업
아래 [설교 전사]를 깊이 있게 분석하여, [스타일 템플릿]과 동일한 디자인의 '핵심이 충실하되 간결한' 설교 요약 HTML 한 페이지를 만드세요.
목표는 설교의 모든 핵심을 담으면서도 한눈에 스캔되는 인포그래픽입니다 — 자세함과 간결함의 균형을 최우선으로 삼으세요.

# 반드시 지킬 것 (형식)
- 출력은 <!DOCTYPE html> 로 시작하는 완전한 HTML 문서 하나. 코드펜스(```)나 설명 금지.
- 템플릿의 <head>(스타일시트 링크, Google Fonts, <style>)와 전체 레이아웃 구조를 '그대로' 유지.
- <title> 과 og:title/og:description/og:image 메타태그를 이 설교 내용에 맞게 채울 것.
  (og:image 는 템플릿의 기존 값을 그대로 사용)
- 헤더: 시리즈명(있으면), 설교 제목, "설교자 | 본문 | 날짜와 예배명", 핵심 주제 박스.
- ★헤더 색상 테마(설교 종류별 구별): 헤더의 그라디언트 div 는 반드시
  class="absolute inset-0 bg-gradient-to-r {th['grad']} opacity-50" 로,
  시리즈명(eyebrow) 텍스트는 "{th['eyebrow']}" 클래스로,
  핵심 주제 박스의 라벨은 "{th['accent']} font-bold" 클래스로 지정할 것.
  (본문 아래 인포그래픽 카드 색상 규칙은 그대로 유지 — 헤더 색만 종류별로 바뀜)
- ★본문 섹션(성경 본문 무결성 — 절대 규칙): 전사의 낭독 여부와 관계없이, 본문({meta.get('scripture') or '해당 범위'})의
  {src_desc} '모든 절' 단위로 <p><strong>절번호</strong> 본문</p> 형식으로 빠짐없이 싣는다.
  전사 속 낭독 부분은 ASR 오인식으로 누락·왜곡될 수 있으므로 본문 섹션의 출처로 삼지 말 것 —
  반드시 개역개정 표준 본문 자체를 정확하게 재현한다. 각 절의 텍스트는 단 한 글자도 축약·요약·의역·
  생략·재구성하지 않는다("요약"·"핵심만 발췌"·"의미가 통하도록 다듬기" 절대 금지, 원문 그대로가 원칙).
  이 섹션은 어디까지나 근거 본문 제공용이며, 설교 내용을 얼마나 충실하고 깊이 있게 요약하는지가
  이 앱의 가장 중요한 목표임을 잊지 말 것 — 본문 섹션에 공들이느라 카드 내용(설교자의 논지·적용)이
  빈약해져서는 안 된다.
- ★맨 아래 두 태그(재생 기능에 필수 — 절대 누락·혼동 금지): <input type="hidden" id="youtube-link">
  의 value 를 아래 유튜브 링크로 채우고, 바로 그 다음 </body> 직전에 <script src="script.js"></script>
  를 정확히 그대로 한 줄 유지한다. 이 태그는 <head>에 있는 tailwind CDN <script> 태그와는
  '완전히 다른 것'이다 — 절대 tailwind 스크립트를 여기 대신 넣거나 중복 삽입하지 말 것.
  이 script.js 가 빠지면 사이트의 전역 오디오 재생 기능이 그 페이지에서 통째로 작동하지 않게 되는
  치명적 오류이므로 반드시 </body> 바로 앞에 있는지 스스로 확인한다. 푸터의 교회명/코너명도 메타에 맞게.

# 반드시 지킬 것 (설교 충실성 — 가장 중요)
- ★제목: 설교자가 실제로 반복 강조한 핵심 메시지·중심 선포에서 도출한다.
  전사에 등장하지 않는 일반적 권면형 제목(예: '~에 귀를 기울이라', '~를 회복하라')을 지어내지 말 것.
  제목을 정한 뒤 스스로 검증: "설교자가 이 제목의 내용을 실제로 말했는가?" 아니라면 다시 정한다.
  제목 옆·헤더의 본문 표기는 설교가 다룬 '전체 범위'(예: 이사야 3:1-12)로 적는다. 첫 절만 적지 말 것.
- ★적용 대상: 설교자가 명시한 '일차 적용 대상'을 절대 바꾸지 않는다.
  설교자가 "이 말씀은 오늘날 교회에 적용해야 한다"고 강조했다면 모든 카드의 서술도 교회·성도 중심으로,
  사회를 향했다면 사회 중심으로 쓴다. 설교자의 고유한 적용을 '일반적인 국가·사회 타락, 심판 메시지'로
  뭉뚱그려 치환하는 것을 금지한다.
- ★절별 해설의 구체성: 설교자가 본문 범위의 여러 절을 짚으며 해설했다면, 각 해설의 '구체적 내용'
  (해당 절 번호, 든 예화·비유, 언급한 통계·시사·현실 지적, 꼬집은 세태)을 그대로 살려 쓴다.
  '지도력 상실', '공동체 붕괴' 같은 추상어 한 마디로 뭉뚱그리지 말고, 설교자가 묘사한 구체적 현상을
  카드 불릿에 절 번호와 함께 풀어쓴다(예: "철없는 리더십(4절): …").
- ★결론 보존: 설교자의 결론 선포에 등장한 핵심 단어를 그대로 보존한다. 특히 설교자가
  '예수 그리스도'를 결론으로 선포했다면 요약의 결론 카드도 반드시 그리스도로 끝나야 하며,
  이를 '하나님', '그분' 같은 일반적 표현으로 흐리는 것을 금지한다. 가능하면 결론부의 선포 문장을
  <blockquote>로 직접 인용해 마무리한다.
- ★구속사적(그리스도 중심) 결론: 본문이 구약의 심판·인간의 실패·역사적 사건을 다루더라도,
  결론과 '오늘의 적용'은 반드시 우리의 참된 소망이자 해답이신 예수 그리스도와 복음으로 연결지어
  마무리한다. 설교자가 그리스도를 명시적으로 언급했다면 그 표현을 그대로 살려 쓰고(위 결론 보존
  원칙 우선), 설교자의 결론이 그리스도를 명시하지 않았더라도 개혁주의 언약신학의 구속사적 관점에서
  본문이 궁극적으로 가리키는 그리스도와 복음을 향해 자연스럽게 짚어주며 마무리한다
  (전사에 없는 이야기를 새로 창작하는 것이 아니라, 설교의 흐름 안에서 그리스도를 향한 시선을
  더해주는 것). "이렇게 행동하면 복 받는다" 식의 기복주의적 결론이나, 그리스도 없이 "이렇게
  살자"로만 끝나는 단순 도덕주의적 결론은 지양한다.
- ★핵심 주제 박스도 위 원칙에 따라, 설교자의 실제 강조점·적용 대상·결론이 드러나게 압축한다.

# 반드시 지킬 것 (구성 — 설교 내용 중심, 매우 중요)
- 먼저 설교 전사를 분석해 실제로 다뤄진 '주제'들을 뽑고, 그 주제별로 인포그래픽 카드를 구성한다.
  카드 수는 설교 내용에 따라 자연스럽게 정한다(대개 3~7개). 정해진 개수를 채우려고
  내용을 억지로 쪼개거나 전사에 없는 내용으로 카드를 만들지 않는다.
- 카드 색상은 내용 성격에 맞게 팔레트에서 골라 쓴다:
  orange=역사·배경, purple=원리·본질, rose=경고·배격, blue=목록·규례, emerald=적용·실천, gray=결론·권면.
  (모든 색을 다 쓸 필요 없음. 마지막 카드는 결론·적용으로 마무리)
- ★모든 카드의 내용은 반드시 설교 전사에 실제로 나온 논지·예화·인용·권면에 근거한다.
  전사에 없는 해석이나 일반적인 신학 지식으로 지어내 채우는 것을 금지한다.
- ★비유·문맥의 정확한 주해(문자주의 오류 방지): 본문에 나오는 역사적 배경·문화적 관습·문학적
  비유(메타포)를 표면적 문자 그대로만 해석하거나 지나치게 단순화하지 말 것. 설교자가 그 비유·배경을
  풀어 설명한 내용을 근거로, 그것이 가리키는 영적 본질(예: 통치와 질서의 원리, 하나님의 영광을
  거스르는 것으로서의 죄의 근원, 언약적 의미)까지 문맥에 맞게 깊이 있게 분석하여 카드에 녹여낸다.
  단순히 '~을 뜻한다'는 한 줄 정의로 끝내지 말고, 그 비유가 왜 그런 의미를 갖는지 근거를 함께 서술한다.

# 반드시 지킬 것 (구조화와 어조 — 매우 중요)
- 카드 배치는 설교의 논리적 흐름(서론 → 본론(대지별) → 결론)을 따라 순서대로 구성해,
  읽는 사람이 설교를 처음부터 끝까지 다시 따라가는 느낌을 받도록 한다. 각 논리 단위를
  <div class="card ...">로 작성한다(색상 규칙은 위 카드 색상 규칙을 따름).
- 핵심 위주 서술: 설교자가 든 예시·비유·해석·적용점을 놓치지 않고, 각 요점에 이해를 돕는 설명을 간결히 붙인다.
  장황한 문단은 피하되 설명 없는 뼈대만 남기지도 않는다. 나열할 내용이 여럿이면
  <ul class="list-disc ..."><li>...</li></ul> 목록으로 정리하되, 각 항목에 '핵심어 + 짧은 설명'을 함께 담는다.
- ★어조: 전체 문서는 "~입니다", "~습니다" 체의 정중하고 현장감 있는 경어체를 처음부터 끝까지
  일관되게 사용한다. "설교자는 ~라고 말했다", "그는 ~라고 강조했다" 식으로 설교를 바깥에서
  전달하는 제3자 관찰자 시점은 금지한다. 대신 그 설교의 메시지를 성도에게 직접 선포·설명하는
  현장의 목소리로 서술한다(예: "오늘 본문은 ~을 보여줍니다", "우리는 ~해야 합니다").
- ★성경 인용(신학적 왜곡 절대 금지 — 매우 중요): 카드 안에서 근거로 삼는 구절은 <blockquote>와 <cite>를
  함께 사용한다(예: <blockquote>"...말씀 인용..."<cite>이사야 3:4</cite></blockquote>).
  이 인용문은 새로 쓰거나 기억으로 재구성하지 말고, 반드시 위 '오늘의 성경 본문' 섹션에 이미 적어 놓은
  해당 절의 문장을 글자 그대로 그 자리에서 복사해서 붙여넣는다. <cite>에 적는 절 번호는 그 인용문이
  실제로 나온 절 번호와 정확히 일치해야 한다. 절 번호와 문장, 주어(의인/악인 등)와 서술어(복/화 등)를
  뒤섞거나 다른 절의 내용과 합성하는 것은 명백한 신학적 왜곡이며 절대 금지한다.
  (실제 발생했던 오류 예: 이사야 3:10-11은 "의인에게는 복이, 악인에게는 화가 있으리라"는 대조 구절인데,
  이를 "의인에게는 복이 있으리니 그들이 자기 죄악 때문에 복을 받으리라"처럼 절 번호와 주어를 뒤섞어
  의인이 죄 때문에 복을 받는다는 앞뒤가 맞지 않는 문장으로 지어내면 안 된다.)
- 강조: 각 카드의 핵심 키워드나 문장은 <span class="keyword">로 감싸 시각적으로 강조한다(카드당 2~4곳).

# 반드시 지킬 것 (분량과 깊이 — 간결함과 충실함의 균형, 매우 중요)
- ★핵심 원칙: 설교의 핵심(논지·적용·결론)을 빠짐없이 담되, 원래의 장황한 요약보다는 간결하게 정리한다.
  다만 '간결함'이 '설명 없는 뼈대'를 뜻하지는 않는다 — 각 요점에는 그것이 왜 그러한지, 무엇을 뜻하는지
  독자가 이해되도록 적절한 설명을 반드시 덧붙인다. 반복과 미사여구만 덜어내고, 내용의 알맹이는 살린다.
- 각 카드는 '도입 2~3문장' + '핵심 불릿 3~4개'로 구성한다. 도입에서 카드의 요지와 배경을 설명하고,
  각 불릿은 핵심어로 시작하되 그 뒤에 1~2문장의 충실한 설명(근거·예화·적용)을 붙인다.
  즉 뼈대만 나열하는 완전한 개조식이 아니라, '핵심어 + 설명'이 결합된 형태로 쓴다.
  한 줄짜리 빈약한 카드도, 문단이 끝없이 늘어지는 카드도 모두 지양한다.
- 설교의 예화·비유·역사적 배경·적용·권면은 핵심을 추려 담되, 독자가 맥락을 이해할 만큼은 풀어 쓴다.
- ★성경 인용: 본론 카드에는 그 논지의 근거가 되는 성경 <blockquote> 인용을 적극 활용한다.
  문서 전체에 최소 2~3개 이상의 <blockquote> 인용을 담는 것을 원칙으로 한다.
  각 인용은 '오늘의 성경 본문' 섹션의 해당 절을 글자 그대로 복사해 붙이고, <cite>에 절 번호를 정확히 단다.
- 핵심 주제 박스는 2문장 내외로 설교 전체를 압축한다.
- 결론 카드는 설교가 실제로 맺은 결론·적용을 '그 흐름 그대로' 담는다. 정해진 틀(예: '버릴 것 vs 취할 것',
  '잡아야 할 것 vs 붙잡아야 할 것', '순종 vs 거절' 같은 2열 대비표)을 기계적으로 만들어 붙이지 말 것 —
  설교자가 실제로 그런 대비 구조로 마무리했을 때만 그 형식을 쓰고, 아니라면 설교의 실제 맺음말을
  자연스럽게 서술한다.
- ★분량 기준: 억지로 길이를 채우지도, 지나치게 축약하지도 않는다. 카드 개수는 설교 내용에 맞게 대개 4~6개.
  각 카드가 '핵심 + 이해에 필요한 설명'을 갖춘, 읽기에 부담 없되 알맹이가 분명한 분량을 목표로 한다.

# 반드시 지킬 것 (전사 오류 교정 — 중요)
- 아래 전사는 자동 음성인식(ASR) 결과라 오탈자·띄어쓰기 오류·동음이의어 오인식이 섞여 있다. 문맥에 맞게 자연스럽게 교정하여 서술한다.
- 특히 다음은 반드시 개역개정 성경 표준 표기로 재검증하여 정확히 적는다:
  · 성경 책 이름(예: 이사야/예레미야애가/데살로니가전서 등)
  · 성경 인물 이름(예: 다윗/모세/사도 바울/느헤미야 등)
  · 지명(예: 예루살렘/시온/갈릴리/소돔과 고모라 등)
  · 신학·예배 용어(예: 언약/칭의/성화/속죄/보혈 등)
- 장·절 표기는 본문({meta.get('scripture') or '해당 본문'})의 범위와 대조하여 어긋나면 바로잡는다.
- 확신이 서지 않는 고유명사는 본문·문맥에 근거해 가장 타당한 성경적 표기를 선택하고, 억지 추측으로 왜곡하지 않는다.

# 반드시 지킬 것 (출력 전 최종 자체 검증 — 절대 생략 금지)
HTML을 출력하기 직전, 작성한 결과를 스스로 다시 읽으며 아래 항목을 하나씩 점검하고, 문제가 있으면
그 부분을 고쳐서 최종본에는 아래 오류가 하나도 남지 않도록 한다:
1. 본문 섹션과 카드 인용 대조: 문서 안의 모든 <blockquote> 인용문을 하나씩, 그 <cite>(또는 절 번호
   표기)가 가리키는 절 번호로 '오늘의 성경 본문' 섹션을 찾아가 실제 문장과 글자 그대로 일치하는지
   대조한다. 하나라도 다르면(단어가 바뀌었거나, 다른 절과 섞였거나, 절 번호가 틀렸으면) 본문 섹션의
   문장을 그대로 복사해 바로잡는다.
2. 논리·신학적 자기모순 검사: 각 인용문과 그 해설이 상식적으로도, 개혁주의 신학적으로도 말이 되는지
   확인한다. 예를 들어 "의인이 자기 죄악 때문에 복을 받는다"처럼 주어와 서술어, 원인과 결과가
   뒤집혀 앞뒤가 안 맞는 문장, 본문의 대조 구조(예: 의인=복 vs 악인=화, 순종=생명 vs 불순종=심판)를
   무너뜨리는 문장이 없는지 반드시 확인한다. 이런 문장을 발견하면 절대 그대로 두지 말고 실제 본문에
   맞게 다시 쓴다.
3. 절 번호 정합성: 각 카드에서 "(N절)"로 언급한 번호가 그 절의 실제 내용과 맞는지 다시 확인한다.
4. 위 1~3 점검을 통과하지 못한 상태로는 절대 최종 출력을 하지 않는다 — 반드시 고친 뒤에 출력한다.

# 메타 정보
- 설교자: {meta['preacher']}
- 설교 종류: {meta['type_name']} ({meta['service']})
- 날짜: {meta['date_kr']}
- 본문(있으면): {meta.get('scripture') or '(전사에서 추론)'}
- 제목(있으면): {meta.get('title') or '(전사에서 도출)'}
- 교회명: {meta['church']}
- 유튜브 링크: {meta.get('youtube') or ''}
- 헤더 그라디언트 클래스: {th['grad']}
- 헤더 eyebrow 클래스: {th['eyebrow']}
- 헤더 accent 클래스: {th['accent']}
{passage_section}
# 스타일 템플릿
{style_template}

# 설교 전사
{transcript}
"""
    return system, user


def _inline_tailwind(html):
    """생성된 HTML의 Tailwind CDN 스크립트(또는 tailwind.css 링크)를
    컴파일된 CSS를 담은 <style>로 교체해 완전 자체 완결형으로 만든다."""
    css_path = os.path.join(BASE_DIR, "assets", "tailwind.css")
    if not os.path.exists(css_path):
        return html
    with open(css_path, encoding="utf-8") as f:
        css = f.read()
    style_tag = "<style>\n" + css + "\n</style>"
    patterns = [
        r'<script[^>]*src=["\']https://cdn\.tailwindcss\.com["\'][^>]*>\s*</script>',
        r'<link[^>]*href=["\'][^"\']*tailwind\.css["\'][^>]*>',
    ]
    for pat in patterns:
        if re.search(pat, html):
            return re.sub(pat, lambda m: style_tag, html, count=1)
    # 참조가 없으면 </head> 앞에 삽입
    if "</head>" in html:
        return html.replace("</head>", style_tag + "\n</head>", 1)
    return html



def _inline_script(html):
    """<script src="script.js"></script> 를 실제 script.js 내용을 담은 인라인 스크립트로 교체.
    하위폴더/오프라인/미리보기 어디서나 유튜브 버튼 등이 동작하도록 자체 완결형으로 만든다."""
    js_path = os.path.join(BASE_DIR, "assets", "script.js")
    if not os.path.exists(js_path):
        return html
    with open(js_path, encoding="utf-8") as f:
        js = f.read()
    tag = "<script>\n" + js + "\n</script>"
    pat = r'<script[^>]*src=["\']script\.js["\'][^>]*>\s*</script>'
    if re.search(pat, html):
        return re.sub(pat, lambda m: tag, html, count=1)
    # ★안전장치: LLM이 script.js 플레이스홀더를 빠뜨리거나(예: tailwind CDN 스크립트를
    # 실수로 중복 삽입) 다른 것으로 대체해버린 경우에도, 재생(유튜브/오디오) 기능이 통째로
    # 빠지는 사고를 막기 위해 </body> 앞에 강제로 삽입한다.
    if "</body>" in html:
        return html.replace("</body>", tag + "\n</body>", 1)
    return html + tag


def _lm_chat(base_url, model, system, user, log, temperature=0.5,
             max_tokens=12000, stream=True, on_delta=None, _allow_fallback=True):
    """LM Studio/OpenRouter(OpenAI 호환) 채팅 호출. 에러를 사람이 읽을 수 있는 메시지로
    변환하고, stream=True 면 on_delta(누적 글자수) 콜백으로 진행 상황을 보고한다.
    빈 응답(내용 없음)이 오면 비스트리밍으로 1회 자동 재시도한다."""
    import urllib.request
    import urllib.error
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }
    is_cloud = "openrouter.ai" in (base_url or "")
    prov = "OpenRouter" if is_cloud else "LM Studio"

    def _empty_msg(finish, reason_chars):
        m = f"{prov}가 빈 응답(내용 없음)을 반환했습니다."
        if reason_chars:
            m += (f" 모델이 추론(reasoning) {reason_chars:,}자만 내놓고 실제 본문을 만들지 못했습니다"
                  " — 추론에 토큰을 소진해 잘렸을 수 있습니다.")
        if finish == "length":
            m += " (finish_reason=length: 최대 토큰 도달)"
        if is_cloud:
            m += (" 추론 전용이 아닌 일반 모델을 선택하거나 잠시 후 다시 시도하세요."
                  " OpenRouter 크레딧·요금 한도도 확인하세요.")
        else:
            m += " 모델이 로드돼 있는지, context length가 충분한지 확인하세요."
        return m

    # base_url이 이미 /v1로 끝나면(OpenRouter: https://openrouter.ai/api/v1)
    # /v1을 다시 붙이지 않는다. LM Studio는 host만 있어 /v1을 붙여야 한다.
    _base = base_url.rstrip("/")
    url = _base + ("/chat/completions" if _base.endswith("/v1")
                   else "/v1/chat/completions")
    headers = {"Content-Type": "application/json"}
    headers.update(_auth_headers(base_url))
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers=headers,
    )
    try:
        resp = urllib.request.urlopen(req, timeout=1200)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            msg = json.loads(body).get("error") or body
        except Exception:
            msg = body
        if is_cloud:
            hint = ("\n  (OpenRouter API 키를 확인하세요: " + DEFAULT_OPENROUTER_KEY_PATH + ")"
                   if e.code in (401, 403) else "")
            raise RuntimeError(f"OpenRouter 오류(HTTP {e.code}): {str(msg)[:500]}{hint}")
        raise RuntimeError(f"LM Studio 오류(HTTP {e.code}): {str(msg)[:500]}\n"
                           "  (컨텍스트 길이 초과라면 LM Studio에서 context length를 늘리세요)")
    except urllib.error.URLError as e:
        if is_cloud:
            raise RuntimeError(f"OpenRouter에 연결할 수 없습니다({e.reason}).")
        raise RuntimeError(f"LM Studio에 연결할 수 없습니다({e.reason}). "
                           "LM Studio 서버가 켜져 있는지 확인하세요.")

    if not stream:
        with resp:
            data = json.loads(resp.read().decode("utf-8"))
        if isinstance(data, dict) and data.get("error"):
            raise RuntimeError(f"{prov} 오류: {str(data['error'])[:500]}")
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError(f"{prov} 응답에 결과가 없습니다: {str(data)[:300]}")
        msg0 = choices[0].get("message", {}) or {}
        content = (msg0.get("content") or "").strip()
        if content:
            return content
        reason = msg0.get("reasoning") or msg0.get("reasoning_content") or ""
        raise RuntimeError(_empty_msg(choices[0].get("finish_reason"), len(reason)))

    # --- 스트리밍(SSE) ---
    chunks, total, reason_chars, finish = [], 0, 0, None
    with resp:
        for raw in resp:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            if data_str == "[DONE]":
                break
            try:
                obj = json.loads(data_str)
            except Exception:
                continue
            if isinstance(obj, dict) and obj.get("error"):
                raise RuntimeError(f"{prov} 오류: {str(obj['error'])[:500]}")
            ch0 = (obj.get("choices") or [{}])[0]
            if ch0.get("finish_reason"):
                finish = ch0.get("finish_reason")
            delta_obj = ch0.get("delta") or {}
            delta = delta_obj.get("content")
            if delta:
                chunks.append(delta)
                total += len(delta)
                if on_delta:
                    on_delta(total)
            rd = delta_obj.get("reasoning") or delta_obj.get("reasoning_content")
            if rd:
                reason_chars += len(rd)
    text = "".join(chunks).strip()
    if text:
        return text
    # 빈 응답: 비스트리밍으로 1회 자동 재시도, 그래도 비면 원인 진단과 함께 실패
    if _allow_fallback:
        log(f"[LLM] {prov} 스트리밍이 빈 응답 → 비스트리밍으로 1회 재시도합니다...")
        try:
            return _lm_chat(base_url, model, system, user, log,
                            temperature=temperature, max_tokens=max_tokens,
                            stream=False, on_delta=on_delta, _allow_fallback=False)
        except RuntimeError as e:
            raise RuntimeError(_empty_msg(finish, reason_chars) + f"\n  (재시도도 실패: {e})")
    raise RuntimeError(_empty_msg(finish, reason_chars))


def correct_transcript(transcript, base_url, model, log, progress=None):
    """ASR 전사 오류(성경 용어·인명·지명·동음이의어)를 로컬 LLM으로 자동 교정.
    실패하면 원본을 그대로 반환한다."""
    prog = progress or (lambda *a, **k: None)
    system = (
        "당신은 한국어 설교 음성인식(ASR) 전사 교정 전문가입니다. "
        "내용을 요약하거나 재구성하지 않고, 오탈자·띄어쓰기·동음이의어 오인식만 바로잡습니다. "
        "특히 성경 책이름·인물·지명·신학 용어는 개역개정 표준 표기로 교정합니다. "
        "문장을 삭제하거나 새 내용을 추가하지 않으며, 설명 없이 교정된 전사문만 출력합니다."
    )
    user = ("다음 설교 전사문의 ASR 오류를 교정하여, 교정된 전사문 전체를 그대로 출력하세요. "
            "요약 금지, 생략 금지, 설명 금지.\n\n" + transcript)
    log(f"[교정] AI 전사 교정 시작... ({len(transcript)}자)")
    src_len = max(len(transcript), 1)

    def on_delta(n):
        prog(min(99.0, n / src_len * 100.0), "전사 교정(AI)")

    prog(None, "전사 교정(AI)")
    try:
        fixed = _lm_chat(base_url, model, system, user, log,
                         temperature=0.2,
                         max_tokens=min(20000, len(transcript) + 3000),
                         stream=True, on_delta=on_delta)
    except RuntimeError as e:
        log(f"[교정] 실패 → 원본 전사를 사용합니다: {e}")
        return transcript
    fixed = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", fixed.strip()).strip()
    if len(fixed) < len(transcript) * 0.6:
        log(f"[교정] 결과가 지나치게 짧습니다({len(fixed)}자) → 원본 전사를 사용합니다.")
        return transcript
    prog(100, "전사 교정(AI)")
    log(f"[교정] 완료 ({len(transcript)} → {len(fixed)}자)")
    return fixed


def proofread_summary_html(html, base_url, model, log, progress=None):
    """생성된 요약 HTML의 '텍스트만' 맞춤법·어법·성경 고유명사 교정. 구조는 보존.
    <style>/<script> 블록은 placeholder로 보호해 컨텍스트를 아끼고 훼손을 막는다."""
    prog = progress or (lambda *a, **k: None)
    stash = []

    def _stash(m):
        stash.append(m.group(0))
        return f"<!--KEEP{len(stash)-1}-->"

    guarded = re.sub(r"<style\b.*?</style>|<script\b.*?</script>",
                     _stash, html, flags=re.S | re.I)
    system = (
        "당신은 한국어 어문 교정 전문가이자 성경 표기 감수자입니다. "
        "주어진 HTML 문서에서 태그·속성·클래스·레이아웃과 <!--KEEP숫자--> 주석은 단 하나도 바꾸지 않고, "
        "한국어 텍스트의 맞춤법·띄어쓰기·어법 오류와 성경 인물·지명·책이름·신학 용어 표기(개역개정 기준)만 교정합니다. "
        "문장 추가·삭제·요약·재구성 금지. 설명 없이 교정된 HTML 문서 전체만 출력합니다."
    )
    user = ("다음 HTML 문서의 텍스트만 교정하여 문서 전체를 그대로 출력하세요. "
            "<!--KEEP숫자--> 주석은 반드시 원래 위치에 그대로 유지하세요.\n\n" + guarded)
    log(f"[교정] 요약 HTML 맞춤법 교정 시작... ({len(guarded):,}자, 스타일/스크립트 제외)")
    src_len = max(len(guarded), 1)

    def on_delta(n):
        prog(min(99.0, n / src_len * 100.0), "맞춤법 교정(AI)")

    prog(None, "맞춤법 교정(AI)")
    fixed = _lm_chat(base_url, model, system, user, log, temperature=0.2,
                     max_tokens=min(24000, len(guarded) + 3000),
                     stream=True, on_delta=on_delta)
    fixed = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", fixed.strip()).strip()
    m = re.search(r"<!DOCTYPE html.*?</html>", fixed, re.IGNORECASE | re.DOTALL)
    if m:
        fixed = m.group(0)
    # 구조 보존 검증: placeholder 전부 존재 + 분량 유지 + 문서 완결
    missing = [i for i in range(len(stash)) if f"<!--KEEP{i}-->" not in fixed]
    if missing or "</html>" not in fixed.lower() or len(fixed) < len(guarded) * 0.7:
        raise RuntimeError(
            "교정 결과가 원본 HTML 구조를 보존하지 못해 적용하지 않았습니다. "
            "기존 요약은 그대로 유지됩니다 — 다시 시도해 보세요.")
    for i, s in enumerate(stash):
        fixed = fixed.replace(f"<!--KEEP{i}-->", s)
    prog(100, "맞춤법 교정(AI)")
    log(f"[교정] 맞춤법 교정 완료 ({len(fixed):,}자)")
    return fixed


def _verse_map_from_html(html):
    """'오늘의 성경 본문' 섹션(scripture-text-section)에서 절번호 -> 절 텍스트(공백 제거) 매핑을 추출.
    라벨이 '3:11'(다장) 이면 절 부분(11)을 키로 쓴다."""
    m = re.search(r'scripture-text-section.*?</div>', html, re.S)
    if not m:
        return {}
    section = m.group(0)
    verses = {}
    for vm in re.finditer(r'<strong[^>]*>\s*([\d:]+)\s*</strong>\s*([^<]+?)\s*</p>', section):
        v = vm.group(1).split(":")[-1]
        if v.isdigit():
            verses[int(v)] = re.sub(r'\s+', '', vm.group(2))
    return verses


def _cite_verses(ref_text):
    """인용 라벨('이사야 3:11', '3:10-11', '10-11절', '11절')에서 '절 번호' 목록을 뽑는다.
    '장:절' 표기에서는 장이 아니라 절(뒤 숫자)을 정확히 골라낸다."""
    m = re.search(r'\d+\s*:\s*(\d+)\s*[-~]\s*(?:\d+\s*:\s*)?(\d+)', ref_text)   # 3:10-11 / 3:10-4:2
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if a <= b <= a + 200:
            return list(range(a, b + 1))
    m = re.search(r'\d+\s*:\s*(\d+)', ref_text)                                 # 3:11
    if m:
        return [int(m.group(1))]
    m = re.search(r'(\d+)\s*[-~]\s*(\d+)\s*절', ref_text)                        # 10-11절
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if a <= b <= a + 200:
            return list(range(a, b + 1))
    m = re.search(r'(\d+)\s*절', ref_text)                                      # 11절
    if m:
        return [int(m.group(1))]
    return sorted(set(int(n) for n in re.findall(r'\d+', ref_text)))


def _check_quote_accuracy(html):
    """카드 안 <blockquote> 성경 인용이 '오늘의 성경 본문' 섹션의 실제 절 문장과 일치하는지 대조한다.
    절 번호와 내용이 뒤섞이거나 지어낸 왜곡 인용(예: 이사야 3:11 오인용 사건)을 자동으로 잡아낸다."""
    verses = _verse_map_from_html(html)
    if not verses:
        return []
    problems = []
    for bm in re.finditer(r'<blockquote[^>]*>(.*?)</blockquote>', html, re.S):
        block = bm.group(1)
        cite_m = re.search(r'<cite[^>]*>([^<]*)</cite>', block)
        ref_text = cite_m.group(1) if cite_m else block
        nums = _cite_verses(ref_text)
        if not nums:
            continue
        official = "".join(verses.get(n, "") for n in nums)
        if not official:
            continue  # 본문 섹션 범위에 없는 절이면 대조 대상에서 제외
        # <cite>이사야 3:1</cite> 같은 출처 표기의 '내용'이 인용문에 섞여 오탐하지 않도록 먼저 제거
        block_wo_cite = re.sub(r'<cite[^>]*>.*?</cite>', '', block, flags=re.S)
        quote_text = re.sub(r'<[^>]+>', '', block_wo_cite)
        quote_text = re.sub(r'\s+', '', quote_text)
        quote_text = quote_text.strip('"\'“”()' + ''.join(str(d) for d in range(10)) + '절:-~ ')
        if len(quote_text) >= 6 and quote_text not in official and official not in quote_text:
            ref_label = "-".join(str(n) for n in nums) + "절"
            problems.append(
                f"카드의 성경 인용이 실제 {ref_label} 본문과 다릅니다 (신학적 왜곡 위험) — "
                f"인용된 문장: \"{re.sub(r'<[^>]+>', '', block_wo_cite).strip()[:70]}\" / "
                f"실제 {ref_label} 본문: \"{official[:70]}\". "
                "지어내거나 다른 절과 섞지 말고 '오늘의 성경 본문' 섹션의 해당 절 문장을 그대로 복사해 인용할 것."
            )
    return problems


def _repair_playback_tags(html, meta):
    """LLM이 자주 빠뜨리는 '재생 필수 태그'(youtube-link 숨김 입력, script.js 스크립트)를
    결정적으로 보정한다. 값이 이미 정해져 있는 이 두 태그의 누락만으로 전체 HTML을
    다시 생성(2회 생성)하는 낭비를 없애기 위해, 검증 '전에' 먼저 삽입해준다.
    반환: (보정된 html, 삽입한 태그 설명 리스트)."""
    inserts, repaired = "", []
    if 'id="youtube-link"' not in html:
        yt = (meta.get("youtube") or "").replace('"', "&quot;")
        inserts += f'<input type="hidden" id="youtube-link" value="{yt}">\n'
        repaired.append("youtube-link 입력")
    if not re.search(r'<script[^>]*src=["\']script\.js["\']', html):
        inserts += '<script src="script.js"></script>\n'
        repaired.append("script.js 스크립트")
    if inserts:
        if "</body>" in html:
            html = html.replace("</body>", inserts + "</body>", 1)
        else:
            html = html + "\n" + inserts
    return html, repaired


def _validate_html(html, meta):
    """생성된 HTML이 필수 요소를 갖췄는지 검사. 문제 목록(비면 통과) 반환."""
    problems = []
    low = html.lower()
    if not low.lstrip().startswith("<!doctype html"):
        problems.append("<!DOCTYPE html> 로 시작하는 완전한 HTML 문서가 아님")
    if "</html>" not in low:
        problems.append("</html> 닫는 태그가 없음 (문서가 중간에 잘림)")
    if 'id="youtube-link"' not in html:
        problems.append('<input type="hidden" id="youtube-link"> 가 누락됨')
    th = meta.get("theme") or {}
    if th.get("grad") and th["grad"] not in html:
        problems.append(f"헤더 그라디언트 클래스({th['grad']})가 적용되지 않음")
    if len(html) < 4000:
        problems.append("분량이 비정상적으로 적음 (성경 본문 섹션이나 핵심 카드가 통째로 누락됐는지 확인할 것)")
    # 성경 인용 <blockquote> 유무는 재생성 사유에서 제외(사용자 요청) — 프롬프트로만 권장한다.
    if not re.search(r'<script[^>]*src=["\']script\.js["\']', html):
        problems.append(
            '맨 아래 <script src="script.js"></script> 태그가 없음(재생 기능이 통째로 빠지는 '
            "치명적 오류 — 이 태그를 <head>의 tailwind CDN <script> 태그와 혼동해서 중복 삽입하거나 "
            "빠뜨리지 말 것. 정확히 </body> 바로 앞에 <script src=\"script.js\"></script> 한 줄만 있어야 함)"
        )
    problems.extend(_check_quote_accuracy(html))
    return problems


def generate_html(transcript, meta, base_url, model, log, progress=None,
                  temperature=0.3, max_tokens=12000):
    prog = progress or (lambda *a, **k: None)
    style_template = _load_style_template()
    # 성경 본문을 bible.db에서 정확히 추출해 LLM에 '정답'으로 제공하고, 생성 후 섹션을 직접 주입한다.
    # 본문란이 비어 있으면 전사에서 본문(책+장)을 추정해 그것으로 조회한다.
    scripture_ref = (meta.get("scripture") or "").strip()
    auto_detected = False
    if not scripture_ref:
        scripture_ref = detect_main_passage(transcript)
        if scripture_ref:
            auto_detected = True
            meta["scripture"] = scripture_ref          # 헤더 표기도 추정 본문에 맞춤
    passage = fetch_bible_passage(scripture_ref)
    multi_chapter = len({v["chapter"] for v in passage}) > 1 if passage else False
    passage_text = build_scripture_prompt_block(passage, multi_chapter) if passage else ""
    if passage and auto_detected:
        log(f"[본문] 본문란이 비어 전사에서 '{scripture_ref}'을(를) 본문으로 추정해 {len(passage)}절을 "
            "추출했습니다. (정확한 범위는 '본문'란에 직접 입력하면 더 좋습니다) ✅")
    elif passage:
        log(f"[본문] bible.db에서 '{scripture_ref}' 본문 {len(passage)}절을 추출했습니다. ✅")
    else:
        log(f"[본문] 본문을 추출하지 못했습니다(참조: {scripture_ref or '없음'}). "
            "'본문'란에 예: '이사야 3:1-12'처럼 입력하면 DB에서 정확한 본문을 넣습니다 "
            "→ 이번에는 LLM이 본문을 재현합니다.")
    system, user = build_prompt(transcript, meta, style_template, passage_text=passage_text)
    url = base_url.rstrip("/")

    def on_delta(n):
        prog(min(95.0, n / 15000 * 100.0), f"요약 HTML 생성 ({n:,}자)")

    html = ""
    for attempt in (1, 2):
        log(f"[LLM] LM Studio 요청 -> {url} (model={model}, 시도 {attempt}/2)")
        prog(None, "요약 HTML 생성")
        html = _clean_html(_lm_chat(base_url, model, system, user, log,
                                    temperature=temperature, max_tokens=max_tokens,
                                    stream=True, on_delta=on_delta))
        # 재생 필수 태그(youtube-link/script.js)는 값이 정해져 있으므로, 누락 시
        # 재생성 대신 여기서 결정적으로 보정한다 → 이 태그 누락만으로 2번 생성하지 않음.
        html, repaired = _repair_playback_tags(html, meta)
        if repaired:
            log("[보정] 누락된 재생 태그를 자동 삽입했습니다(재생성 없이 해결): "
                + ", ".join(repaired))
        problems = _validate_html(html, meta)
        if not problems:
            log("[검증] HTML 필수 요소 검사 통과 ✅")
            break
        log("[검증] 문제 발견:\n  - " + "\n  - ".join(problems))
        if attempt == 1:
            log("[검증] 문제를 지적하여 1회 재생성합니다...")
            user += ("\n\n# 이전 시도에서 발견된 문제 (이번에는 반드시 모두 해결할 것)\n- "
                     + "\n- ".join(problems))
        else:
            log("[검증] 재시도에서도 문제가 남았지만 그대로 진행합니다.")
    # DB에서 뽑은 정확한 본문으로 '오늘의 성경 본문' 섹션을 확정 주입(LLM 재현 오류 원천 차단)
    if passage:
        before = html
        html = _inject_scripture_section(html, passage, multi_chapter)
        if html != before:
            log(f"[본문] 본문 섹션을 bible.db 본문({len(passage)}절)으로 교체했습니다. ✅")
    html = _inline_tailwind(html)
    html = _inline_script(html)
    prog(100, "요약 HTML 생성")
    log(f"[LLM] HTML 생성 완료 ({len(html)}자)")
    return html


def _clean_html(text):
    """코드펜스·앞뒤 설명을 제거하고 HTML 문서를 추출한다. 모델이 <!DOCTYPE 를 빠뜨리거나
    문서 앞에 설명 문장을 붙여도, 재생성하지 않고 결정적으로 보정한다."""
    text = re.sub(r"^```[a-zA-Z]*\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text.strip())
    # 1) 정상: <!DOCTYPE ... </html> 범위만 추출
    m = re.search(r"<!DOCTYPE html.*?</html>", text, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(0)
    # 2) DOCTYPE 없이 <html>...</html> 만 있으면 DOCTYPE 보정
    m = re.search(r"<html.*?</html>", text, re.IGNORECASE | re.DOTALL)
    if m:
        return "<!DOCTYPE html>\n" + m.group(0)
    # 3) 닫는 </html>가 없어 잘렸더라도, 문서 시작 지점부터 살리고 앞쪽 설명은 버린다
    low = text.lower()
    idx = low.find("<!doctype html")
    if idx != -1:
        return text[idx:]
    idx = low.find("<html")
    if idx != -1:
        return "<!DOCTYPE html>\n" + text[idx:]
    return text


# ==========================================================================
# 3. 저장 + git 커밋/푸시
# ==========================================================================
def make_filename(prefix, date_yymmdd):
    return f"{prefix}{date_yymmdd}.html"


def _git_commit_push(repo_path, msg, log, do_push=True):
    """add → (변경 있으면) commit → push. '커밋할 것 없음'은 오류로 보지 않고, 밀리지 않은
    커밋이 있으면 그대로 push 한다. push 실패는 인증/거부를 구분해 안내한다."""
    noninteractive = {"GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": "echo"}
    _run(["git", "-C", repo_path, "add", "-A"], log)
    # 변경이 있을 때만 커밋한다(없으면 'nothing to commit'으로 실패해 push까지 막히던 문제 방지)
    status = subprocess.run(["git", "-C", repo_path, "status", "--porcelain"],
                            capture_output=True, text=True)
    if status.stdout.strip():
        _run(["git", "-C", repo_path, "commit", "-m", msg], log)
    else:
        log("[git] 커밋할 변경이 없습니다 (파일 내용이 이전과 동일) — 밀리지 않은 커밋이 있으면 그대로 push합니다.")
    if not do_push:
        log("[git] 커밋 완료 (push는 수동으로)")
        return
    # 원격보다 앞선(밀어야 할) 로컬 커밋이 있는지 확인
    ahead = subprocess.run(["git", "-C", repo_path, "rev-list", "--count", "@{u}..HEAD"],
                           capture_output=True, text=True)
    if ahead.returncode == 0 and ahead.stdout.strip() == "0":
        log("[git] 원격과 이미 동일합니다 — push할 커밋이 없습니다. ✅")
        return
    try:
        _run(["git", "-C", repo_path, "push"], log, env=noninteractive)
    except RuntimeError as e:
        low = str(e).lower()
        if any(k in low for k in ("authentication failed", "could not read username",
                                  "could not read password", "terminal prompts disabled",
                                  "permission denied", "invalid username or password",
                                  "403 forbidden", "support for password authentication")):
            raise RuntimeError(
                "GitHub 인증에 실패했습니다. 터미널에서 'gh auth login'으로 로그인하거나, "
                "HTTPS 원격이면 개인 액세스 토큰(자격 증명 도우미 osxkeychain), SSH 원격이면 SSH 키를 설정하세요. "
                "인증을 갖추면 자동 push가 정상 동작합니다.")
        if "no upstream branch" in low or "set-upstream" in low:
            raise RuntimeError(
                "현재 브랜치에 업스트림(추적 원격)이 설정돼 있지 않습니다. 터미널에서 한 번 "
                "'git -C {} push -u origin HEAD'를 실행해 업스트림을 지정하면 이후 자동 push됩니다.".format(repo_path))
        log("[git] push 거부됨 → 원격 변경분을 가져와(rebase) 다시 push합니다...")
        try:
            _run(["git", "-C", repo_path, "pull", "--rebase"], log, env=noninteractive)
            _run(["git", "-C", repo_path, "push"], log, env=noninteractive)
        except RuntimeError:
            # rebase가 실제 내용 충돌로 중간에 멈췄을 수 있다 — 그대로 두면 다음 실행 때마다
            # 이 repo의 모든 커밋/푸시가 막히므로, 반드시 안전하게 되돌려(abort) 깨끗한 상태로 만든다.
            # (방금 만든 로컬 커밋 자체는 사라지지 않는다 — 되돌리는 것은 실패한 rebase 시도뿐)
            log("[git] rebase 중 충돌 발생 → 원격의 동일 파일 변경과 겹칩니다. rebase를 안전하게 되돌립니다...")
            try:
                _run(["git", "-C", repo_path, "rebase", "--abort"], log)
            except RuntimeError:
                pass
            raise RuntimeError(
                "원격 저장소에 같은 파일의 다른 변경이 먼저 올라와 있어 자동으로 합칠 수 없습니다"
                "(다른 실행에서 방금 이 파일을 수정·푸시했을 가능성). "
                f"방금 만든 커밋은 로컬 repo({repo_path})에 안전하게 남아 있습니다 — "
                "터미널에서 해당 repo로 이동해 'git pull --rebase' 후 충돌 부분을 직접 검토·해결하고 "
                "'git add' → 'git rebase --continue' → 'git push' 로 마무리하세요."
            )
    log("[git] 커밋 및 푸시 완료 ✅")


def _upload_audio(media_src, dest_dir, media_rel, log, bitrate="48k"):
    """녹음/미디어 원본을 dest_dir/media_rel(mp3)로 변환. GitHub 용량 절약을 위해
    발화 최적화 저용량(모노 + 저비트레이트) mp3 로 인코딩. 실패 시 원본 복사."""
    target = os.path.join(dest_dir, media_rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    ff = find_ffmpeg()
    if ff:
        try:
            # 모노 다운믹스 + 저비트레이트(기본 48kbps) → 60분 설교 약 20MB 이하
            _run([ff, "-y", "-i", media_src, "-ac", "1",
                  "-codec:a", "libmp3lame", "-b:a", bitrate, target], log)
            mb = os.path.getsize(target) / (1024 * 1024)
            log(f"[오디오] 재생용 mp3 업로드 ({mb:.1f}MB, {bitrate} 모노) -> {target}")
            return "converted"
        except RuntimeError as e:
            log(f"[오디오] mp3 변환 실패({e}) → 원본 복사")
    shutil.copy(media_src, target)
    log(f"[오디오] 원본 복사 -> {target}")
    return "copied"


def save_and_push(html, repo_path, filename, log, do_push=True,
                  commit_msg=None, subdir="", media_src="", media_rel="", audio_bitrate="48k",
                  delete_source=False):
    # repo 경로가 유효하면 거기에(하위폴더 포함), 아니면 앱 내 output 폴더에 저장
    push_skip_reason = ""
    if repo_path and os.path.isdir(repo_path):
        dest_dir = os.path.join(repo_path, subdir) if subdir else repo_path
        can_push = do_push
        if not do_push:
            push_skip_reason = ("자동 푸시가 '아니오(저장만)'로 설정되어 있습니다. "
                                "고급 설정에서 '예 (저장 후 commit & push)'로 바꾸세요.")
        elif not os.path.isdir(os.path.join(repo_path, ".git")):
            can_push = False
            push_skip_reason = (f"repo 경로에 .git 폴더가 없어 git 저장소가 아닙니다({repo_path}). "
                                "GitHub에서 클론한 폴더 경로를 지정하세요.")
    else:
        dest_dir = os.path.join(BASE_DIR, "output", subdir) if subdir else os.path.join(BASE_DIR, "output")
        can_push = False
        if repo_path:
            push_skip_reason = f"repo 경로가 올바르지 않습니다({repo_path})."
            log(f"[저장] repo 경로가 올바르지 않습니다({repo_path}). 대신 output 폴더에 저장합니다.")
        else:
            push_skip_reason = "repo 경로가 설정되지 않았습니다. 고급 설정에서 repo 경로를 지정하세요."
            log("[저장] repo 경로가 설정되지 않았습니다. output 폴더에 저장합니다. (고급 설정에서 repo 경로를 지정하면 GitHub로 push됩니다)")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, filename)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    log(f"[저장] {dest}")
    # CSS/JS 는 각 페이지에 인라인됨. 녹음/미디어면 오디오 파일도 함께 업로드
    if media_src and os.path.exists(media_src) and media_rel:
        result = _upload_audio(media_src, dest_dir, media_rel, log, bitrate=audio_bitrate)
        # mp3 변환이 실제로 성공(converted)했고, 앱 내부 원본일 때만 안전하게 삭제
        if result == "converted" and delete_source:
            try:
                real = os.path.realpath(media_src)
                if real.startswith(os.path.realpath(BASE_DIR) + os.sep):
                    os.remove(media_src)
                    log(f"[오디오] 변환 완료 — 원본 삭제: {os.path.basename(media_src)}")
                else:
                    log("[오디오] 원본이 앱 폴더 밖이라 삭제하지 않습니다.")
            except OSError as e:
                log(f"[오디오] 원본 삭제 실패: {e}")

    if not can_push:
        log("[git] git push를 건너뜁니다 — " + (push_skip_reason or "파일만 저장했습니다."))
        return dest

    msg = commit_msg or f"Add sermon summary {filename}"
    try:
        _git_commit_push(repo_path, msg, log, do_push=True)
    except RuntimeError as e:
        log(f"[git] 경고: {e}")
        log("[git] 파일은 저장되었으나 push에 실패했습니다. 인증(gh auth status) 확인 후 수동으로 git push 하세요.")
    return dest


def relink_youtube(html_path, youtube_url, repo_path="", auto_push=False, log=None):
    """녹음 기반 요약의 오디오 재생 링크를 유튜브 링크로 교체하고
    업로드돼 있던 오디오 파일을 삭제한다. repo 안이면 커밋/푸시까지."""
    log = log or (lambda m: None)
    with open(html_path, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r'<input[^>]*id="youtube-link"[^>]*>', html)
    if not m:
        raise RuntimeError("이 요약에서 재생 링크(youtube-link) 입력을 찾을 수 없습니다.")
    tag = m.group(0)
    vm = re.search(r'value="([^"]*)"', tag)
    old = (vm.group(1) if vm else "").strip()
    if old.startswith("http"):
        raise RuntimeError("이미 유튜브 링크로 연결된 요약입니다. (녹음 기반 요약만 교체 가능)")
    if vm:
        new_tag = tag.replace(f'value="{vm.group(1)}"', f'value="{youtube_url}"', 1)
    else:
        new_tag = tag[:-1].rstrip("/").rstrip() + f' value="{youtube_url}">'
    html = html.replace(tag, new_tag, 1)

    # 페이지의 인라인 공통 스크립트를 최신으로 갱신
    # (예전에 생성된 페이지도 '소리만 듣기' 플레이어를 쓰게 됨)
    js_path = os.path.join(BASE_DIR, "assets", "script.js")
    if os.path.exists(js_path):
        with open(js_path, encoding="utf-8") as f:
            js = f.read()
        script_tag = "<script>\n" + js + "\n</script>"
        pat = r"<script>\s*// 설교 요약 페이지 공통 스크립트.*?</script>"
        if re.search(pat, html, re.S):
            html = re.sub(pat, lambda _: script_tag, html, count=1, flags=re.S)
            log("[연결] 페이지 공통 스크립트를 최신 버전으로 갱신")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    log(f"[연결] 재생 링크 교체: {old or '(비어 있음)'} → {youtube_url}")

    # 기존 오디오 파일 삭제 (HTML 폴더 하위의 상대경로만)
    if old:
        base = os.path.realpath(os.path.dirname(html_path))
        audio = os.path.realpath(os.path.join(base, old))
        if audio.startswith(base + os.sep) and os.path.exists(audio):
            try:
                os.remove(audio)
                log(f"[연결] 기존 오디오 파일 삭제: {old}")
            except OSError as e:
                log(f"[연결] 오디오 삭제 실패: {e}")
        else:
            log("[연결] 삭제할 오디오 파일이 없습니다.")

    # repo 안이면 커밋/푸시
    rp = os.path.realpath(repo_path) if (repo_path and os.path.isdir(repo_path)) else ""
    if rp and os.path.realpath(html_path).startswith(rp + os.sep):
        try:
            _git_commit_push(repo_path,
                             f"Relink {os.path.basename(html_path)} to YouTube (remove audio)",
                             log, do_push=auto_push)
        except RuntimeError as e:
            log(f"[git] 경고: {e}")
    else:
        log("[git] repo 밖 파일이라 git 반영은 건너뜁니다.")
    return old


# ==========================================================================
# 전체 실행 (오케스트레이션)
# ==========================================================================
def run_pipeline(*, source, is_youtube, sermon_type, custom_prefix,
                 date_yymmdd, preacher, scripture, title,
                 whisper_model, lm_url, lm_model, repo_path, church,
                 auto_push, log, progress=None, prefer_captions=True, audio_bitrate="48k",
                 delete_source_after_upload=True, transcript_text=None):
    prog = progress or (lambda *a, **k: None)
    info, prefix = resolve_prefix(sermon_type, custom_prefix)
    if not prefix:
        raise RuntimeError("파일 접두어가 비어 있습니다. (기타 선택 시 접두어를 직접 입력)")

    yy, mm, dd = date_yymmdd[0:2], date_yymmdd[2:4], date_yymmdd[4:6]
    date_kr = f"20{yy}년 {int(mm)}월 {int(dd)}일 {info['service']}".strip()

    work_dir = os.path.join(BASE_DIR, "_work")
    os.makedirs(work_dir, exist_ok=True)
    raw_path = os.path.join(work_dir, f"{prefix}{date_yymmdd}_transcript.txt")
    fixed_path = os.path.join(work_dir, f"{prefix}{date_yymmdd}_transcript_fixed.txt")

    if transcript_text:
        # 재생성 모드: 저장된 전사본으로 전사·교정 단계를 건너뛴다
        log("=== 1-2/4 저장된 전사본 사용 (재생성 모드) ===")
        log(f"[전사] 저장본 {len(transcript_text)}자 — 전사/교정을 건너뜁니다. ⚡")
        transcript = transcript_text
    else:
        log("=== 1/4 전사 시작 ===")
        transcript = get_transcript(source, is_youtube, whisper_model, work_dir, log, prog,
                                    prefer_captions=prefer_captions)
        # 전사 원본 백업 저장
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        log("=== 2/4 AI 전사 교정 ===")
        transcript = correct_transcript(transcript, lm_url, lm_model, log, prog)
        with open(fixed_path, "w", encoding="utf-8") as f:
            f.write(transcript)

    log("=== 3/4 HTML 생성 시작 ===")
    prog(None, "요약 HTML 생성")
    # 유튜브면 재생링크=유튜브 URL, 녹음/미디어면 업로드할 오디오 상대경로
    media_rel = "" if is_youtube else f"audio/{prefix}{date_yymmdd}.mp3"
    play_link = source if is_youtube else media_rel
    meta = {
        "preacher": preacher, "type_name": sermon_type,
        "service": info["service"], "date_kr": date_kr,
        "scripture": scripture, "title": title,
        "church": church, "youtube": play_link,
        "theme": info.get("theme"),
    }
    html = generate_html(transcript, meta, lm_url, lm_model, log, progress=prog)

    log("=== 4/4 저장 및 git ===")
    prog(None, "저장/업로드")
    filename = make_filename(prefix, date_yymmdd)
    subdir = info.get("subdir", "")
    media_src = "" if is_youtube else source
    dest = save_and_push(html, repo_path, filename, log, do_push=auto_push, subdir=subdir,
                         media_src=media_src, media_rel=media_rel, audio_bitrate=audio_bitrate,
                         delete_source=delete_source_after_upload)

    prog(100, "완료")
    return {"filename": filename, "path": dest, "html": html,
            "transcript_chars": len(transcript)}


def list_audio_devices():
    """macOS avfoundation 오디오 입력 장치 목록 반환. [{index, name}, ...]
    문제가 있으면 원인을 담은 RuntimeError를 던진다."""
    ff = find_ffmpeg()
    if not ff:
        raise RuntimeError(
            "ffmpeg를 찾을 수 없습니다. 터미널에서 'brew install ffmpeg' 실행 후 앱을 재시작하세요.")
    try:
        # 주의: 옵션명은 -list_devices (언더스코어). 하이픈이면 ffmpeg가 거부한다.
        pr = subprocess.run([ff, "-hide_banner", "-f", "avfoundation",
                             "-list_devices", "true", "-i", ""],
                            capture_output=True, text=True, timeout=15)
    except subprocess.TimeoutExpired:
        raise RuntimeError("ffmpeg 장치 조회가 응답하지 않습니다. ffmpeg를 재설치해 보세요.")
    devices, in_audio = [], False
    for line in pr.stderr.splitlines():
        if "AVFoundation audio devices" in line:
            in_audio = True
            continue
        if "AVFoundation video devices" in line:
            in_audio = False
            continue
        m = re.search(r"\[(\d+)\]\s+(.*)$", line)
        if in_audio and m:
            devices.append({"index": m.group(1), "name": m.group(2).strip()})
    if not devices:
        tail = " | ".join(l.strip() for l in pr.stderr.strip().splitlines()[-3:])
        raise RuntimeError(
            "오디오 입력 장치를 찾지 못했습니다. "
            "① 시스템 설정 > 개인정보 보호 및 보안 > 마이크에서 터미널 허용 "
            "② 앱 재시작 후 ↻ 새로고침. "
            f"[ffmpeg 응답: {tail}]")
    return devices
