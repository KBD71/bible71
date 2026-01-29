document.addEventListener('DOMContentLoaded', () => {
    // --- 전역 변수 및 객체 ---
    let ytPlayer, isPlayerReady = false;
    const audioKeyMap = new Map();
    let currentTabIndex = 0;
    let playlist = [];
    let currentPlayIndex = 0;

    // --- DOM 요소 캐싱 ---
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const floatingNav = document.getElementById('floating-nav');
    const prevTabBtn = document.getElementById('prev-tab');
    const nextTabBtn = document.getElementById('next-tab');
    const currentTabInfo = document.getElementById('current-tab-info');
    const progressBar = document.getElementById('reading-progress');

    const modalOverlay = document.getElementById('text-modal');
    const modalCloseBtn = document.getElementById('modal-close');
    const modalTitle = document.getElementById('modal-title');
    const modalIframe = document.getElementById('modal-iframe');

    const audioPlayerBar = document.getElementById('audio-player');
    const playerInfo = document.getElementById('player-info');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const closePlayerBtn = document.getElementById('close-player-btn');

    // --- 초기화 ---
    function init() {
        initYouTubeAPI();
        loadAudioKeys();
        setupEventListeners();
        loadCompletionStatus();
        updateFloatingNav();
        updateReadingProgress();
    }

    // --- YouTube API 관련 ---
    function initYouTubeAPI() {
        const tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        document.head.appendChild(tag);
        window.onYouTubeIframeAPIReady = () => {
            ytPlayer = new YT.Player('player-container', {
                height: '0', width: '0',
                playerVars: { 'autoplay': 0, 'controls': 0, 'rel': 0, 'fs': 0 },
                events: {
                    'onReady': (event) => {
                        isPlayerReady = true;
                        // Expose player to window for global control from index.html
                        window.player = ytPlayer;
                    },
                    'onStateChange': onPlayerStateChange
                }
            });
        };
    }


    // --- 부모 창 플레이어 제목 업데이트 함수 ---
    function updateParentPlayerTitle(title) {
        try {
            // iframe에서 실행 중인지 확인하고 부모 창의 playerTitle 업데이트
            if (window.parent && window.parent !== window) {
                const parentPlayerTitle = window.parent.document.getElementById('player-title');
                if (parentPlayerTitle) {
                    parentPlayerTitle.textContent = title;
                    console.log('Parent player title updated:', title);
                }
            }
        } catch (e) {
            // Cross-origin 이슈 등으로 접근 불가능한 경우 무시
            console.warn('Cannot update parent player title:', e);
        }
    }

    // --- 데이터 로딩 및 파싱 ---
    // mcbible.txt와 HTML 파일 간의 책 코드 불일치를 해결하기 위한 매핑
    // mcbible.txt (오디오 소스) → bible_html (본문 파일) 형식으로 변환
    const bookCodeMapping = {
        "MRK": "MAR",  // 마가복음: mcbible.txt는 MRK, bible_html은 MAR 사용
        "JHN": "JOH",  // 요한복음: mcbible.txt는 JHN, bible_html은 JOH 사용
        "PHP": "PHI",  // 빌립보서: mcbible.txt는 PHP, bible_html은 PHI 사용
        "JAS": "JAM"   // 야고보서: mcbible.txt는 JAS, bible_html은 JAM 사용
    };

    async function loadAudioKeys() {
        try {
            const response = await fetch('https://kbd71.github.io/bible71/address/mcbible.txt');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const text = await response.text();
            text.split('\n').forEach(line => {
                if (line.trim()) {
                    const parts = line.trim().split(/\s+/);
                    const longKey = parts[0];
                    const url = parts[1];
                    if (longKey && url) {
                        const keyParts = longKey.split('_');
                        if (keyParts.length >= 3) {
                            const book = keyParts[2];
                            // 책 코드 매핑 적용 (MRK → MAR 등)
                            const mappedBook = bookCodeMapping[book] || book;
                            const chapter = parseInt(keyParts.at(-1), 10);
                            const shortKey = `${mappedBook}_${chapter}`;
                            audioKeyMap.set(shortKey, url);
                        }
                    }
                }
            });
        } catch (error) {
            console.error("mcbible.txt 로드 실패:", error);
        }
    }

    function getYouTubeID(url) {
        const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
        const match = url.match(regex);
        return match ? match[1] : null;
    }

    // --- 이벤트 리스너 설정 ---
    function setupEventListeners() {
        tabButtons.forEach((button, index) => button.addEventListener('click', () => switchTab(index)));
        document.querySelectorAll('.view-text-btn').forEach(button => button.addEventListener('click', () => openTextModal(button)));
        document.querySelectorAll('.listen-audio-btn').forEach(button => button.addEventListener('click', () => playAudio(button)));

        modalCloseBtn.addEventListener('click', closeModal);
        modalOverlay.addEventListener('click', (e) => { if (e.target === modalOverlay) closeModal(); });

        playPauseBtn.addEventListener('click', togglePlayPause);
        closePlayerBtn.addEventListener('click', closeAudioPlayer);

        prevTabBtn.addEventListener('click', () => switchTab(currentTabIndex - 1));
        nextTabBtn.addEventListener('click', () => switchTab(currentTabIndex + 1));

        let lastScrollY = window.scrollY;
        window.addEventListener('scroll', () => {
            updateReadingProgress();
            checkReadingCompletion();
            const currentScrollY = window.scrollY;
            if (currentScrollY > lastScrollY && currentScrollY > 100) {
                if (!audioPlayerBar.classList.contains('visible')) floatingNav.classList.add('hidden');
            } else {
                floatingNav.classList.remove('hidden');
            }
            lastScrollY = currentScrollY < 0 ? 0 : currentScrollY;
        }, { passive: true });
        window.addEventListener('resize', updateReadingProgress);
    }

    // --- 기능별 함수 ---
    // 스크롤 위치 저장 변수
    let savedScrollY = 0;

    function openTextModal(button) {
        const paths = button.dataset.path.split(',').map(p => p.trim());
        const title = button.dataset.title;

        modalTitle.innerText = title;
        modalOverlay.classList.add('visible');

        // 이전 콘텐츠 초기화 (srcdoc가 src보다 우선순위가 높으므로 반드시 제거)
        modalIframe.removeAttribute('srcdoc');

        // 현재 스크롤 위치 저장
        savedScrollY = window.scrollY;

        // 배경 스크롤 방지 (모바일/데스크톱 공통)
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed';
        document.body.style.top = `-${savedScrollY}px`;
        document.body.style.left = '0';
        document.body.style.right = '0';

        // 단일 경로이면서 부분 절 지정이 없는 경우: 기존 iframe 방식
        if (paths.length === 1 && !paths[0].includes('#')) {
            modalIframe.src = paths[0];
            modalIframe.style.display = 'block';

            modalIframe.onload = () => {
                applyIframeStyles(modalIframe);
            };
        }
        // 다중 경로 또는 부분 절 지정이 있는 경우: fetch로 콘텐츠 합치기
        else {
            loadAndMergeContent(paths);
        }
    }

    // iframe 스타일 적용 헬퍼 함수
    function applyIframeStyles(iframe) {
        try {
            const doc = iframe.contentDocument || iframe.contentWindow.document;

            // 1. 중복 타이틀 숨기기
            const h1 = doc.querySelector('h1');
            if (h1) h1.style.display = 'none';

            // 2. 폰트 사이즈 적용
            if (window.parent && window.parent.currentFontSize) {
                const fontSize = 16 * (window.parent.currentFontSize / 100);
                doc.documentElement.style.fontSize = fontSize + 'px';
                doc.body.style.fontSize = fontSize + 'px';
            }

            // 3. iframe 내부 body 스크롤 강제 활성화
            doc.body.style.overflow = 'auto';
            doc.body.style.overflowY = 'scroll';
            doc.body.style.webkitOverflowScrolling = 'touch';
        } catch (e) {
            console.warn('Cannot access iframe content:', e);
        }

        iframe.style.pointerEvents = 'auto';
        iframe.style.touchAction = 'pan-y';
        iframe.style.overflowY = 'auto';
        iframe.style.webkitOverflowScrolling = 'touch';
    }

    // 다중 URL의 콘텐츠를 가져와 합치는 함수
    async function loadAndMergeContent(paths) {
        try {
            const contentPromises = paths.map(async (pathWithHash) => {
                // URL과 절 범위 분리 (예: url#1-15)
                const [url, verseRange] = pathWithHash.split('#');

                const response = await fetch(url);
                if (!response.ok) throw new Error(`Failed to fetch: ${url}`);
                const html = await response.text();

                // HTML 파싱
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const bibleContent = doc.querySelector('.bible-content');
                const chapterTitle = doc.querySelector('h1');

                if (!bibleContent) return '';

                // 부분 절 필터링
                if (verseRange) {
                    const [startVerse, endVerse] = verseRange.split('-').map(Number);
                    const paragraphs = bibleContent.querySelectorAll('p');

                    paragraphs.forEach(p => {
                        const verseSpan = p.querySelector('.verse-number');
                        if (verseSpan) {
                            const verseNum = parseInt(verseSpan.textContent, 10);
                            if (verseNum < startVerse || verseNum > endVerse) {
                                p.style.display = 'none';
                            }
                        }
                    });

                    // 범위 밖의 소제목도 숨기기
                    const subtitles = bibleContent.querySelectorAll('.subtitle');
                    subtitles.forEach(subtitle => {
                        const nextP = subtitle.nextElementSibling;
                        if (nextP && nextP.style.display === 'none') {
                            subtitle.style.display = 'none';
                        }
                    });
                }

                // 장 제목 추가 (여러 장을 합칠 때 구분용)
                let result = '';
                if (chapterTitle && paths.length > 1) {
                    result += `<div class="chapter-divider" style="font-size: 1.5em; font-weight: 600; color: #343a40; border-bottom: 2px solid #dee2e6; padding: 1rem 0; margin: 2rem 0 1rem 0;">${chapterTitle.textContent}</div>`;
                }
                result += bibleContent.innerHTML;

                return result;
            });

            const contents = await Promise.all(contentPromises);
            const mergedContent = contents.join('');

            // 폰트 사이즈 계산
            let fontSize = '1.15em';
            if (window.parent && window.parent.currentFontSize) {
                fontSize = (16 * (window.parent.currentFontSize / 100)) + 'px';
            }

            // 합친 콘텐츠를 iframe에 동적으로 삽입
            const fullHtml = `
                <!DOCTYPE html>
                <html lang="ko">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600&display=swap');
                        body {
                            font-family: 'Noto Serif KR', serif;
                            line-height: 2;
                            background-color: #f8f9fa;
                            color: #212529;
                            margin: 0;
                            padding: 2.5rem;
                            font-size: ${fontSize};
                            overflow-y: scroll;
                            -webkit-overflow-scrolling: touch;
                        }
                        .container { max-width: 800px; margin: 0 auto; }
                        .bible-content p { font-size: 1.15em; margin-top: 0; margin-bottom: 0.5rem; }
                        .verse-number { font-size: 0.7em; font-weight: 600; color: #868e96; vertical-align: super; margin-right: 0.5em; }
                        .subtitle { font-size: 1.1em; font-weight: 600; color: #dc3545; margin: 1.5rem 0 0.8rem 0; padding: 0.3rem 0; border-left: 4px solid #dc3545; padding-left: 1rem; background-color: #f8f9fa; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="bible-content">${mergedContent}</div>
                    </div>
                </body>
                </html>
            `;

            // iframe에 동적 콘텐츠 로드
            modalIframe.style.display = 'block';
            modalIframe.srcdoc = fullHtml;

            modalIframe.onload = () => {
                modalIframe.style.pointerEvents = 'auto';
                modalIframe.style.touchAction = 'pan-y';
                modalIframe.style.overflowY = 'auto';
                modalIframe.style.webkitOverflowScrolling = 'touch';
            };

        } catch (error) {
            console.error('콘텐츠 로드 실패:', error);
            modalIframe.srcdoc = `<html><body style="padding: 2rem; font-family: sans-serif;"><h2>콘텐츠를 불러올 수 없습니다.</h2><p>${error.message}</p></body></html>`;
        }
    }

    function closeModal() {
        modalOverlay.classList.remove('visible');

        // 배경 스크롤 복원
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.left = '';
        document.body.style.right = '';

        // 스크롤 위치 복원
        window.scrollTo(0, savedScrollY);

        // iframe 초기화 (srcdoc가 src보다 우선순위가 높으므로 반드시 함께 초기화해야 함)
        modalIframe.onload = null;
        modalIframe.removeAttribute('srcdoc');  // srcdoc 속성 제거 (중요!)
        modalIframe.src = 'about:blank';
        setTimeout(() => modalIframe.src = '', 100);
    }

    function switchTab(index) {
        if (index < 0 || index >= tabButtons.length) return;
        currentTabIndex = index;
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => { content.classList.remove('active'); });
        tabButtons[index].classList.add('active');
        tabContents[index].classList.add('active');
        window.scrollTo({ top: 0, behavior: 'auto' });
        updateFloatingNav();
        setTimeout(updateReadingProgress, 150);

        // 오디오 플레이어가 활성화된 상태라면 탭 이동 시 해당 탭의 오디오로 자동 전환
        if (audioPlayerBar.classList.contains('visible')) {
            const activeContent = tabContents[index];
            const audioBtn = activeContent.querySelector('.listen-audio-btn');
            if (audioBtn) {
                playAudio(audioBtn);
            }
        }
    }

    function playAudio(button, retryCount = 0) {
        const MAX_RETRIES = 10;

        // 버튼에 로딩 상태 표시
        if (retryCount === 0) {
            button.classList.add('loading');
            button.disabled = true;
            button.dataset.originalText = button.textContent;
            button.textContent = '로딩 중...';
        }

        // 로딩 상태 해제 함수
        const clearLoading = () => {
            button.classList.remove('loading');
            button.disabled = false;
            if (button.dataset.originalText) {
                button.textContent = button.dataset.originalText;
            }
        };

        // Wait for player to be ready
        if (!isPlayerReady) {
            if (retryCount < MAX_RETRIES) {
                console.log(`Player not ready, waiting... (attempt ${retryCount + 1}/${MAX_RETRIES})`);
                setTimeout(() => playAudio(button, retryCount + 1), 500);
                return;
            } else {
                clearLoading();
                alert('오디오 플레이어가 준비되지 않았습니다. 페이지를 새로고침해주세요.');
                return;
            }
        }

        // Wait for audio keys to be loaded
        if (audioKeyMap.size === 0) {
            if (retryCount < MAX_RETRIES) {
                console.log(`Audio keys not loaded, waiting... (attempt ${retryCount + 1}/${MAX_RETRIES})`);
                setTimeout(() => playAudio(button, retryCount + 1), 500);
                return;
            } else {
                clearLoading();
                alert('오디오 정보를 불러오지 못했습니다. 페이지를 새로고침해주세요.');
                return;
            }
        }

        // 로딩 완료, 상태 해제
        clearLoading();

        const key = button.dataset.key; // e.g., "GEN_9_10" or "GEN_9"
        const title = button.dataset.title;

        // 1. 키 파싱 및 재생 목록 생성
        playlist = [];
        currentPlayIndex = 0;

        const parts = key.split('_');

        // Case A: Composite Key (e.g., GEN_9_10) - Existing Logic
        // Check if key has more than 2 parts (BOOK_CH1_CH2...) OR if it explicitly has multiple chapters
        if (parts.length > 2) {
            const bookCode = parts[0]; // 'GEN'
            const chapters = parts.slice(1);

            chapters.forEach(chapterStr => {
                const singleChapterKey = `${bookCode}_${chapterStr}`;
                const url = audioKeyMap.get(singleChapterKey);

                if (url) {
                    const videoId = getYouTubeID(url);
                    if (videoId) {
                        playlist.push({
                            videoId: videoId,
                            title: `${title} (${chapterStr}장)`
                        });
                    }
                } else {
                    console.warn(`오디오 정보를 찾을 수 없음: ${singleChapterKey}`);
                }
            });
        }
        // Case B: Single Key (e.g., GEN_9) - New Logic for Separate Buttons
        else {
            // Check for sibling buttons in the same card
            const cardContent = button.closest('.card-content');
            if (cardContent) {
                const siblingBtns = Array.from(cardContent.querySelectorAll('.listen-audio-btn'));

                if (siblingBtns.length > 1) {
                    // Build playlist from all siblings
                    siblingBtns.forEach((btn, index) => {
                        const siblingKey = btn.dataset.key;
                        const siblingTitle = btn.dataset.title;

                        // Parse key to get chapter number for title (assuming BOOK_CHAPTER format)
                        const siblingParts = siblingKey.split('_');
                        const chapterStr = siblingParts.length >= 2 ? siblingParts[1] : '';

                        const url = audioKeyMap.get(siblingKey);
                        if (url) {
                            const videoId = getYouTubeID(url);
                            if (videoId) {
                                playlist.push({
                                    videoId: videoId,
                                    title: siblingTitle
                                });
                            }
                        }

                        // If this is the clicked button, set start index
                        if (btn === button) {
                            currentPlayIndex = playlist.length - 1;
                        }
                    });
                }
            }

            // If playlist is still empty (no siblings or single button), add the clicked button
            if (playlist.length === 0) {
                const url = audioKeyMap.get(key);
                if (url) {
                    const videoId = getYouTubeID(url);
                    if (videoId) {
                        playlist.push({
                            videoId: videoId,
                            title: title
                        });
                    }
                }
            }
        }

        if (playlist.length > 0) {
            // 플레이어 UI 표시
            floatingNav.classList.add('hidden');
            audioPlayerBar.classList.add('visible');

            // 첫 번째 영상 재생 (또는 클릭한 버튼에 해당하는 영상)
            playNextVideo();
        } else {
            alert('재생할 오디오 정보를 찾을 수 없습니다. (Key: ' + key + ')');
        }
    }

    function playNextVideo() {
        if (currentPlayIndex < playlist.length) {
            const item = playlist[currentPlayIndex];
            // 큐에 넣고 바로 재생
            ytPlayer.loadVideoById(item.videoId);
            // loadVideoById는 자동으로 재생됨. cueVideoById는 대기만 함.
            // 연속 재생을 위해서는 loadVideoById가 적절함.

            // 전체 타이틀 표시 (현재 몇 번째인지 표시해주는 것도 좋음)
            // playerInfo.textContent = `재생 중: ${item.title}`; 
            // 원래 타이틀 유지를 원하면 아래와 같이:
            // playerInfo.textContent = `재생 중: ${document.querySelector('.listen-audio-btn[data-key="'+ ... +'"]').dataset.title}`;
            // 하지만 여기서는 간단히:
            const displayTitle = `${item.title} (${currentPlayIndex + 1}/${playlist.length})`;
            playerInfo.textContent = displayTitle;

            // 부모 창의 플레이어 제목 업데이트
            updateParentPlayerTitle(item.title);

            currentPlayIndex++;
        } else {
            // 재생 목록 끝
            closeAudioPlayer();
        }
    }

    function togglePlayPause() {
        if (!ytPlayer || typeof ytPlayer.getPlayerState !== 'function') return;
        const playerState = ytPlayer.getPlayerState();
        if (playerState === YT.PlayerState.PLAYING) {
            ytPlayer.pauseVideo();
        } else {
            ytPlayer.playVideo();
        }
    }

    function onPlayerStateChange(event) {
        playPauseBtn.innerHTML = (event.data === YT.PlayerState.PLAYING) ? '❚❚' : '▶';

        if (event.data === YT.PlayerState.ENDED) {
            playNextVideo();
        }
    }

    function closeAudioPlayer() {
        if (ytPlayer && typeof ytPlayer.stopVideo === 'function') ytPlayer.stopVideo();
        audioPlayerBar.classList.remove('visible');
        floatingNav.classList.remove('hidden');
    }

    function updateFloatingNav() {
        if (!currentTabInfo) return;
        currentTabInfo.textContent = `${currentTabIndex + 1}/${tabButtons.length}`;
        prevTabBtn.disabled = currentTabIndex === 0;
        nextTabBtn.disabled = currentTabIndex === tabButtons.length - 1;
    }

    function updateReadingProgress() {
        const activeContent = document.querySelector('.tab-content.active');
        if (!activeContent) return;
        const scrollableHeight = activeContent.scrollHeight - window.innerHeight;
        const progress = scrollableHeight > 0 ? (window.scrollY / scrollableHeight) * 100 : 0;
        progressBar.style.width = Math.min(100, progress) + '%';
    }

    function checkReadingCompletion() {
        if (parseFloat(progressBar.style.width) >= 95) {
            const currentTab = tabButtons[currentTabIndex];
            if (currentTab && !currentTab.classList.contains('completed')) {
                currentTab.classList.add('completed');
                saveCompletionStatus();
            }
        }
    }

    function saveCompletionStatus() {
        const dateKey = document.querySelector('h1').textContent;
        const completed = Array.from(tabButtons).map((tab, index) => tab.classList.contains('completed') ? index : -1).filter(i => i !== -1);
        localStorage.setItem(`completed_${dateKey}`, JSON.stringify(completed));
    }

    function loadCompletionStatus() {
        const dateKey = document.querySelector('h1').textContent;
        const completed = JSON.parse(localStorage.getItem(`completed_${dateKey}`) || '[]');
        completed.forEach(index => {
            if (tabButtons[index]) tabButtons[index].classList.add('completed');
        });
    }

    init();
});
