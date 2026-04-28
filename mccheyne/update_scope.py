import os
import re

book_map = {
    '창세기': 'OT_01_GEN', '출애굽기': 'OT_02_EXO', '레위기': 'OT_03_LEV', '민수기': 'OT_04_NUM', '신명기': 'OT_05_DEU',
    '여호수아': 'OT_06_JOS', '사사기': 'OT_07_JDG', '룻기': 'OT_08_RUT', '사무엘상': 'OT_09_1SA', '사무엘하': 'OT_10_2SA',
    '열왕기상': 'OT_11_1KI', '열왕기하': 'OT_12_2KI', '역대상': 'OT_13_1CH', '역대하': 'OT_14_2CH', '에스라': 'OT_15_EZR',
    '느헤미야': 'OT_16_NEH', '에스더': 'OT_17_EST', '욥기': 'OT_18_JOB', '시편': 'OT_19_PSA', '잠언': 'OT_20_PRO',
    '전도서': 'OT_21_ECC', '아가': 'OT_22_SNG', '이사야': 'OT_23_ISA', '예레미야': 'OT_24_JER', '예레미야애가': 'OT_25_LAM',
    '에스겔': 'OT_26_EZE', '다니엘': 'OT_27_DAN', '호세아': 'OT_28_HOS', '요엘': 'OT_29_JOE', '아모스': 'OT_30_AMO',
    '오바댜': 'OT_31_OBA', '요나': 'OT_32_JON', '미가': 'OT_33_MIC', '나훔': 'OT_34_NAH', '하박국': 'OT_35_HAB',
    '스바냐': 'OT_36_ZEP', '학개': 'OT_37_HAG', '스가랴': 'OT_38_ZEC', '말라기': 'OT_39_MAL',
    
    '마태복음': 'NT_01_MAT', '마가복음': 'NT_02_MRK', '누가복음': 'NT_03_LUK', '요한복음': 'NT_04_JHN', '사도행전': 'NT_05_ACT',
    '로마서': 'NT_06_ROM', '고린도전서': 'NT_07_1CO', '고린도후서': 'NT_08_2CO', '갈라디아서': 'NT_09_GAL', '에베소서': 'NT_10_EPH',
    '빌립보서': 'NT_11_PHP', '골로새서': 'NT_12_COL', '데살로니가전서': 'NT_13_1TH', '데살로니가후서': 'NT_14_2TH',
    '디모데전서': 'NT_15_1TI', '디모데후서': 'NT_16_2TI', '디도서': 'NT_17_TIT', '빌레몬서': 'NT_18_PHM', '히브리서': 'NT_19_HEB',
    '야고보서': 'NT_20_JAS', '베드로전서': 'NT_21_1PE', '베드로후서': 'NT_22_2PE', '요한1서': 'NT_23_1JO', '요한2서': 'NT_24_2JO',
    '요한3서': 'NT_25_3JO', '유다서': 'NT_26_JUD', '요한계시록': 'NT_27_REV'
}

def parse_xhtml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'<ul class="reading-list">(.*?)</ul>', content, re.DOTALL)
    if not match: return []
    items = re.findall(r'<li><a href="#reading\d+">([^<]+)</a></li>', match.group(1))
    return items

def test():
    items = parse_xhtml('c:/Users/matht/OneDrive/Desktop/bible71/mccheyne/temp_epub/EPUB/day_0601.xhtml')
    print("Parsed items:", items)

if __name__ == '__main__':
    test()
