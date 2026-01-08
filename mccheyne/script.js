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
                            const chapter = parseInt(keyParts.at(-1), 10);
                            const shortKey = `${book}_${chapter}`;
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
    function openTextModal(button) {
        modalTitle.innerText = button.dataset.title;
        modalIframe.src = button.dataset.path;
        modalOverlay.classList.add('visible');

        // 모바일에서 스크롤 문제 방지를 위한 개선된 방법
        if (window.innerWidth <= 768) {
            // 모바일에서는 body만 고정하고 position 조정
            document.body.style.position = 'fixed';
            document.body.style.top = `-${window.scrollY}px`;
            document.body.style.width = '100%';
        } else {
            // 데스크톱에서는 기존 방식 유지
            document.documentElement.style.overflow = 'hidden';
        }

        // iframe 로딩 완료 후 처리
        modalIframe.onload = () => {
            try {
                const doc = modalIframe.contentDocument || modalIframe.contentWindow.document;

                // 1. 중복 타이틀 숨기기
                const h1 = doc.querySelector('h1');
                if (h1) h1.style.display = 'none';

                // 2. 폰트 사이즈 적용 (부모 창에서 currentFontSize 가져오기)
                if (window.parent && window.parent.currentFontSize) {
                    const fontSize = 16 * (window.parent.currentFontSize / 100);
                    doc.documentElement.style.fontSize = fontSize + 'px';
                    doc.body.style.fontSize = fontSize + 'px';
                } else if (window.parent && typeof window.parent.applyFontSize === 'function') {
                    // Fallback: 부모 창의 함수 호출
                    window.parent.applyFontSize();
                }
            } catch (e) {
                console.warn('Cannot access iframe content:', e);
            }

            if (window.innerWidth <= 768) {
                modalIframe.style.pointerEvents = 'auto';
                modalIframe.style.touchAction = 'auto';
            }
        };
    }

    function closeModal() {
        modalOverlay.classList.remove('visible');

        // 모바일에서 스크롤 위치 복원
        if (window.innerWidth <= 768) {
            const scrollY = document.body.style.top;
            document.body.style.position = '';
            document.body.style.top = '';
            document.body.style.width = '';
            window.scrollTo(0, parseInt(scrollY || '0') * -1);
        } else {
            document.documentElement.style.overflow = '';
        }

        // iframe 초기화
        modalIframe.onload = null;
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

    function playAudio(button) {
        if (!isPlayerReady) { alert('오디오 플레이어가 아직 준비되지 않았습니다.'); return; }

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
