// Anthropic AI SDK를 가져옵니다.
const Anthropic = require('@anthropic-ai/sdk');

// Vercel 환경 변수에서 API 키를 안전하게 불러옵니다.
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Vercel 서버리스 함수의 기본 핸들러입니다.
module.exports = async (req, res) => {
  // POST 요청이 아니면 에러를 반환합니다.
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    // 클라이언트로부터 받은 메시지를 추출합니다.
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // AI에게 보낼 메시지를 생성합니다.
    const msg = await anthropic.messages.create({
      // ✍️ TODO: 요청하신 모델명으로 변경하세요. 현재는 안정적인 Sonnet 3.5 모델을 사용합니다.
      model: "claude-3-5-sonnet-20240620", 
      max_tokens: 1024,
      system: "당신은 존 칼빈의 신학적 전통을 따르는 개혁신학 성경 연구 도우미입니다. 사용자의 질문에 대해 성경 구절을 인용하고 신학적 개념을 명확히 하여, 친절하고 이해하기 쉽게 답변해주세요.",
      messages: [{ role: 'user', content: message }],
    });

    // AI의 답변을 클라이언트에 전송합니다.
    res.status(200).json({ reply: msg.content[0].text });

  } catch (error) {
    console.error('Error calling Anthropic API:', error);
    res.status(500).json({ error: 'AI 응답을 가져오는 중 오류가 발생했습니다.' });
  }
};
