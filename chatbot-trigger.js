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
            <!-- Q&A 아이콘 -->
            <div style="color: #F5EFE6; font-weight: bold; font-size: 16px; text-align: center;">
                Q&A
            </div>
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