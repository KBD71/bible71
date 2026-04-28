$bookMap = @{
    '창세기'=@('OT_01_GEN','GEN'); '출애굽기'=@('OT_02_EXO','EXO'); '레위기'=@('OT_03_LEV','LEV'); '민수기'=@('OT_04_NUM','NUM'); '신명기'=@('OT_05_DEU','DEU');
    '여호수아'=@('OT_06_JOS','JOS'); '사사기'=@('OT_07_JDG','JDG'); '룻기'=@('OT_08_RUT','RUT'); '사무엘상'=@('OT_09_1SA','1SA'); '사무엘하'=@('OT_10_2SA','2SA');
    '열왕기상'=@('OT_11_1KI','1KI'); '열왕기하'=@('OT_12_2KI','2KI'); '역대상'=@('OT_13_1CH','1CH'); '역대하'=@('OT_14_2CH','2CH'); '에스라'=@('OT_15_EZR','EZR');
    '느헤미야'=@('OT_16_NEH','NEH'); '에스더'=@('OT_17_EST','EST'); '욥기'=@('OT_18_JOB','JOB'); '시편'=@('OT_19_PSA','PSA'); '잠언'=@('OT_20_PRO','PRO');
    '전도서'=@('OT_21_ECC','ECC'); '아가'=@('OT_22_SNG','SNG'); '이사야'=@('OT_23_ISA','ISA'); '예레미야'=@('OT_24_JER','JER'); '예레미야애가'=@('OT_25_LAM','LAM');
    '에스겔'=@('OT_26_EZE','EZE'); '다니엘'=@('OT_27_DAN','DAN'); '호세아'=@('OT_28_HOS','HOS'); '요엘'=@('OT_29_JOE','JOE'); '아모스'=@('OT_30_AMO','AMO');
    '오바댜'=@('OT_31_OBA','OBA'); '요나'=@('OT_32_JON','JON'); '미가'=@('OT_33_MIC','MIC'); '나훔'=@('OT_34_NAH','NAH'); '하박국'=@('OT_35_HAB','HAB');
    '스바냐'=@('OT_36_ZEP','ZEP'); '학개'=@('OT_37_HAG','HAG'); '스가랴'=@('OT_38_ZEC','ZEC'); '말라기'=@('OT_39_MAL','MAL');
    '마태복음'=@('NT_01_MAT','MAT'); '마가복음'=@('NT_02_MAR','MRK'); '누가복음'=@('NT_03_LUK','LUK'); '요한복음'=@('NT_04_JOH','JHN'); '사도행전'=@('NT_05_ACT','ACT');
    '로마서'=@('NT_06_ROM','ROM'); '고린도전서'=@('NT_07_1CO','1CO'); '고린도후서'=@('NT_08_2CO','2CO'); '갈라디아서'=@('NT_09_GAL','GAL'); '에베소서'=@('NT_10_EPH','EPH');
    '빌립보서'=@('NT_11_PHI','PHP'); '골로새서'=@('NT_12_COL','COL'); '데살로니가전서'=@('NT_13_1TH','1TH'); '데살로니가후서'=@('NT_14_2TH','2TH');
    '디모데전서'=@('NT_15_1TI','1TI'); '디모데후서'=@('NT_16_2TI','2TI'); '디도서'=@('NT_17_TIT','TIT'); '빌레몬서'=@('NT_18_PHM','PHM'); '히브리서'=@('NT_19_HEB','HEB');
    '야고보서'=@('NT_20_JAM','JAS'); '베드로전서'=@('NT_21_1PE','1PE'); '베드로후서'=@('NT_22_2PE','2PE'); '요한1서'=@('NT_23_1JO','1JO'); '요한2서'=@('NT_24_2JO','2JO');
    '요한3서'=@('NT_25_3JO','3JO'); '유다서'=@('NT_26_JUD','JUD'); '요한계시록'=@('NT_27_REV','REV')
}

$dates = @()
for ($i=24; $i -le 31; $i++) { $dates += "05{0:D2}" -f $i }
for ($i=1; $i -le 30; $i++) { $dates += "06{0:D2}" -f $i }

foreach ($d in $dates) {
    $epubPath = "c:\Users\matht\OneDrive\Desktop\bible71\mccheyne\temp_epub\EPUB\day_$d.xhtml"
    if (-not (Test-Path $epubPath)) { continue }
    $content = Get-Content $epubPath -Raw
    $pattern = '(?s)<ul class="reading-list">(.*?)</ul>'
    if ($content -match $pattern) {
        $ul = $matches[1]
        $items = [regex]::Matches($ul, '<li><a href="#reading\d+">([^<]+)</a></li>')
        $readings = @()
        foreach ($item in $items) {
            $readings += $item.Groups[1].Value
        }
        Write-Host "$d : $($readings -join ', ')"
    }
}
