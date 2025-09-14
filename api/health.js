// Vercel 서버리스 함수: 헬스체크
export default function handler(req, res) {
    // CORS 헤더 설정
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'GET') {
        return res.status(405).json({
            error: 'GET 요청만 허용됩니다.'
        });
    }

    res.json({
        status: 'OK',
        timestamp: new Date().toISOString(),
        message: '성경 챗봇 API가 정상 작동 중입니다! 📖'
    });
}