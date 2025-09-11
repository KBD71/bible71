// 페이지 초기화 및 빌드 로직
// contentData 객체는 이 스크립트를 불러오기 전에
// 각 mcMMDD.html 파일 안에서 먼저 정의되어 있어야 합니다.

class PageBuilder {
    constructor() {
        this.contentData = window.contentData || null;
        this.cache = new Map();
    }

    async initializePage() {
        try {
            if (!this.contentData) {
                throw new Error('contentData가 정의되지 않았습니다.');
            }

            const videoId = await this.getVideoId();
            await this.buildPage(videoId);
        } catch (error) {
            this.handleError(error);
        }
    }

    async getVideoId() {
        const dateStr = this.contentData.date;
        const [month, day] = dateStr.match(/\d+/g).map(s => s.padStart(2, '0'));
        const addressFilePath = `../address/${month}${day}.txt`;
        
        // 캐시 확인
        if (this.cache.has(addressFilePath)) {
            return this.cache.get(addressFilePath);
        }

        const addressResponse = await fetch(addressFilePath);
        if (!addressResponse.ok) {
            throw new Error(`주소 파일을 찾을 수 없습니다: ${addressFilePath}`);
        }
        
        const addressText = await addressResponse.text();
        const mcLine = addressText.split('\n').find(line => line.startsWith('mc:'));
        
        if (!mcLine) {
            throw new Error(`'mc:' 접두사를 가진 주소를 '${addressFilePath}' 파일에서 찾을 수 없습니다.`);
        }
        
        const youtubeUrl = mcLine.substring(3).trim();
        const videoId = this.extractVideoID(youtubeUrl);
        
        if (!videoId) {
            throw new Error(`유튜브 주소에서 비디오 ID를 추출할 수 없습니다: ${youtubeUrl}`);
        }

        // 캐시에 저장
        this.cache.set(addressFilePath, videoId);
        return videoId;
    }

    extractVideoID(url) {
        const patterns = [
            /(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})/,
            /(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})/,
            /(?:https?:\/\/)?youtu\.be\/([a-zA-Z0-9_-]{11})/,
            /(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})/
        ];

        for (const pattern of patterns) {
            const match = url.match(pattern);
            if (match) return match[1];
        }
        
        return null;
    }

    async buildPage(videoId) {
        try {
            const template = await this.loadTemplate();
            const processedTemplate = this.processTemplate(template, videoId);
            this.renderPage(processedTemplate);
        } catch (error) {
            throw new Error(`페이지 빌드 실패: ${error.message}`);
        }
    }

    async loadTemplate() {
        const response = await fetch('../template/mc_layout.html');
        if (!response.ok) {
            throw new Error('템플릿 파일을 로드할 수 없습니다.');
        }
        return await response.text();
    }

    processTemplate(template, videoId) {
        const replacements = {
            '<!-- %%PAGE_TITLE%% -->': `${this.contentData.date} 맥체인 성경읽기`,
            '<!-- %%VIDEO_ID%% -->': videoId,
            '<!-- %%TITLE_SECTION%% -->': this.buildTitleSection(),
            '<!-- %%MAIN_CONTENT%% -->': this.buildMainContent()
        };

        let processedTemplate = template;
        for (const [placeholder, replacement] of Object.entries(replacements)) {
            processedTemplate = processedTemplate.replace(new RegExp(placeholder, 'g'), replacement);
        }

        return processedTemplate;
    }

    buildTitleSection() {
        return `<h1>${this.contentData.date} 맥체인 성경읽기<br><span class="subtitle">${this.contentData.title}</span></h1>`;
    }

    buildMainContent() {
        if (!this.contentData.cards || !Array.isArray(this.contentData.cards)) {
            return '<p>콘텐츠 데이터가 없습니다.</p>';
        }

        return this.contentData.cards.map(card => this.buildCardHtml(card)).join('');
    }

    buildCardHtml(card) {
        const sections = [
            { key: 'overview', title: '개요 (Overview)', tag: 'p' },
            { key: 'svg', title: '시각적 분석 (Visual Analysis)', tag: 'div' },
            { key: 'context', title: '배경지식 및 신학적 통찰 (Context & Theology)', tag: 'p' },
            { key: 'keyVerses', title: '주요 구절 해설 (Key Verse Commentary)', custom: true },
            { key: 'integrationTheme', title: '관통하는 주제 (Overarching Theme)', tag: 'p' },
            { key: 'redemptivePanorama', title: '구속사의 파노라마 (Panorama of Redemptive History)', tag: 'div' },
            { key: 'redemptiveContext', title: '구속사적 맥락 (Redemptive-Historical Context)', tag: 'p' },
            { key: 'analysisTable', title: '주제별 심층 분석표 (Thematic Analysis Table)', tag: 'div' },
            { key: 'application', title: '오늘의 교훈 (Application)', tag: 'p' },
            { key: 'bibleText', title: '성경 본문 (Full Text)', tag: 'div' }
        ];

        let cardHtml = `<section class="chapter-card ${card.cardClass || ''}"><h2>${card.title}</h2>`;

        sections.forEach(section => {
            if (card[section.key]) {
                cardHtml += `<h3>${section.title}</h3>`;
                
                if (section.key === 'keyVerses' && Array.isArray(card.keyVerses)) {
                    card.keyVerses.forEach(kv => {
                        cardHtml += `<div class="commentary">
                            <p><strong>${this.escapeHtml(kv.verse)}</strong> - "${this.escapeHtml(kv.text)}"</p>
                            <p>${this.escapeHtml(kv.commentary)}</p>
                        </div>`;
                    });
                } else {
                    const content = section.key === 'svg' || section.key === 'redemptivePanorama' || 
                                  section.key === 'analysisTable' || section.key === 'bibleText' 
                                  ? card[section.key] 
                                  : this.escapeHtml(card[section.key]);
                    cardHtml += `<${section.tag}>${content}</${section.tag}>`;
                }
            }
        });

        cardHtml += '</section>';
        return cardHtml;
    }

    escapeHtml(text) {
        if (typeof text !== 'string') return text;
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    renderPage(html) {
        document.documentElement.innerHTML = html;
    }

    handleError(error) {
        console.error("페이지 초기화 오류:", error);
        document.body.innerHTML = `
            <div style="padding:20px; text-align:center; font-family:sans-serif;">
                <h2>페이지 로딩 실패</h2>
                <p style="color:red;">${this.escapeHtml(error.message)}</p>
                <p>'address' 폴더에 오늘 날짜의 .txt 파일이 있고, 그 안에 'mc:'로 시작하는 정확한 유튜브 주소가 있는지 확인해주세요.</p>
                <button onclick="location.reload()" style="margin-top:10px; padding:8px 16px;">다시 시도</button>
            </div>`;
    }
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    const pageBuilder = new PageBuilder();
    pageBuilder.initializePage();
});

// 이전 버전과의 호환성을 위한 전역 함수들
window.initializePage = () => {
    const pageBuilder = new PageBuilder();
    return pageBuilder.initializePage();
};

window.extractVideoID = (url) => {
    const pageBuilder = new PageBuilder();
    return pageBuilder.extractVideoID(url);
};
