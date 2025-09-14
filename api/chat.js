// Vercel 서버리스 함수: 챗봇 API
import axios from 'axios';

// 성경 관련 키워드
const BIBLE_KEYWORDS = [
    '성경', '하나님', '예수', '그리스도', '주님', '성령', '신앙', '믿음', '구원', '은혜',
    '기도', '예배', '교회', '목사', '장로', '성도', '크리스천', '기독교', '개신교', '개혁신학',
    '칼빈', '루터', '종교개혁', '웨스트민스터', '성화', '칭의', '선택', '예정', '언약',
    '구약', '신약', '창세기', '출애굽기', '레위기', '민수기', '신명기', '여호수아', '사사기', '룻기',
    '사무엘', '열왕기', '역대기', '에스라', '느헤미야', '에스더', '욥기', '시편', '잠언', '전도서', '아가',
    '이사야', '예레미야', '예레미야애가', '에스겔', '다니엘', '호세아', '요엘', '아모스', '오바댜',
    '요나', '미가', '나훔', '하박국', '스바냐', '학개', '스가랴', '말라기',
    '마태복음', '마가복음', '누가복음', '요한복음', '사도행전', '로마서', '고린도전서', '고린도후서',
    '갈라디아서', '에베소서', '빌립보서', '골로새서', '데살로니가전서', '데살로니가후서',
    '디모데전서', '디모데후서', '디도서', '빌레몬서', '히브리서', '야고보서', '베드로전서', '베드로후서',
    '요한일서', '요한이서', '요한삼서', '유다서', '요한계시록'
];

// 질문 적절성 검사
function isAppropriateQuestion(question) {
    const lowerQuestion = question.toLowerCase();

    // 성경/신앙 관련 키워드가 포함되어 있는지 확인
    const hasRelevantKeyword = BIBLE_KEYWORDS.some(keyword =>
        lowerQuestion.includes(keyword.toLowerCase())
    );

    // 기본적인 신앙 질문들
    const faithQuestions = ['기도', '믿음', '구원', '천국', '지옥', '죄', '회개', '사랑'];
    const hasFaithKeyword = faithQuestions.some(keyword =>
        lowerQuestion.includes(keyword)
    );

    return hasRelevantKeyword || hasFaithKeyword;
}

// Claude API 호출
async function callClaudeAPI(message) {
    try {
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

        return {
            success: true,
            response: response.data.content[0].text
        };
    } catch (error) {
        console.error('Claude API 오류:', error.response?.data || error.message);

        return {
            success: false,
            error: error.response?.data?.error?.message || '일시적인 오류가 발생했습니다.'
        };
    }
}

// Vercel 서버리스 함수 핸들러
export default async function handler(req, res) {
    // CORS 헤더 설정
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // OPTIONS 요청 처리 (CORS preflight)
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    // GET 요청시 디버그 정보 반환
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

    // POST 요청만 허용
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

        // 질문 적절성 검사
        if (!isAppropriateQuestion(message)) {
            return res.json({
                success: true,
                response: '죄송합니다. 성경이나 신앙생활과 관련된 질문만 답변드릴 수 있습니다. 🙏'
            });
        }

        // Claude API 호출
        const result = await callClaudeAPI(message);

        if (result.success) {
            return res.json({
                success: true,
                response: result.response
            });
        } else {
            // API 오류시 기본 응답
            const fallbackResponses = {
                '기도': '기도는 하나님과의 소통입니다. "아무것도 염려하지 말고 다만 모든 일에 기도와 간구로, 너희 구할 것을 감사함으로 하나님께 아뢰라" (빌립보서 4:6) 🙏',
                '구원': '구원은 오직 예수 그리스도를 믿음으로만 얻을 수 있습니다. "믿음으로 말미암아 은혜로 구원을 받았나니 이것은 너희에게서 난 것이 아니요 하나님의 선물이라" (에베소서 2:8) ✨',
                '성경': '성경을 체계적으로 읽으시려면 맥체인 성경읽기를 추천합니다! "모든 성경은 하나님의 감동으로 된 것으로 교훈과 책망과 바르게 함과 의로 교육하기에 유익하니" (디모데후서 3:16) 📖'
            };

            const lowerMessage = message.toLowerCase();
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

    } catch (error) {
        console.error('서버 오류:', error);
        return res.status(500).json({
            success: false,
            error: '서버 오류가 발생했습니다.'
        });
    }
}