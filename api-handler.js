// API 호출 및 응답 처리 시스템

class BibleChatAPI {
    constructor() {
        this.apiService = CONFIG.API_SERVICE;
        this.model = CONFIG.MODEL;
        this.maxTokens = CONFIG.MAX_TOKENS;
        this.temperature = CONFIG.TEMPERATURE;

        // API 설정
        if (this.apiService === 'claude') {
            this.apiKey = CONFIG.CLAUDE_API_KEY;
            this.apiUrl = CONFIG.CLAUDE_API_URL;
            this.anthropicVersion = CONFIG.ANTHROPIC_VERSION;
        } else {
            this.apiKey = CONFIG.OPENAI_API_KEY;
            this.apiUrl = CONFIG.OPENAI_API_URL;
        }

        // 대화 히스토리 (최근 5개 대화만 유지)
        this.conversationHistory = [];
        this.maxHistoryLength = 5;
    }

    // API 키 확인
    isConfigured() {
        return this.apiKey && this.apiKey !== '';
    }

    // 대화 히스토리에 메시지 추가
    addToHistory(role, content) {
        this.conversationHistory.push({ role, content });

        // 히스토리 길이 제한
        if (this.conversationHistory.length > this.maxHistoryLength * 2) {
            this.conversationHistory = this.conversationHistory.slice(-this.maxHistoryLength * 2);
        }
    }

    // 메시지 구성 (Claude와 OpenAI 형식 구분)
    buildMessages(userQuestion) {
        const questionCategory = categorizeQuestion(userQuestion);
        const systemPrompt = REFORMED_THEOLOGY.getSystemPrompt();
        const specificGuidance = REFORMED_THEOLOGY.getSpecificGuidance(questionCategory);

        const fullSystemPrompt = systemPrompt + (specificGuidance ? '\n\n특별 지침: ' + specificGuidance : '');

        if (this.apiService === 'claude') {
            // Claude 형식
            const messages = [];

            // 대화 히스토리 추가 (Claude는 system과 user 메시지 번갈아가며)
            this.conversationHistory.forEach(msg => {
                messages.push({
                    role: msg.role === 'assistant' ? 'assistant' : 'user',
                    content: msg.content
                });
            });

            // 현재 질문 추가
            messages.push({
                role: "user",
                content: userQuestion
            });

            return {
                system: fullSystemPrompt,
                messages: messages
            };
        } else {
            // OpenAI 형식
            const messages = [
                {
                    role: "system",
                    content: fullSystemPrompt
                }
            ];

            // 최근 대화 히스토리 추가
            messages.push(...this.conversationHistory);

            // 현재 질문 추가
            messages.push({
                role: "user",
                content: userQuestion
            });

            return { messages };
        }
    }

    // API 호출
    async callAPI(userQuestion) {
        if (!this.isConfigured()) {
            throw new Error('API가 설정되지 않았습니다. config.js 파일에서 API 키를 설정해주세요.');
        }

        try {
            const messageData = this.buildMessages(userQuestion);
            let response;

            if (this.apiService === 'claude') {
                // Claude API 호출
                response = await fetch(this.apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'x-api-key': this.apiKey,
                        'anthropic-version': this.anthropicVersion
                    },
                    body: JSON.stringify({
                        model: this.model,
                        system: messageData.system,
                        messages: messageData.messages,
                        max_tokens: this.maxTokens,
                        temperature: this.temperature
                    })
                });
            } else {
                // OpenAI API 호출
                response = await fetch(this.apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${this.apiKey}`
                    },
                    body: JSON.stringify({
                        model: this.model,
                        messages: messageData.messages,
                        max_tokens: this.maxTokens,
                        temperature: this.temperature,
                        presence_penalty: 0.1,
                        frequency_penalty: 0.1
                    })
                });
            }

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMessage = this.apiService === 'claude'
                    ? errorData.error?.message || 'Claude API 오류'
                    : errorData.error?.message || 'OpenAI API 오류';
                throw new Error(`API 오류 (${response.status}): ${errorMessage}`);
            }

            const data = await response.json();
            let assistantResponse;

            if (this.apiService === 'claude') {
                // Claude 응답 처리
                if (!data.content || !data.content[0] || !data.content[0].text) {
                    throw new Error('Claude API로부터 올바르지 않은 응답을 받았습니다.');
                }
                assistantResponse = data.content[0].text;
            } else {
                // OpenAI 응답 처리
                if (!data.choices || !data.choices[0] || !data.choices[0].message) {
                    throw new Error('OpenAI API로부터 올바르지 않은 응답을 받았습니다.');
                }
                assistantResponse = data.choices[0].message.content;
            }

            // 대화 히스토리에 추가
            this.addToHistory("user", userQuestion);
            this.addToHistory("assistant", assistantResponse);

            return {
                success: true,
                response: assistantResponse,
                usage: data.usage || data.usage_stats || {}
            };

        } catch (error) {
            console.error('API 호출 오류:', error);
            return {
                success: false,
                error: error.message,
                fallbackResponse: this.getFallbackResponse(userQuestion)
            };
        }
    }

    // API 실패 시 대체 응답
    getFallbackResponse(question) {
        const fallbackResponses = [
            {
                keywords: ['구원', '믿음', '예수'],
                response: '구원은 오직 예수 그리스도를 믿음으로만 얻을 수 있습니다. "믿음으로 말미암아 은혜로 구원을 받았나니 이것은 너희에게서 난 것이 아니요 하나님의 선물이라" (에베소서 2:8) 🙏'
            },
            {
                keywords: ['기도', '간구'],
                response: '기도는 하나님과의 소통이며, 우리의 필요를 아뢰고 하나님의 뜻을 구하는 것입니다. "아무것도 염려하지 말고 다만 모든 일에 기도와 간구로, 너희 구할 것을 감사함으로 하나님께 아뢰라" (빌립보서 4:6) 💭'
            },
            {
                keywords: ['성경', '말씀'],
                response: '성경은 하나님의 말씀으로 우리의 믿음과 행위에 완전한 지침이 됩니다. "모든 성경은 하나님의 감동으로 된 것으로 교훈과 책망과 바르게 함과 의로 교육하기에 유익하니" (디모데후서 3:16) 📖'
            }
        ];

        // 키워드 매칭으로 적절한 응답 찾기
        for (const fallback of fallbackResponses) {
            if (fallback.keywords.some(keyword => question.includes(keyword))) {
                return fallback.response;
            }
        }

        // 기본 응답
        return '죄송합니다. 현재 서비스에 일시적인 문제가 있습니다. 성경 말씀을 묵상하시거나 기도로 하나님께 직접 구하시기를 권합니다. "너희 중에 누구든지 지혜가 부족하거든 모든 사람에게 후히 주시고 꾸짖지 아니하시는 하나님께 구하라 그리하면 주시리라" (야고보서 1:5) 🙏';
    }

    // 대화 히스토리 초기화
    clearHistory() {
        this.conversationHistory = [];
    }

    // 응답 후처리 (길이 제한, 형식화 등)
    formatResponse(response) {
        // 너무 긴 응답 자르기
        if (response.length > 1500) {
            const truncated = response.substring(0, 1400);
            const lastSentence = truncated.lastIndexOf('.');
            if (lastSentence > 1000) {
                response = truncated.substring(0, lastSentence + 1) + '\n\n더 자세한 내용이 필요하시면 다시 질문해주세요.';
            }
        }

        // 기본적인 형식 정리
        response = response.replace(/\n{3,}/g, '\n\n'); // 연속된 줄바꿈 정리
        response = response.trim();

        return response;
    }
}

// API 핸들러 인스턴스 생성
const bibleAPI = new BibleChatAPI();