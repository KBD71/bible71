document.addEventListener('DOMContentLoaded', () => {
    // --- 전역 변수 및 객체 ---
    let ytPlayer, isPlayerReady = false;
    const audioKeyMap = new Map();
    let currentTabIndex = 0;

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

                // 2. 폰트 사이즈 적용 (부모 창의 함수 호출)
                if (window.parent && typeof window.parent.applyFontSize === 'function') {
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
        const key = button.dataset.key;
        const title = button.dataset.title;
        const url = audioKeyMap.get(key);
        if (url) {
            const videoId = getYouTubeID(url);
            if (videoId) {
                ytPlayer.loadVideoById(videoId);
                playerInfo.textContent = `재생 중: ${title}`;
                floatingNav.classList.add('hidden');
                audioPlayerBar.classList.add('visible');
            } else { alert('유효한 YouTube 주소가 아닙니다.'); }
        } else { alert('오디오 정보를 찾을 수 없습니다. (Key: ' + key + ')'); }
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
