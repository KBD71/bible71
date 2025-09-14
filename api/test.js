// 간단한 테스트 API 함수
module.exports = (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    res.json({
        message: 'API 함수가 작동합니다!',
        timestamp: new Date().toISOString(),
        method: req.method,
        url: req.url
    });
};