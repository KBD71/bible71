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

        // 성경 관련 키워드 검사 (더 유연하게)
        const bibleKeywords = [
            '성경', '하나님', '예수', '그리스도', '주님', '성령', '신앙', '믿음', '구원', '은혜', '기도',
            '교회', '목사', '장로', '성도', '크리스천', '기독교', '개신교', '개혁신학',
            '칼빈', '루터', '종교개혁', '웨스트민스터', '성화', '칭의', '선택', '예정', '언약',
            '말씀', '복음', '십자가', '부활', '천국', '지옥', '죄', '회개', '사랑', '소망', '평화',
            '찬송', '예배', '봉사', '선교', '전도', '목회', '신학', '교리', '성도', '교제',
            '주일', '새벽기도', '성경공부', '큐티', '묵상', '기도회', '부흥', '성령충만',
            '감사', '축복', '시련', '고난', '위로', '격려', '소명', '사명', '순종', '겸손'
        ];
        const lowerMessage = message.toLowerCase();
        const isRelevant = bibleKeywords.some(keyword => lowerMessage.includes(keyword.toLowerCase()));

        // 일반적인 인사말이나 간단한 질문도 허용
        const generalGreetings = ['안녕', '안녕하세요', '반가워', '처음', '소개', '도움', '질문'];
        const isGreeting = generalGreetings.some(greeting => lowerMessage.includes(greeting));

        if (!isRelevant && !isGreeting) {
            return res.json({
                success: true,
                response: '안녕하세요! 저는 개혁신학 성경 도우미입니다. 성경이나 신앙생활에 관련된 질문을 해주세요. 🙏'
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
        console.error('Claude API 오류:', error.response?.data || error.message);

        // 더 상세한 오류 로깅
        if (error.response) {
            console.error('Response status:', error.response.status);
            console.error('Response headers:', error.response.headers);
            console.error('Response data:', error.response.data);
        }

        // 기본 응답 (더 풍부하게)
        const fallbackResponses = {
            '기도': '기도는 하나님과의 소통입니다. "아무것도 염려하지 말고 다만 모든 일에 기도와 간구로, 너희 구할 것을 감사함으로 하나님께 아뢰라" (빌립보서 4:6) 🙏',
            '구원': '구원은 오직 예수 그리스도를 믿음으로만 얻을 수 있습니다. "믿음으로 말미암아 은혜로 구원을 받았나니 이것은 너희에게서 난 것이 아니요 하나님의 선물이라" (에베소서 2:8) ✨',
            '성경': '성경을 체계적으로 읽으시려면 맥체인 성경읽기를 추천합니다! "모든 성경은 하나님의 감동으로 된 것으로 교훈과 책망과 바르게 함과 의로 교육하기에 유익하니" (디모데후서 3:16) 📖',
            '하나님': '"하나님이 세상을 이처럼 사랑하사 독생자를 주셨으니 이는 그를 믿는 자마다 멸망하지 않고 영생을 얻게 하려 하심이라" (요한복음 3:16) 💝',
            '예수': '"예수께서 이르시되 내가 곧 길이요 진리요 생명이니 나로 말미암지 않고는 아버지께로 올 자가 없느니라" (요한복음 14:6) ✝️',
            '믿음': '"믿음은 바라는 것들의 실상이요 보이지 않는 것들의 증거니" (히브리서 11:1) 🌟',
            '사랑': '"하나님은 사랑이시라" (요한일서 4:8) 하나님의 사랑이 우리 삶의 중심입니다. ❤️',
            '소망': '"우리가 그리스도 안에서 바라기만 하면 모든 사람 가운데 가장 불쌍한 자리라" (고린도전서 15:19) 영원한 소망이 우리에게 있습니다. 🌈',
            '안녕': '안녕하세요! 저는 개혁신학을 바탕으로 한 성경 도우미입니다. 성경이나 신앙에 관해 궁금한 것이 있으시면 언제든 물어보세요! 😊'
        };

        const lowerMessage = req.body.message?.toLowerCase() || '';
        let fallbackResponse = '현재 AI 서비스에 일시적인 문제가 있습니다. 하지만 성경의 진리는 변하지 않습니다. "하나님의 말씀은 살았고 활력이 있어 좌우에 날선 어떤 검보다도 예리하다" (히브리서 4:12) 📖';

        // 키워드 매칭으로 적절한 응답 선택
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