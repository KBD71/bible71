// 백엔드 서버를 사용하는 API 호출 시스템

class BibleChatBackendAPI {
    constructor() {
        this.backendUrl = CONFIG.BACKEND_URL;
        this.conversationHistory = [];
        this.maxHistoryLength = 5;
    }

    // 백엔드 서버 연결 확인
    isConfigured() {
        return true; // 백엔드 서버가 API 키를 관리
    }

    // 대화 히스토리에 메시지 추가
    addToHistory(role, content) {
        this.conversationHistory.push({ role, content });

        // 최대 길이 유지
        if (this.conversationHistory.length > this.maxHistoryLength * 2) {
            this.conversationHistory = this.conversationHistory.slice(-this.maxHistoryLength * 2);
        }
    }

    // 백엔드 API 호출
    async callAPI(message) {
        try {
            // 메시지를 히스토리에 추가
            this.addToHistory('user', message);

            const response = await fetch(`${this.backendUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `서버 오류: ${response.status}`);
            }

            if (data.success) {
                // 응답을 히스토리에 추가
                this.addToHistory('assistant', data.response);

                return {
                    success: true,
                    response: data.response
                };
            } else {
                throw new Error(data.error || '알 수 없는 오류가 발생했습니다.');
            }

        } catch (error) {
            console.error('백엔드 API 호출 오류:', error);

            // 네트워크 오류인 경우
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                return {
                    success: false,
                    error: '서버에 연결할 수 없습니다. 백엔드 서버가 실행 중인지 확인해주세요.',
                    fallbackResponse: this.getFallbackResponse(message)
                };
            }

            // 기타 오류
            return {
                success: false,
                error: error.message,
                fallbackResponse: this.getFallbackResponse(message)
            };
        }
    }

    // 서버 연결 실패시 기본 응답
    getFallbackResponse(message) {
        const lowerMessage = message.toLowerCase();

        if (lowerMessage.includes('기도') || lowerMessage.includes('기도시간') || lowerMessage.includes('기도방법')) {
            return '기도는 하나님과의 소통입니다. "아무것도 염려하지 말고 다만 모든 일에 기도와 간구로, 너희 구할 것을 감사함으로 하나님께 아뢰라" (빌립보서 4:6) 🙏';
        } else if (lowerMessage.includes('성경읽기') || lowerMessage.includes('읽기계획') || lowerMessage.includes('성경공부')) {
            return '성경을 체계적으로 읽으시려면 맥체인 성경읽기를 추천합니다! "모든 성경은 하나님의 감동으로 된 것으로 교훈과 책망과 바르게 함과 의로 교육하기에 유익하니" (디모데후서 3:16) 📖';
        } else if (lowerMessage.includes('구원') || lowerMessage.includes('믿음')) {
            return '구원은 오직 예수 그리스도를 믿음으로만 얻을 수 있습니다. "믿음으로 말미암아 은혜로 구원을 받았나니 이것은 너희에게서 난 것이 아니요 하나님의 선물이라" (에베소서 2:8) ✨';
        } else if (lowerMessage.includes('오늘') && (lowerMessage.includes('말씀') || lowerMessage.includes('성경') || lowerMessage.includes('구절'))) {
            const today = new Date();
            const verses = [
                '"여호와는 나의 목자시니 내게 부족함이 없으리로다" - 시편 23:1',
                '"수고하고 무거운 짐 진 자들아 다 내게로 오라 내가 너희를 쉬게 하리라" - 마태복음 11:28',
                '"내가 너희에게 평강을 끼치노니 곧 나의 평강을 너희에게 주노라" - 요한복음 14:27',
                '"범사에 감사하라 이것이 그리스도 예수 안에서 너희를 향하신 하나님의 뜻이니라" - 데살로니가전서 5:18'
            ];
            return verses[today.getDate() % verses.length];
        } else {
            return '서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요. 💡';
        }
    }

    // 응답 포매팅 (백엔드에서 이미 처리됨)
    formatResponse(response) {
        return response;
    }
}

// 전역 API 인스턴스 생성
const bibleAPI = new BibleChatBackendAPI();