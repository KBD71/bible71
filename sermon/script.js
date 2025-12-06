// sermon/script.js

// Global variables
var player;
var videoId = null;
var isPlayerReady = false;

// DOM Elements (Sermon Page Specific)
const listenBtn = document.getElementById('play-btn');
const buttonText = document.getElementById('btn-text');
const iconSpan = document.getElementById('btn-icon');

// 1. Find Video ID from HTML Comment
function findVideoIdFromComment() {
    const iterator = document.createNodeIterator(
        document.documentElement,
        NodeFilter.SHOW_COMMENT,
        null
    );

    let currentNode;
    while (currentNode = iterator.nextNode()) {
        const commentContent = currentNode.nodeValue.trim();

        // Look for YouTube URL in comment with specific prefix "링크 :"
        // Format: <!-- 링크 : https://youtu.be/... -->
        const linkMatch = commentContent.match(/링크\s*:\s*(https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)[a-zA-Z0-9_-]{11})/);

        if (linkMatch) {
            const url = linkMatch[1];
            videoId = getYouTubeID(url);
            console.log(`Found video ID from comment: ${videoId}`);
            initYouTubeAPI();
            return;
        }

        // Fallback: Try to find just the URL if "링크 :" is missing
        const urlMatch = commentContent.match(/^(https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)[a-zA-Z0-9_-]{11})$/);
        if (urlMatch) {
            videoId = getYouTubeID(urlMatch[1]);
            console.log(`Found video ID from comment (direct URL): ${videoId}`);
            initYouTubeAPI();
            return;
        }
    }

    console.warn("No YouTube video link found in comments.");
    updateButtonState('unavailable', '오디오 없음');
}

// Helper: Extract ID from URL
function getYouTubeID(url) {
    const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
}

// 2. Initialize YouTube API
function initYouTubeAPI() {
    if (window.YT && window.YT.Player) {
        createPlayer();
    } else {
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }
}

// Called by YouTube API
function onYouTubeIframeAPIReady() {
    createPlayer();
}

function createPlayer() {
    if (isPlayerReady) return;

    player = new YT.Player('hidden-player-container', {
        height: '1',
        width: '1',
        videoId: videoId,
        playerVars: {
            'playsinline': 1
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

// 3. Event Handlers
function onPlayerReady(event) {
    isPlayerReady = true;
    updateButtonState('ready', '설교 듣기');
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        updateButtonState('playing', '일시정지');
    } else if (event.data == YT.PlayerState.PAUSED || event.data == YT.PlayerState.ENDED) {
        updateButtonState('ready', '다시 듣기');
    } else if (event.data == YT.PlayerState.BUFFERING) {
        updateButtonState('loading', '로딩 중...');
    }
}

function togglePlay() {
    if (!player || !isPlayerReady) return;

    if (player.getPlayerState() == YT.PlayerState.PLAYING) {
        player.pauseVideo();
    } else {
        player.playVideo();
    }
}

// UI State Manager (Sermon Page Specific)
function updateButtonState(state, text) {
    if (!listenBtn) return;

    if (buttonText) buttonText.innerText = text;

    switch (state) {
        case 'loading':
            listenBtn.disabled = true;
            if (iconSpan) iconSpan.innerText = '...';
            break;
        case 'ready':
            listenBtn.disabled = false;
            if (iconSpan) iconSpan.innerText = '▶';
            break;
        case 'playing':
            listenBtn.disabled = false;
            if (iconSpan) iconSpan.innerText = '❚❚';
            break;
        case 'unavailable':
            listenBtn.disabled = true;
            if (iconSpan) iconSpan.innerText = 'X';
            break;
        case 'error':
            listenBtn.disabled = true;
            if (iconSpan) iconSpan.innerText = '!';
            break;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (listenBtn) {
        listenBtn.addEventListener('click', togglePlay);
        findVideoIdFromComment();
    }
});
