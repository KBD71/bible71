// 성경 관련 질문 필터링 시스템

class QuestionFilter {
    constructor() {
        this.bibleKeywords = CONFIG.BIBLE_KEYWORDS;
        this.prohibitedTopics = [
            '정치', '선거', '정당', '대통령', '국회의원',
            '주식', '투자', '돈', '부동산', '재테크',
            '연애', '결혼', '이혼', '섹스', '성관계',
            '폭력', '살인', '자살', '마약', '범죄',
            '타종교', '불교', '이슬람', '힌두교', '점술',
            '게임', '영화', '드라마', '연예인', '스포츠'
        ];
    }

    // 질문이 성경/신앙 관련인지 확인
    isBibleRelated(question) {
        const normalizedQuestion = question.toLowerCase();

        // 성경 관련 키워드가 있는지 확인
        const hasBibleKeyword = this.bibleKeywords.some(keyword =>
            normalizedQuestion.includes(keyword.toLowerCase())
        );

        // 금지된 주제가 있는지 확인
        const hasProhibitedTopic = this.prohibitedTopics.some(topic =>
            normalizedQuestion.includes(topic)
        );

        // 일반적인 신앙 관련 표현들 확인
        const faithExpressions = [
            '어떻게 살아야', '왜 하나님', '주님께서', '말씀에서',
            '신앙', '믿음', '기도', '예배', '교회', '목사',
            '성경에서', '하나님의 뜻', '구원', '천국', '지옥',
            '죄', '회개', '용서', '사랑', '은혜', '축복'
        ];

        const hasFaithExpression = faithExpressions.some(expr =>
            normalizedQuestion.includes(expr)
        );

        return (hasBibleKeyword || hasFaithExpression) && !hasProhibitedTopic;
    }

    // 질문의 적절성 검사
    isAppropriate(question) {
        // 너무 짧은 질문 필터링
        if (question.trim().length < 3) {
            return {
                isValid: false,
                reason: 'too_short',
                message: '질문이 너무 짧습니다. 더 구체적으로 질문해주세요.'
            };
        }

        // 너무 긴 질문 필터링
        if (question.length > 500) {
            return {
                isValid: false,
                reason: 'too_long',
                message: '질문이 너무 깁니다. 더 간결하게 질문해주세요.'
            };
        }

        // 반복된 문자나 의미없는 텍스트 확인
        const repeatedPattern = /(.)\1{10,}/;
        if (repeatedPattern.test(question)) {
            return {
                isValid: false,
                reason: 'invalid_format',
                message: '올바른 형식의 질문을 입력해주세요.'
            };
        }

        // 성경 관련성 확인
        if (!this.isBibleRelated(question)) {
            return {
                isValid: false,
                reason: 'not_bible_related',
                message: '죄송합니다. 성경이나 신앙생활과 관련된 질문만 답변드릴 수 있습니다. 🙏'
            };
        }

        return {
            isValid: true,
            reason: 'valid',
            message: ''
        };
    }

    // 질문을 정제하여 API에 보낼 형태로 가공
    sanitizeQuestion(question) {
        // 기본적인 정제
        let cleaned = question.trim();

        // 특수문자 정리 (기본적인 문장부호는 유지)
        cleaned = cleaned.replace(/[^\w가-힣\s.,!?;:()\-"']/g, '');

        // 연속된 공백 제거
        cleaned = cleaned.replace(/\s+/g, ' ');

        // 질문 형태로 변환 (마지막에 물음표가 없으면 추가)
        if (!cleaned.endsWith('?') && !cleaned.endsWith('.') && !cleaned.endsWith('!')) {
            cleaned += '?';
        }

        return cleaned;
    }

    // 응급 상황 감지 (자살, 위기 등)
    detectEmergency(question) {
        const emergencyKeywords = [
            '자살', '죽고싶', '살기싫', '우울해서', '절망적',
            '죽어버리고', '세상이 싫어', '포기하고 싶'
        ];

        const hasEmergencyKeyword = emergencyKeywords.some(keyword =>
            question.includes(keyword)
        );

        if (hasEmergencyKeyword) {
            return {
                isEmergency: true,
                message: '힘든 시간을 보내고 계신 것 같습니다. 전문적인 도움이 필요하시면 생명의전화(109) 또는 가까운 상담센터에 연락해주세요. 하나님께서는 당신을 사랑하고 계십니다. 🙏'
            };
        }

        return {
            isEmergency: false,
            message: ''
        };
    }

    // 질문 복잡도 분석
    analyzeComplexity(question) {
        const words = question.split(/\s+/);
        const sentences = question.split(/[.!?]+/).filter(s => s.trim().length > 0);

        let complexity = 'simple';

        if (words.length > 20 || sentences.length > 2) {
            complexity = 'medium';
        }

        if (words.length > 50 || sentences.length > 4) {
            complexity = 'complex';
        }

        return {
            complexity,
            wordCount: words.length,
            sentenceCount: sentences.length
        };
    }
}

// 전역에서 사용할 수 있도록 인스턴스 생성
const questionFilter = new QuestionFilter();