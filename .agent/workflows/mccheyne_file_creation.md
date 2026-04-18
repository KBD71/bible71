---
description: how to create a new McCheyne daily reading file
---

This workflow ensures that new McCheyne reading files are compatible with the 5.0 audio playback, navigation, and TTS system.

### Steps to Create a New File

1.  **Use the AI Prompt**
    Use the definitive prompt saved in the artifacts to generate the HTML content via ChatGPT/Claude.
    The prompt contains exact boilerplate code that must not be modified.

2.  **Verify Critical Structure (Checklist)**
    Before committing, check these items:

    - [ ] `<link rel="stylesheet" href="style.css">` present in `<head>`
    - [ ] `.listen-audio-btn { display: none !important; }` in `<style>` block
    - [ ] Tab IDs are exactly: `content-overview`, `content-hebrew`, `content-book1`~`content-book4`, `content-integration`
    - [ ] No `style="display:none;"` on any `tab-content` div
    - [ ] All `data-path` URLs start with `https://kbd71.github.io/bible71/bible_html/` (never external sites)
    - [ ] `data-path` URLs follow pattern: `OT/OT_NN_CODE_CH.html` or `NT/NT_NN_CODE_CH.html`
    - [ ] No markdown link syntax `[text](url)` in `data-path` values
    - [ ] Audio `data-key` has NO zero padding (e.g., `LEV_23` not `LEV_023`)
    - [ ] All `listen-audio-btn` have both `data-key` and `data-title`
    - [ ] All `view-text-btn` have both `data-path` and `data-title`
    - [ ] Buttons wrapped in `<div class="button-group">`
    - [ ] Cards use `<article class="chapter-card card-bookN"><div class="card-content">` structure
    - [ ] `id="text-modal"` modal overlay present
    - [ ] `id="floating-nav"` with `id="current-tab-info"` present
    - [ ] `id="player-container"` present
    - [ ] `id="audio-player"` with `id="play-pause-btn"` and `id="close-player-btn"` present
    - [ ] `<script src="script.js"></script>` present after audio-player div
    - [ ] `playOriginalAudio` TTS function script present after script.js
    - [ ] No Korean characters mixed into TTS onclick text (e.g., `λόγος` not `λό고스`)
    - [ ] No `[cite: N]` artifacts in text

3.  **Content Quality Check**
    - [ ] Hebrew tab has: alphabet guide, ALL words of verse analyzed (not just 2-3), full sentence with word-by-word gloss, theology
    - [ ] Each book tab has 3 `<h4>` sections: 역사적 문맥, 구속사적 의미, 개혁주의 적용
    - [ ] Each `<h4>` section has at least 4-5 sentences
    - [ ] Integration tab has 3+ paragraphs with overarching Reformed theme

4.  **Common data-path Examples**
    - 레위기 23장: `https://kbd71.github.io/bible71/bible_html/OT/OT_03_LEV_23.html`
    - 시편 30편: `https://kbd71.github.io/bible71/bible_html/OT/OT_19_PSA_30.html`
    - 전도서 6장: `https://kbd71.github.io/bible71/bible_html/OT/OT_21_ECC_06.html`
    - 디모데후서 2장: `https://kbd71.github.io/bible71/bible_html/NT/NT_55_2TI_02.html`
    - 디모데전서 1장: `https://kbd71.github.io/bible71/bible_html/NT/NT_54_1TI_01.html`
    - 요한복음 15장: `https://kbd71.github.io/bible71/bible_html/NT/NT_43_JOH_15.html`

5.  **Save and Deploy**
    Save the verified file as `mccheyne/mcMMDD.html`, then `git add`, `git commit`, and `git push`.
