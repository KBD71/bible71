// Vercel 서버리스 함수: 성경 챗봇 API

module.exports = async (req, res) => {
    // CORS 설정
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // OPTIONS 요청 처리
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    // GET 요청시 디버그 정보
    if (req.method === 'GET') {
        return res.json({
            status: 'OK',
            timestamp: new Date().toISOString(),
            message: '성경 챗봇 API가 작동 중입니다! 📖',
            debug: {
                hasApiKey: !!process.env.CLAUDE_API_KEY,
                apiKeyLength: process.env.CLAUDE_API_KEY ? process.env.CLAUDE_API_KEY.length : 0,
                model: process.env.CLAUDE_MODEL || 'claude-sonnet-4-20250514',
                maxTokens: process.env.MAX_TOKENS || '300',
                temperature: process.env.TEMPERATURE || '0.3'
            }
        });
    }

    // POST 요청 처리
    if (req.method !== 'POST') {
        return res.status(405).json({
            success: false,
            error: 'POST, GET 요청만 허용됩니다.'
        });
    }

    // API 키 확인
    if (!process.env.CLAUDE_API_KEY) {
        console.error('CLAUDE_API_KEY 환경변수가 설정되지 않았습니다');
        return res.status(500).json({
            success: false,
            error: 'API 키가 설정되지 않았습니다. Vercel 환경변수를 확인해주세요.'
        });
    }

    try {
        const { message } = req.body;

        // 입력 검증
        if (!message || typeof message !== 'string') {
            return res.status(400).json({
                success: false,
                error: '메시지를 입력해주세요.'
            });
        }

        // 메시지 길이 제한
        if (message.length > 500) {
            return res.status(400).json({
                success: false,
                error: '메시지가 너무 깁니다. (최대 500자)'
            });
        }

        // 성경 관련 키워드 검사
        const bibleKeywords = ['성경', '하나님', '예수', '그리스도', '주님', '성령', '신앙', '믿음', '구원', '은혜', '기도'];
        const lowerMessage = message.toLowerCase();
        const isRelevant = bibleKeywords.some(keyword => lowerMessage.includes(keyword.toLowerCase()));

        if (!isRelevant && !lowerMessage.includes('기도') && !lowerMessage.includes('믿음')) {
            return res.json({
                success: true,
                response: '죄송합니다. 성경이나 신앙생활과 관련된 질문만 답변드릴 수 있습니다. 🙏'
            });
        }

        // Claude API 호출을 위한 axios import
        const axios = require('axios');

        const response = await axios.post(
            'https://api.anthropic.com/v1/messages',
            {
                model: process.env.CLAUDE_MODEL || 'claude-sonnet-4-20250514',
                max_tokens: parseInt(process.env.MAX_TOKENS) || 300,
                temperature: parseFloat(process.env.TEMPERATURE) || 0.3,
                messages: [
                    {
                        role: 'user',
                        content: `당신은 개혁신학을 바탕으로 한 성경 교사입니다. 존 칼빈의 전통을 따라 성경을 해석하고 가르칩니다. 다음 질문에 한국어로 간결하고 정확하게 답변해주세요 (최대 200자): ${message}`
                    }
                ]
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': process.env.CLAUDE_API_KEY,
                    'anthropic-version': '2023-06-01'
                }
            }
        );

        return res.json({
            success: true,
            response: response.data.content[0].text
        });

    } catch (error) {
        console.error('API 오류:', error.response?.data || error.message);

        // 기본 응답
        const fallbackResponses = {
            '기도': '기도는 하나님과의 소통입니다. "아무것도 염려하지 말고 다만 모든 일에 기도와 간구로, 너희 구할 것을 감사함으로 하나님께 아뢰라" (빌립보서 4:6) 🙏',
            '구원': '구원은 오직 예수 그리스도를 믿음으로만 얻을 수 있습니다. "믿음으로 말미암아 은혜로 구원을 받았나니 이것은 너희에게서 난 것이 아니요 하나님의 선물이라" (에베소서 2:8) ✨',
            '성경': '성경을 체계적으로 읽으시려면 맥체인 성경읽기를 추천합니다! "모든 성경은 하나님의 감동으로 된 것으로 교훈과 책망과 바르게 함과 의로 교육하기에 유익하니" (디모데후서 3:16) 📖'
        };

        const lowerMessage = req.body.message?.toLowerCase() || '';
        let fallbackResponse = '죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요.';

        for (const [keyword, response] of Object.entries(fallbackResponses)) {
            if (lowerMessage.includes(keyword)) {
                fallbackResponse = response;
                break;
            }
        }

        return res.json({
            success: true,
            response: fallbackResponse
        });
    }
};