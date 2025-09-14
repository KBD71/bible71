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

            console.log('🔗 API 호출 시작:', `${this.backendUrl}/api/chat`);
            console.log('📤 전송 데이터:', { message });

            const response = await fetch(`${this.backendUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message
                })
            });

            console.log('📥 응답 상태:', response.status, response.statusText);

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
            console.error('❌ 백엔드 API 호출 오류:', error);
            console.error('🔍 오류 상세:', {
                name: error.name,
                message: error.message,
                stack: error.stack
            });

            // 네트워크 오류인 경우
            if (error.name === 'TypeError' && (error.message.includes('fetch') || error.message.includes('Failed to fetch'))) {
                console.error('🌐 네트워크 연결 오류 발생');
                return {
                    success: false,
                    error: '서버에 연결할 수 없습니다. 네트워크 상태를 확인해주세요.'
                };
            }

            // 기타 오류
            return {
                success: false,
                error: error.message
            };
        }
    }


    // 응답 포매팅 (백엔드에서 이미 처리됨)
    formatResponse(response) {
        return response;
    }
}

// 전역 API 인스턴스 생성
const bibleAPI = new BibleChatBackendAPI();