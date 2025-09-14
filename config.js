// API 설정 파일
// 실제 사용시 API 키는 환경변수나 서버사이드에서 관리해야 합니다.

const CONFIG = {
    // Claude API 설정 (기본 사용)
    CLAUDE_API_KEY: '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', // 보안을 위해 API 키는 별도로 설정하세요 (백엔드 서버 사용시)
    CLAUDE_API_URL: 'https://api.anthropic.com/v1/messages',

    // OpenAI API 설정 (대체 옵션)
    // OPENAI_API_KEY: '',
    // OPENAI_API_URL: 'https://api.openai.com/v1/chat/completions',

    // 사용할 API 서비스 선택
    API_SERVICE: 'claude', // 'claude' 또는 'openai'

    // 모델 설정
    MODEL: 'claude-sonnet-4-20250514', // Claude Sonnet 4 (최신 최고 성능 모델)
    // MODEL: 'claude-3-5-haiku-20241022', // Claude 3.5 Haiku (빠르고 경제적)
    // MODEL: 'claude-3-5-sonnet-20241022', // Claude 3.5 Sonnet (더 정확, 비싸)

    // 응답 설정
    MAX_TOKENS: 300, // 간결한 답변을 위해 토큰 수 제한
    TEMPERATURE: 0.3, // 더 일관된 응답을 위해 낮은 값 설정

    // Claude 전용 설정
    ANTHROPIC_VERSION: '2023-06-01',

    // 성경 관련 키워드 (질문 필터링용)
    BIBLE_KEYWORDS: [
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
    ]
};

// API 키가 설정되지 않은 경우 경고
if (CONFIG.API_SERVICE === 'claude' && (!CONFIG.CLAUDE_API_KEY || CONFIG.CLAUDE_API_KEY === '')) {
    console.warn('⚠️ Claude API 키가 설정되지 않았습니다. config.js 파일에서 CLAUDE_API_KEY를 설정해주세요.');
} else if (CONFIG.API_SERVICE === 'openai' && (!CONFIG.OPENAI_API_KEY || CONFIG.OPENAI_API_KEY === '')) {
    console.warn('⚠️ OpenAI API 키가 설정되지 않았습니다. config.js 파일에서 OPENAI_API_KEY를 설정해주세요.');
}
