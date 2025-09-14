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
            <!-- 존 칼빈의 문장: "Cor meum tibi offero Domine prompte et sincere" -->
            <svg viewBox="0 0 100 100" fill="currentColor">
                <!-- 손 (오른손, 위로 향함) -->
                <g fill="currentColor">
                    <!-- 손목 -->
                    <rect x="40" y="55" width="20" height="12" rx="3"/>

                    <!-- 손바닥 -->
                    <ellipse cx="50" cy="45" rx="12" ry="8"/>

                    <!-- 엄지손가락 -->
                    <ellipse cx="35" cy="40" rx="4" ry="8" transform="rotate(-30 35 40)"/>

                    <!-- 검지손가락 -->
                    <rect x="45" y="30" width="4" height="15" rx="2"/>

                    <!-- 중지손가락 -->
                    <rect x="50" y="25" width="4" height="20" rx="2"/>

                    <!-- 약지손가락 -->
                    <rect x="55" y="30" width="4" height="15" rx="2"/>

                    <!-- 소지손가락 -->
                    <rect x="60" y="35" width="3" height="12" rx="1.5"/>
                </g>

                <!-- 손 위의 심장 (하트 모양) -->
                <g fill="#DAA520">
                    <!-- 하트 모양 (두 개의 원과 삼각형 조합) -->
                    <circle cx="45" cy="20" r="6"/>
                    <circle cx="55" cy="20" r="6"/>
                    <path d="M38 24 L50 38 L62 24 Q62 18 55 18 Q50 15 45 18 Q38 18 38 24 Z"/>
                </g>

                <!-- 하트 내부의 십자가 (선택적) -->
                <g stroke="currentColor" stroke-width="1.5" fill="none">
                    <line x1="50" y1="18" x2="50" y2="28"/>
                    <line x1="45" y1="23" x2="55" y2="23"/>
                </g>

                <!-- 문장 테두리 (원형) -->
                <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="2" opacity="0.3"/>
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