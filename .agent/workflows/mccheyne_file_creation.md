---
description: how to create a new McCheyne daily reading file
---

This workflow ensures that new McCheyne reading files are compatible with the 5.0 audio playback and navigation system.

### Steps to Create a New File

1.  **Copy the Template**
    Copy `mccheyne/template_mccheyne.html` to a new file named `mcMMDD.html` (e.g., `mc0406.html`).

2.  **Fill in the Placeholders**
    Replace all `{{...}}` placeholders with the actual content for that day:
    - **Dates**: Update `<title>`, `<h1>`, and `<h3>`.
    - **Tab Labels**: Update the text in `<nav class="tabs">`.
    - **Event Handlers**: Ensure `onclick="switchTab(N)"` matches the tab index (0 for Overview, 1-4 for Bible books, 5 for Integration).
    - **Bible Content**: Fill in the 소주제, 핵심질문, 상세개요, and 신학해설.
    - **Audio Keys**: Set `data-key` in the `.listen-audio-btn` to the correct Bible key (e.g., `LEV_8`, `PSA_9`). These keys must match the mapping in `mcbible.txt`.
    - **Text Paths**: Set `data-path` in the `.view-text-btn` to the full URL of the Bible passage HTML.

3.  **Verify Vital Components**
    Ensure the following IDs and classes are present at the bottom of the file (should be included in the template):
    - `id="text-modal"` (Modal overlay)
    - `id="floating-nav"` (Bottom-left ◀ ▶ buttons)
    - `id="player-container"` (YouTube container)
    - `id="audio-player"` (Global player UI)
    - `<script src="script.js"></script>`

4.  **Test the File**
    - Open the file in a browser.
    - Verify that clicking a Bible tab triggers the audio player (shows "재생 대기 중..." or the title).
    - Verify that "본문 보기" opens the modal correctly.
    - Verify that the floating navigation (◀ ▶) switches tabs.
