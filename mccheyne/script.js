document.addEventListener('DOMContentLoaded', () => {
    // --- 전역 변수 및 객체 ---
    const audioKeyMap = new Map();
    let ytPlayer, isPlayerReady = false;

    // --- DOM 요소 캐싱 ---
    const tabs = {
        buttons: document.querySelectorAll('.tab-btn'),
        contents: document.querySelectorAll('.tab-content'),
        currentIndex: 0
    };
    const nav = {
        container: document.getElementById('floating-nav'),
        prevBtn: document.getElementById('prev-tab'),
        nextBtn: document.getElementById('next-tab'),
        info: document.getElementById('current-tab-info')
    };
    const progressBar = document.getElementById('reading-progress');
    const modal = {
        overlay: document.getElementById('text-modal'),
        closeBtn: document.getElementById('modal-close'),
        title: document.getElementById('modal-title'),
        iframe: document.getElementById('modal-iframe')
    };
    const audioPlayer = {
        container: document.getElementById('audio-player'),
        info: document.getElementById('player-info'),
        playPauseBtn: document.getElementById('play-pause-btn'),
        closeBtn: document.getElementById('close-player-btn')
    };

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
                playerVars: { 'autoplay': 1, 'controls': 0, 'rel': 0, 'fs': 0 },
                events: {
                    'onReady': () => { isPlayerReady = true; },
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
                            const chapter = parseInt(keyParts.at(-1), 10); // 숫자로 변환
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
        tabs.buttons.forEach((button, index) => button.addEventListener('click', () => switchTab(index)));
        document.querySelectorAll('.view-text-btn').forEach(button => button.addEventListener('click', () => openTextModal(button)));
        document.querySelectorAll('.listen-audio-btn').forEach(button => button.addEventListener('click', () => playAudio(button)));
        modal.closeBtn.addEventListener('click', () => modal.overlay.classList.remove('visible'));
        modal.overlay.addEventListener('click', (e) => { if (e.target === modal.overlay) modal.overlay.classList.remove('visible'); });
        
        audioPlayer.playPauseBtn.addEventListener('click', togglePlayPause);
        audioPlayer.closeBtn.addEventListener('click', closeAudioPlayer);

        nav.prevBtn.addEventListener('click', () => switchTab(tabs.currentIndex - 1));
        nav.nextBtn.addEventListener('click', () => switchTab(tabs.currentIndex + 1));
        
        let lastScrollY = window.scrollY;
        window.addEventListener('scroll', () => {
            updateReadingProgress();
            checkReadingCompletion();
            const currentScrollY = window.scrollY;
            if (currentScrollY > lastScrollY && currentScrollY > 100) {
                if (!audioPlayer.container.classList.contains('visible')) nav.container.classList.add('hidden');
            } else {
                nav.container.classList.remove('hidden');
            }
            lastScrollY = currentScrollY < 0 ? 0 : currentScrollY;
        }, { passive: true });
        window.addEventListener('resize', updateReadingProgress);
    }

    // --- 기능별 함수 ---
    function switchTab(index) {
        if (index < 0 || index >= tabs.buttons.length) return;
        tabs.currentIndex = index;
        tabs.buttons.forEach(btn => btn.classList.remove('active'));
        tabs.contents.forEach(content => { content.classList.remove('active'); });
        tabs.buttons[index].classList.add('active');
        tabs.contents[index].classList.add('active');
        window.scrollTo({ top: 0, behavior: 'auto' });
        updateFloatingNav();
        setTimeout(updateReadingProgress, 150);
    }

    function openTextModal(button) {
        modal.title.innerText = button.dataset.title;
        modal.iframe.src = button.dataset.path;
        modal.overlay.classList.add('visible');
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
                audioPlayer.info.textContent = `재생 중: ${title}`;
                nav.container.classList.add('hidden');
                audioPlayer.container.classList.add('visible');
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
        audioPlayer.playPauseBtn.innerHTML = (event.data === YT.PlayerState.PLAYING) ? '❚❚' : '▶';
    }

    function closeAudioPlayer() {
        if (ytPlayer && typeof ytPlayer.stopVideo === 'function') ytPlayer.stopVideo();
        audioPlayer.container.classList.remove('visible');
        nav.container.classList.remove('hidden');
    }

    function updateFloatingNav() {
        if (!nav.info) return;
        nav.info.textContent = `${tabs.currentIndex + 1}/${tabs.buttons.length}`;
        nav.prevBtn.disabled = tabs.currentIndex === 0;
        nav.nextBtn.disabled = tabs.currentIndex === tabs.buttons.length - 1;
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
            const currentTab = tabs.buttons[tabs.currentIndex];
            if (currentTab && !currentTab.classList.contains('completed')) {
                currentTab.classList.add('completed');
                saveCompletionStatus();
            }
        }
    }

    function saveCompletionStatus() {
        const dateKey = document.querySelector('h1').textContent;
        const completed = Array.from(tabs.buttons).map((tab, index) => tab.classList.contains('completed') ? index : -1).filter(i => i !== -1);
        localStorage.setItem(`completed_${dateKey}`, JSON.stringify(completed));
    }

    function loadCompletionStatus() {
        const dateKey = document.querySelector('h1').textContent;
        const completed = JSON.parse(localStorage.getItem(`completed_${dateKey}`) || '[]');
        completed.forEach(index => {
            if (tabs.buttons[index]) tabs.buttons[index].classList.add('completed');
        });
    }

    init();
});
