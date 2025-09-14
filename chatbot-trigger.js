// iframe 페이지용 챗봇 트리거 스크립트
// 메인페이지의 챗봇과 통신하여 챗봇 기능을 사용할 수 있게 함

(function() {
    // iframe 내부에서 실행되는지 확인
    if (window.self === window.top) {
        // 메인페이지에서는 실행하지 않음
        return;
    }

    // 챗봇 트리거 버튼 스타일
    const style = document.createElement('style');
    style.textContent = `
        .chatbot-trigger-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: #8B0000;
            border-radius: 50%;
            border: 2px solid #DAA520;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .chatbot-trigger-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 25px rgba(0,0,0,0.4);
        }
        .chatbot-trigger-btn svg {
            width: 28px;
            height: 28px;
            color: #F5EFE6;
        }
        @media (max-width: 768px) {
            .chatbot-trigger-btn {
                bottom: 15px;
                right: 15px;
                width: 55px;
                height: 55px;
            }
        }

        /* 간단한 알림 팝업 스타일 */
        .chatbot-info-popup {
            position: fixed;
            bottom: 90px;
            right: 20px;
            background: white;
            border: 2px solid #DAA520;
            border-radius: 15px;
            padding: 12px 16px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            z-index: 10000;
            max-width: 280px;
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 14px;
            color: #4E342E;
            display: none;
        }
        .chatbot-info-popup::after {
            content: '';
            position: absolute;
            top: 100%;
            right: 30px;
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-top: 8px solid #DAA520;
        }
    `;
    document.head.appendChild(style);

    // 챗봇 트리거 버튼 HTML
    const triggerHTML = `
        <button class="chatbot-trigger-btn" id="chatbot-trigger-iframe">
            <!-- 존 칼빈 옆모습 실루엣 아이콘 -->
            <svg viewBox="0 0 100 100" fill="currentColor">
                <!-- 칼빈의 특징적인 베레모 -->
                <path d="M25 20c0-8 8-15 20-15s20 7 20 15c0 3-2 6-5 8 3 2 5 5 5 8 0 2-1 4-3 5-2 3-8 5-12 5s-10-2-12-5c-2-1-3-3-3-5 0-3 2-6 5-8-3-2-5-5-5-8z"/>

                <!-- 얼굴 윤곽 (옆모습) -->
                <path d="M45 25c8 0 12 2 15 5v25c0 8-7 15-15 15s-15-7-15-15V30c3-3 7-5 15-5z"/>

                <!-- 특징적인 긴 코 -->
                <path d="M60 40c2 0 4 1 4 3s-2 3-4 3-2-1-2-3 0-3 2-3z"/>

                <!-- 수염 -->
                <path d="M45 50c5 0 8 2 10 5v8c0 5-4 8-10 8s-10-3-10-8v-8c2-3 5-5 10-5z"/>

                <!-- 베레모의 접힌 부분 -->
                <path d="M35 22c-2-1-3-3-2-5s3-2 5-1 8 3 12 3 10-2 12-3c2-1 4-1 5 1s0 4-2 5c-3 2-8 4-15 4s-12-2-15-4z"/>

                <!-- 성경을 들고 있는 모습 -->
                <rect x="25" y="65" width="12" height="8" rx="2" fill="currentColor"/>
                <rect x="24" y="63" width="14" height="2" rx="1" fill="currentColor"/>
                <line x1="28" y1="67" x2="33" y2="67" stroke="#F5EFE6" stroke-width="0.5"/>
                <line x1="28" y1="69" x2="35" y2="69" stroke="#F5EFE6" stroke-width="0.5"/>
            </svg>
        </button>
        <div class="chatbot-info-popup" id="chatbot-info-popup">
            성경 도우미 챗봇을 사용하려면 이 버튼을 클릭하세요! 🙏
        </div>
    `;

    // DOM에 추가
    document.body.insertAdjacentHTML('beforeend', triggerHTML);

    // 기능 구현
    const triggerBtn = document.getElementById('chatbot-trigger-iframe');
    const infoPopup = document.getElementById('chatbot-info-popup');

    // 메인 페이지의 챗봇 열기
    triggerBtn.addEventListener('click', () => {
        // 부모 창(메인페이지)에 메시지 전송
        window.parent.postMessage({
            type: 'OPEN_CHATBOT'
        }, window.location.origin);

        // 정보 팝업 숨기기
        infoPopup.style.display = 'none';
    });

    // 페이지 로드 후 잠깐 정보 팝업 표시
    setTimeout(() => {
        infoPopup.style.display = 'block';
        setTimeout(() => {
            infoPopup.style.display = 'none';
        }, 4000);
    }, 2000);

    // 키보드 단축키 (Ctrl + / 또는 Cmd + /)로 챗봇 열기
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            window.parent.postMessage({
                type: 'OPEN_CHATBOT'
            }, window.location.origin);
        }
    });

    console.log('챗봇 트리거가 활성화되었습니다. 우측 하단 버튼을 클릭하거나 Ctrl+/ (또는 Cmd+/)를 눌러 챗봇을 사용하세요.');
})();