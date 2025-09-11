// 페이지 초기화 및 빌드 로직

// contentData 객체는 이 스크립트를 불러오기 전에
// 각 mcMMDD.html 파일 안에서 먼저 정의되어 있어야 합니다.

async function initializePage() {
    try {
        const dateStr = contentData.date;
        const [month, day] = dateStr.match(/\d+/g).map(s => s.padStart(2, '0'));
        const addressFilePath = `../address/${month}${day}.txt`;

        const addressResponse = await fetch(addressFilePath);
        if (!addressResponse.ok) throw new Error(`주소 파일을 찾을 수 없습니다: ${addressFilePath}`);
        const addressText = await addressResponse.text();
        
        const mcLine = addressText.split('\n').find(line => line.startsWith('mc:'));
        if (!mcLine) throw new Error(`'mc:' 접두사를 가진 주소를 '${addressFilePath}' 파일에서 찾을 수 없습니다.`);
        
        const youtubeUrl = mcLine.substring(3).trim();
        const videoId = extractVideoID(youtubeUrl);
        if (!videoId) throw new Error(`유튜브 주소에서 비디오 ID를 추출할 수 없습니다: ${youtubeUrl}`);

        // 이제 videoId를 contentData에 넣는 대신, buildPage 함수에 직접 전달합니다.
        await buildPage(videoId);

    } catch (error) {
        console.error("페이지 초기화 오류:", error);
        document.body.innerHTML = `<div style="padding:20px; text-align:center; font-family:sans-serif;">
            <h2>페이지 로딩 실패</h2><p style="color:red;">${error.message}</p>
            <p>'address' 폴더에 오늘 날짜의 .txt 파일이 있고, 그 안에 'mc:'로 시작하는 정확한 유튜브 주소가 있는지 확인해주세요.</p></div>`;
    }
}

function extractVideoID(url) {
    const regex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
}

async function buildPage(videoId) {
    const response = await fetch('../template/mc_layout.html');
    let template = await response.text();

    template = template.replace(//g, `${contentData.date} 맥체인 성경읽기`);
    template = template.replace(//g, videoId);

    const titleHtml = `<h1>${contentData.date} 맥체인 성경읽기<br><span class="subtitle">${contentData.mainTitle}</span></h1><p class="intro-passage">${contentData.passages}</p>`;
    template = template.replace('', titleHtml);

    let mainContentHtml = '';
    contentData.cards.forEach(card => {
        let cardHtml = `<section class="chapter-card ${card.cardClass}"><h2>${card.title}</h2>`;
        if (card.overview) cardHtml += `<h3>개요 (Overview)</h3><p>${card.overview}</p>`;
        if (card.svg) cardHtml += `<h3>시각적 분석 (Visual Analysis)</h3>${card.svg}`;
        if (card.context) cardHtml += `<h3>배경지식 및 신학적 통찰 (Context & Theology)</h3><p>${card.context}</p>`;
        if (card.keyVerses && card.keyVerses.length > 0) {
            cardHtml += `<h3>주요 구절 해설 (Key Verse Commentary)</h3>`;
            card.keyVerses.forEach(kv => {
                cardHtml += `<div class="commentary"><p><strong>${kv.verse}</strong> - "${kv.text}"</p><p>${kv.commentary}</p></div>`;
            });
        }
        if (card.integrationTheme) cardHtml += `<h3>관통하는 주제 (Overarching Theme)</h3><p>${card.integrationTheme}</p>`;
        if (card.redemptivePanorama) cardHtml += `<h3>구속사의 파노라마 (Panorama of Redemptive History)</h3>${card.redemptivePanorama}`;
        if (card.redemptiveContext) cardHtml += `<h3>구속사적 맥락 (Redemptive-Historical Context)</h3><p>${card.redemptiveContext}</p>`;
        if (card.analysisTable) cardHtml += `<h3>주제별 심층 분석표 (Thematic Analysis Table)</h3>${card.analysisTable}`;
        if (card.application) cardHtml += `<h3>오늘의 교훈 (Application)</h3><p>${card.application}</p>`;
        if (card.bibleText) cardHtml += `<h3>성경 본문 (Full Text)</h3>${card.bibleText}`;
        cardHtml += `</section>`;
        mainContentHtml += cardHtml;
    });
    template = template.replace('', mainContentHtml);

    document.documentElement.innerHTML = template;
}

// 페이지 로드 시 초기화 함수 실행
initializePage();
