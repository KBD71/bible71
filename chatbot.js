// 성경 도우미 챗봇 스크립트
// 모든 페이지에서 사용할 수 있는 플로팅 챗봇

(function() {
    // 이미 챗봇이 추가되어 있다면 중복 방지
    if (document.getElementById('chatbot-container')) {
        return;
    }

    // 챗봇 CSS 스타일 추가
    const style = document.createElement('style');
    style.textContent = `
        :root {
            --color-primary: #8B0000;
            --color-secondary: #004D40;
            --color-accent: #DAA520;
            --color-text-main: #4E342E;
            --color-text-light: #6D4C41;
            --color-parchment: #F5EFE6;
        }

        .chatbot-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 10000;
            font-family: 'Noto Sans KR', sans-serif;
        }
        .chatbot-toggle {
            width: 60px;
            height: 60px;
            background: var(--color-primary);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            border: 2px solid var(--color-accent);
        }
        .chatbot-toggle:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 25px rgba(0,0,0,0.4);
        }
        .chatbot-toggle svg {
            width: 28px;
            height: 28px;
            color: var(--color-parchment);
        }
        .chatbot-window {
            position: absolute;
            bottom: 80px;
            right: 0;
            width: 350px;
            height: 500px;
            background: var(--color-parchment);
            border: 2px solid var(--color-accent);
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            display: none;
            flex-direction: column;
            overflow: hidden;
        }
        .chatbot-header {
            background: linear-gradient(135deg, var(--color-primary), #A00000);
            color: var(--color-parchment);
            padding: 16px;
            text-align: center;
            font-weight: 600;
            font-size: 16px;
            border-bottom: 1px solid var(--color-accent);
        }
        .chatbot-messages {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            background: var(--color-parchment);
        }
        .message {
            margin-bottom: 12px;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }
        .message.user {
            justify-content: flex-end;
        }
        .message.bot {
            justify-content: flex-start;
        }
        .message-content {
            max-width: 80%;
            padding: 10px 12px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.4;
        }
        .message.user .message-content {
            background: var(--color-secondary);
            color: var(--color-parchment);
            border-bottom-right-radius: 4px;
        }
        .message.bot .message-content {
            background: rgba(218, 165, 32, 0.1);
            color: var(--color-text-main);
            border: 1px solid rgba(218, 165, 32, 0.3);
            border-bottom-left-radius: 4px;
        }
        .chatbot-input {
            padding: 12px;
            border-top: 1px solid rgba(218, 165, 32, 0.3);
            background: var(--color-parchment);
        }
        .chatbot-input-field {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid rgba(218, 165, 32, 0.3);
            border-radius: 20px;
            outline: none;
            font-size: 14px;
            background: white;
            color: var(--color-text-main);
            box-sizing: border-box;
        }
        .chatbot-input-field:focus {
            border-color: var(--color-accent);
        }
        .quick-questions {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 8px;
        }
        .quick-question-btn {
            padding: 6px 12px;
            background: rgba(218, 165, 32, 0.1);
            border: 1px solid rgba(218, 165, 32, 0.3);
            border-radius: 15px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
            color: var(--color-text-main);
        }
        .quick-question-btn:hover {
            background: var(--color-accent);
            color: white;
        }
        @media (max-width: 768px) {
            .chatbot-container {
                bottom: 15px;
                right: 15px;
            }
            .chatbot-window {
                width: calc(100vw - 30px);
                right: -15px;
                height: 450px;
            }
            .chatbot-toggle {
                width: 55px;
                height: 55px;
            }
        }
    `;
    document.head.appendChild(style);

    // 챗봇 HTML 구조 생성
    const chatbotHTML = `
        <div class="chatbot-container" id="chatbot-container">
            <div class="chatbot-window" id="chatbot-window">
                <div class="chatbot-header">
                    성경 도우미 챗봇
                </div>
                <div class="chatbot-messages" id="chatbot-messages">
                    <div class="message bot">
                        <div class="message-content">
                            안녕하세요! 성경 공부와 관련된 질문을 도와드리겠습니다. 궁금한 것이 있으시면 언제든 물어보세요! 🙏
                        </div>
                    </div>
                </div>
                <div class="chatbot-input">
                    <input type="text" class="chatbot-input-field" id="chatbot-input" placeholder="성경이나 신앙에 관해 질문해보세요...">
                    <div class="quick-questions">
                        <button class="quick-question-btn" data-question="오늘의 성경구절 추천해주세요">오늘의 말씀</button>
                        <button class="quick-question-btn" data-question="기도 시간을 어떻게 가져야 할까요?">기도 방법</button>
                        <button class="quick-question-btn" data-question="성경 읽기 계획을 추천해주세요">읽기 계획</button>
                        <button class="quick-question-btn" data-question="신앙생활에 도움이 되는 조언을 해주세요">신앙 조언</button>
                    </div>
                </div>
            </div>

            <div class="chatbot-toggle" id="chatbot-toggle">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
            </div>
        </div>
    `;

    // DOM에 챗봇 추가
    document.body.insertAdjacentHTML('beforeend', chatbotHTML);

    // 챗봇 기능 구현
    function initChatbot() {
        const chatbotToggle = document.getElementById('chatbot-toggle');
        const chatbotWindow = document.getElementById('chatbot-window');
        const chatbotInput = document.getElementById('chatbot-input');
        const chatbotMessages = document.getElementById('chatbot-messages');
        const quickQuestionBtns = document.querySelectorAll('.quick-question-btn');

        let isChatbotOpen = false;

        // 챗봇 토글 기능
        chatbotToggle.addEventListener('click', () => {
            isChatbotOpen = !isChatbotOpen;
            chatbotWindow.style.display = isChatbotOpen ? 'flex' : 'none';

            if (isChatbotOpen) {
                chatbotInput.focus();
            }
        });

        // 메시지 추가 함수
        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;

            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.textContent = content;

            messageDiv.appendChild(messageContent);
            chatbotMessages.appendChild(messageDiv);

            // 스크롤을 맨 아래로
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        }

        // 챗봇 응답 생성 함수
        function getBotResponse(userMessage) {
            const message = userMessage.toLowerCase();

            // 성경 관련 키워드 응답
            if (message.includes('기도') || message.includes('기도시간') || message.includes('기도방법')) {
                return '기도는 하나님과의 소통입니다. 조용한 곳에서 마음을 편히 하시고, 감사한 마음으로 하나님께 대화하듯 기도해보세요. 매일 일정한 시간을 정해 기도하는 것이 좋습니다. 🙏';
            } else if (message.includes('성경읽기') || message.includes('읽기계획') || message.includes('성경공부')) {
                return '성경을 체계적으로 읽으시려면 맥체인 성경읽기를 추천합니다! 하루에 구약 2장, 신약 2장씩 읽으면 1년에 성경을 완독할 수 있습니다. 📖';
            } else if (message.includes('오늘') && (message.includes('말씀') || message.includes('성경') || message.includes('구절'))) {
                const today = new Date();
                const verses = [
                    '"여호와는 나의 목자시니 내게 부족함이 없으리로다" - 시편 23:1',
                    '"수고하고 무거운 짐 진 자들아 다 내게로 오라 내가 너희를 쉬게 하리라" - 마태복음 11:28',
                    '"내가 너희에게 평강을 끼치노니 곧 나의 평강을 너희에게 주노라" - 요한복음 14:27',
                    '"범사에 감사하라 이것이 그리스도 예수 안에서 너희를 향하신 하나님의 뜻이니라" - 데살로니가전서 5:18'
                ];
                return verses[today.getDate() % verses.length];
            } else if (message.includes('신앙') || message.includes('조언') || message.includes('도움')) {
                return '신앙생활의 기본은 말씀과 기도입니다. 매일 성경을 읽고 기도하며, 주일 예배에 참석하세요. 또한 다른 성도들과 교제하며 서로 격려하는 것도 중요합니다. 하나님의 사랑 안에서 성장해 나가시길 기도합니다! ✨';
            } else if (message.includes('안녕') || message.includes('반가') || message.includes('처음')) {
                return '안녕하세요! 성경 공부를 도와주는 챗봇입니다. 성경이나 신앙에 관한 궁금한 점이 있으시면 언제든 말씀해주세요! 😊';
            } else if (message.includes('감사') || message.includes('고마워')) {
                return '천만에요! 더 궁금한 것이 있으시면 언제든 물어보세요. 하나님의 은혜가 함께 하시길 기도합니다! 🙏';
            } else {
                return '죄송합니다. 정확한 답변을 드리기 어려워요. 성경이나 신앙생활에 관련된 구체적인 질문을 해주시면 더 도움이 될 것 같습니다. 위의 버튼들을 눌러보시는 것도 좋아요! 💡';
            }
        }

        // 메시지 전송 함수
        function sendMessage() {
            const message = chatbotInput.value.trim();
            if (message === '') return;

            // 사용자 메시지 추가
            addMessage(message, true);

            // 입력창 비우기
            chatbotInput.value = '';

            // 잠시 후 봇 응답 (실제 환경에서는 API 호출)
            setTimeout(() => {
                const response = getBotResponse(message);
                addMessage(response, false);
            }, 500);
        }

        // 엔터키로 메시지 전송
        chatbotInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // 빠른 질문 버튼 클릭 처리
        quickQuestionBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const question = btn.dataset.question;
                addMessage(question, true);

                setTimeout(() => {
                    const response = getBotResponse(question);
                    addMessage(response, false);
                }, 500);
            });
        });

        // 외부 클릭시 챗봇 닫기
        document.addEventListener('click', (e) => {
            if (!chatbotToggle.contains(e.target) && !chatbotWindow.contains(e.target) && isChatbotOpen) {
                isChatbotOpen = false;
                chatbotWindow.style.display = 'none';
            }
        });
    }

    // DOM이 로드된 후 초기화
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatbot);
    } else {
        initChatbot();
    }
})();