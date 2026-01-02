import json
import re

# JSON content from the URL
json_data = """
{"0101":{"family":["Genesis 1","Matthew 1"],"secret":["Ezra 1","Acts 1"]},"0102":{"family":["Genesis 2","Matthew 2"],"secret":["Ezra 2","Acts 2"]},"0103":{"family":["Genesis 3","Matthew 3"],"secret":["Ezra 3","Acts 3"]},"0104":{"family":["Genesis 4","Matthew 4"],"secret":["Ezra 4","Acts  4"]},"0105":{"family":["Genesis 5","Matthew 5"],"secret":["Ezra 5","Acts 5"]},"0106":{"family":["Genesis 6","Matthew 6"],"secret":["Ezra 6","Acts 6"]},"0107":{"family":["Genesis 7","Matthew 7"],"secret":["Ezra 7","Acts 7"]},"0108":{"family":["Genesis 8","Matthew 8"],"secret":["Ezra 8","Acts 8"]},"0109":{"family":["Genesis 9-10","Matthew 9"],"secret":["Ezra 9","Acts 9"]},"0110":{"family":["Genesis 11","Matthew 10"],"secret":["Ezra 10","Acts 10"]},"0111":{"family":["Genesis 12","Matthew 11"],"secret":["Nehemiah 1","Acts 11"]},"0112":{"family":["Genesis 13","Matthew 12"],"secret":["Nehemiah 2","Acts 12"]},"0113":{"family":["Genesis 14","Matthew 13"],"secret":["Nehemiah 3","Acts 13"]},"0114":{"family":["Genesis 15","Matthew 14"],"secret":["Nehemiah 4","Acts 14"]},"0115":{"family":["Genesis 16","Matthew 15"],"secret":["Nehemiah 5","Acts 15"]},"0116":{"family":["Genesis 17","Matthew 16"],"secret":["Nehemiah 6","Acts 16"]},"0117":{"family":["Genesis 18","Matthew 17"],"secret":["Nehemiah 7","Acts 17"]},"0118":{"family":["Genesis 19","Matthew 18"],"secret":["Nehemiah 8","Acts 18"]},"0119":{"family":["Genesis 20","Matthew 19"],"secret":["Nehemiah 9","Acts 19"]},"0120":{"family":["Genesis 21","Matthew 20"],"secret":["Nehemiah 10","Acts 20"]},"0121":{"family":["Genesis 22","Matthew 21"],"secret":["Nehemiah 11","Acts 21"]},"0122":{"family":["Genesis 23","Matthew 22"],"secret":["Nehemiah 12","Acts 22"]},"0123":{"family":["Genesis 24","Matthew 23"],"secret":["Nehemiah 13","Acts 23"]},"0124":{"family":["Genesis 25","Matthew 24"],"secret":["Esther 1","Acts 24"]},"0125":{"family":["Genesis 26","Matthew 25"],"secret":["Esther 2","Acts 25"]},"0126":{"family":["Genesis 27","Matthew 26"],"secret":["Esther 3","Acts 26"]},"0127":{"family":["Genesis 28","Matthew 27"],"secret":["Esther 4","Acts 27"]},"0128":{"family":["Genesis 29","Matthew 28"],"secret":["Esther 5","Acts 28"]},"0129":{"family":["Genesis 30","Mark 1"],"secret":["Esther 6","Romans 1"]},"0130":{"family":["Genesis 31","Mark 2"],"secret":["Esther 7","Romans 2"]},"0131":{"family":["Genesis 32","Mark 3"],"secret":["Esther 8","Romans 3"]},"0201":{"family":["Genesis 33","Mark 4"],"secret":["Esther 9-10","Romans 4"]},"0202":{"family":["Genesis 34","Mark 5"],"secret":["Job 1","Romans 5"]},"0203":{"family":["Genesis 35-36","Mark 6"],"secret":["Job 2","Romans 6"]},"0204":{"family":["Genesis 37","Mark 7"],"secret":["Job 3","Romans 7"]},"0205":{"family":["Genesis 38","Mark 8"],"secret":["Job 4","Romans 8"]},"0206":{"family":["Genesis 39","Mark 9"],"secret":["Job 5","Romans 9"]},"0207":{"family":["Genesis 40","Mark 10"],"secret":["Job 6","Romans 10"]},"0208":{"family":["Genesis 41","Mark 11"],"secret":["Job 7","Romans 11"]},"0209":{"family":["Genesis 42","Mark 12"],"secret":["Job 8","Romans 12"]},"0210":{"family":["Genesis 43","Mark 13"],"secret":["Job 9","Romans 13"]},"0211":{"family":["Genesis 44","Mark 14"],"secret":["Job 10","Romans 14"]},"0212":{"family":["Genesis 45","Mark 15"],"secret":["Job 11","Romans 15"]},"0213":{"family":["Genesis 46","Mark 16"],"secret":["Job 12","Romans 16"]},"0214":{"family":["Genesis 47","Luke 1:1-38"],"secret":["Job 13","1 Corinthians 1"]},"0215":{"family":["Genesis 48","Luke 1:39ff"],"secret":["Job 14","1 Corinthians 2"]},"0216":{"family":["Genesis 49","Luke 2"],"secret":["Job 15","1 Corinthians 3"]},"0217":{"family":["Genesis 50","Luke 3"],"secret":["Job 16-17","1 Corinthians 4"]},"0218":{"family":["Exodus 1","Luke 4"],"secret":["Job 18","1 Corinthians 5"]},"0219":{"family":["Exodus 2","Luke 5"],"secret":["Job 19","1 Corinthians 6"]},"0220":{"family":["Exodus 3","Luke 6"],"secret":["Job 20","1 Corinthians 7"]},"0221":{"family":["Exodus 4","Luke 7"],"secret":["Job 21","1 Corinthians 8"]},"0222":{"family":["Exodus 5","Luke 8"],"secret":["Job 22","1 Corinthians 9"]},"0223":{"family":["Exodus 6","Luke 9"],"secret":["Job 23","1 Corinthians 10"]},"0224":{"family":["Exodus 7","Luke 10"],"secret":["Job 24","1 Corinthians 11"]},"0225":{"family":["Exodus 8","Luke 11"],"secret":["Job 25-26","1 Corinthians 12"]},"0226":{"family":["Exodus 9","Luke 12"],"secret":["Job 27","1 Corinthians 13"]},"0227":{"family":["Exodus 10","Luke 13"],"secret":["Job 28","1 Corinthians 14"]},"0228":{"family":["Exodus 11-12:21","Luke 14"],"secret":["Job 29","1 Corinthians 15"]},"0301":{"family":["Exodus 12:22ff","Luke 15"],"secret":["Job 30","1 Corinthians 16"]},"0302":{"family":["Exodus 13","Luke 16"],"secret":["Job 31","2 Corinthians 1"]},"0303":{"family":["Exodus 14","Luke 17"],"secret":["Job 32","2 Corinthians 2"]},"0304":{"family":["Exodus 15","Luke 18"],"secret":["Job 33","2 Corinthians 3"]},"0305":{"family":["Exodus 16","Luke 19"],"secret":["Job 34","2 Corinthians 4"]},"0306":{"family":["Exodus 17","Luke 20"],"secret":["Job 35","2 Corinthians 5"]},"0307":{"family":["Exodus 18","Luke 21"],"secret":["Job 36","2 Corinthians 6"]},"0308":{"family":["Exodus 19","Luke 22"],"secret":["Job 37","2 Corinthians 7"]},"0309":{"family":["Exodus 20","Luke 23"],"secret":["Job 38","2 Corinthians 8"]},"0310":{"family":["Exodus 21","Luke 24"],"secret":["Job 39","2 Corinthians 9"]},"0311":{"family":["Exodus 22","John 1"],"secret":["Job 40","2 Corinthians 10"]},"0312":{"family":["Exodus 23","John 2"],"secret":["Job 41","2 Corinthians 11"]},"0313":{"family":["Exodus 24","John 3"],"secret":["Job 42","2 Corinthians 12"]},"0314":{"family":["Exodus 25","John 4"],"secret":["Proverbs 1","2 Corinthians 13"]},"0315":{"family":["Exodus 26","John 5"],"secret":["Proverbs 2","Galatians 1"]},"0316":{"family":["Exodus 27","John 6"],"secret":["Proverbs 3","Galatians 2"]},"0317":{"family":["Exodus 28","John 7"],"secret":["Proverbs 4","Galatians 3"]},"0318":{"family":["Exodus 29","John 8"],"secret":["Proverbs 5","Galatians 4"]},"0319":{"family":["Exodus 30","John 9"],"secret":["Proverbs 6","Galatians 5"]},"0320":{"family":["Exodus 31","John 10"],"secret":["Proverbs 7","Galatians 6"]},"0321":{"family":["Exodus 32","John 11"],"secret":["Proverbs 8","Ephesians 1"]},"0322":{"family":["Exodus 33","John 12"],"secret":["Proverbs 9","Ephesians 2"]},"0323":{"family":["Exodus 34","John 13"],"secret":["Proverbs 10","Ephesians 3"]},"0324":{"family":["Exodus 35","John 14"],"secret":["Proverbs 11","Ephesians 4"]},"0325":{"family":["Exodus 36","John 15"],"secret":["Proverbs 12","Ephesians 5"]},"0326":{"family":["Exodus 37","John 16"],"secret":["Proverbs 13","Ephesians 6"]},"0327":{"family":["Exodus 38","John 17"],"secret":["Proverbs 14","Philippians 1"]},"0328":{"family":["Exodus 39","John 18"],"secret":["Proverbs 15","Philippians 2"]},"0329":{"family":["Exodus 40","John 19"],"secret":["Proverbs 16","Philippians 3"]},"0330":{"family":["Leviticus 1","John 20"],"secret":["Proverbs 17","Philippians 4"]},"0331":{"family":["Leviticus 2-3","John 21"],"secret":["Proverbs 18","Colossians 1"]},"0401":{"family":["Leviticus 4","Psalms 1-2"],"secret":["Proverbs 19","Colossians 2"]},"0402":{"family":["Leviticus 5","Psalms 3-4"],"secret":["Proverbs 20","Colossians 3"]},"0403":{"family":["Leviticus 6","Psalms 5-6"],"secret":["Proverbs 21","Colossians 4"]},"0404":{"family":["Leviticus 7","Psalms 7-8"],"secret":["Proverbs 22","1 Thessalonians 1"]},"0405":{"family":["Leviticus 8","Psalms 9"],"secret":["Proverbs 23","1 Thessalonians 2"]},"0406":{"family":["Leviticus 9","Psalms 10"],"secret":["Proverbs 24","1 Thessalonians 3"]},"0407":{"family":["Leviticus 10","Psalms 11-12"],"secret":["Proverbs 25","1 Thessalonians 4"]},"0408":{"family":["Leviticus 11-12","Psalms 13-14"],"secret":["Proverbs 26","1 Thessalonians 5"]},"0409":{"family":["Leviticus 13","Psalms 15-16"],"secret":["Proverbs 27","2 Thessalonians 1"]},"0410":{"family":["Leviticus 14","Psalms 17"],"secret":["Proverbs 28","2 Thessalonians 2"]},"0411":{"family":["Leviticus 15","Psalms 18"],"secret":["Proverbs 29","2 Thessalonians 3"]},"0412":{"family":["Leviticus 16","Psalms 19"],"secret":["Proverbs 30","1 Timothy 1"]},"0413":{"family":["Leviticus 17","Psalms 20-21"],"secret":["Proverbs 31","1 Timothy 2"]},"0414":{"family":["Leviticus 18","Psalms 22"],"secret":["Ecclesiastes 1","1 Timothy 3"]},"0415":{"family":["Leviticus 19","Psalms 23-24"],"secret":["Ecclesiastes 2","1 Timothy 4"]},"0416":{"family":["Leviticus 20","Psalms 25"],"secret":["Ecclesiastes 3","1 Timothy 5"]},"0417":{"family":["Leviticus 21","Psalms 26-27"],"secret":["Ecclesiastes 4","1 Timothy 6"]},"0418":{"family":["Leviticus 22","Psalms 28-29"],"secret":["Ecclesiastes 5","2 Timothy 1"]},"0419":{"family":["Leviticus 23","Psalms 30"],"secret":["Ecclesiastes 6","2 Timothy 2"]},"0420":{"family":["Leviticus 24","Psalms 31"],"secret":["Ecclesiastes 7","2 Timothy 3"]},"0421":{"family":["Leviticus 25","Psalms 32"],"secret":["Ecclesiastes 8","2 Timothy 4"]},"0422":{"family":["Leviticus 26","Psalms 33"],"secret":["Ecclesiastes 9","Titus 1"]},"0423":{"family":["Leviticus 27","Psalms 34"],"secret":["Ecclesiastes 10","Titus 2"]},"0424":{"family":["Numbers 1","Psalms 35"],"secret":["Ecclesiastes 11","Titus 3"]},"0425":{"family":["Numbers 2","Psalms 36"],"secret":["Ecclesiastes 12","Philemon 1"]},"0426":{"family":["Numbers 3","Psalms 37"],"secret":["Song of Songs 1","Hebrews 1"]},"0427":{"family":["Numbers 4","Psalms 38"],"secret":["Song of Songs 2","Hebrews 2"]},"0428":{"family":["Numbers 5","Psalms 39"],"secret":["Song of Songs 3","Hebrews 3"]},"0429":{"family":["Numbers 6","Psalms 40-41"],"secret":["Song of Songs 4","Hebrews 4"]},"0430":{"family":["Numbers 7","Psalms 42-43"],"secret":["Song of Songs 5","Hebrews 5"]},"0501":{"family":["Numbers 8","Psalms 44"],"secret":["Song of Songs 6","Hebrews 6"]},"0502":{"family":["Numbers 9","Psalms 45"],"secret":["Song of Songs 7","Hebrews 7"]},"0503":{"family":["Numbers 10","Psalms 46-47"],"secret":["Song of Songs 8","Hebrews 8"]},"0504":{"family":["Numbers 11","Psalms 48"],"secret":["Isaiah 1","Hebrews 9"]},"0505":{"family":["Numbers 12-13","Psalms 49"],"secret":["Isaiah 2","Hebrews 10"]},"0506":{"family":["Numbers 14","Psalms 50"],"secret":["Isaiah 3-4","Hebrews 11"]},"0507":{"family":["Numbers 15","Psalms 51"],"secret":["Isaiah 5","Hebrews 12"]},"0508":{"family":["Numbers 16","Psalms 52-54"],"secret":["Isaiah 6","Hebrews 13"]},"0509":{"family":["Numbers 17-18","Psalms 55"],"secret":["Isaiah 7","James 1"]},"0510":{"family":["Numbers 19","Psalms 56-57"],"secret":["Isaiah 8-9:7","James 2"]},"0511":{"family":["Numbers 20","Psalms 58-59"],"secret":["Isaiah 9:8-10:4","James 3"]},"0512":{"family":["Numbers 21","Psalms 60-61"],"secret":["Isaiah 10:5ff","James 4"]},"0513":{"family":["Numbers 22","Psalms 62-63"],"secret":["Isaiah 11-12","James 5"]},"0514":{"family":["Numbers 23","Psalms 64-65"],"secret":["Isaiah 13","1 Peter 1"]},"0515":{"family":["Numbers 24","Psalms 66-67"],"secret":["Isaiah 14","1 Peter 2"]},"0516":{"family":["Numbers 25","Psalms 68"],"secret":["Isaiah 15","1 Peter 3"]},"0517":{"family":["Numbers 26","Psalms 69"],"secret":["Isaiah 16","1 Peter 4"]},"0518":{"family":["Numbers 27","Psalms 70-71"],"secret":["Isaiah 17-18","1 Peter 5"]},"0519":{"family":["Numbers 28","Psalms 72"],"secret":["Isaiah 19-20","2 Peter 1"]},"0520":{"family":["Numbers 29","Psalms 73"],"secret":["Isaiah 21","2 Peter 2"]},"0521":{"family":["Numbers 30","Psalms 74"],"secret":["Isaiah 22","2 Peter 3"]},"0522":{"family":["Numbers 31","Psalms 75-76"],"secret":["Isaiah 23","1 John 1"]},"0523":{"family":["Numbers 32","Psalms 77"],"secret":["Isaiah 24","1 John 2"]},"0524":{"family":["Numbers 33","Psalms 78:1-37"],"secret":["Isaiah 25","1 John 3"]},"0525":{"family":["Numbers 34","Psalms 78:38ff"],"secret":["Isaiah 26","1 John 4"]},"0526":{"family":["Numbers 35","Psalms 79"],"secret":["Isaiah 27","1 John 5"]},"0527":{"family":["Numbers 36","Psalms 80"],"secret":["Isaiah 28","2 John 1"]},"0528":{"family":["Deuteronomy 1","Psalms 81-82"],"secret":["Isaiah 29","3 John 1"]},"0529":{"family":["Deuteronomy 2","Psalms 83-84"],"secret":["Isaiah 30","Jude 1"]},"0530":{"family":["Deuteronomy 3","Psalms 85"],"secret":["Isaiah 31","Revelation 1"]},"0531":{"family":["Deuteronomy 4","Psalms 86-87"],"secret":["Isaiah 32","Revelation 2"]},"0601":{"family":["Deuteronomy 5","Psalms 88"],"secret":["Isaiah 33","Revelation 3"]},"0602":{"family":["Deuteronomy 6","Psalms 89"],"secret":["Isaiah 34","Revelation 4"]},"0603":{"family":["Deuteronomy 7","Psalms 90"],"secret":["Isaiah 35","Revelation 5"]},"0604":{"family":["Deuteronomy 8","Psalms 91"],"secret":["Isaiah 36","Revelation 6"]},"0605":{"family":["Deuteronomy 9","Psalms 92-93"],"secret":["Isaiah 37","Revelation 7"]},"0606":{"family":["Deuteronomy 10","Psalms 94"],"secret":["Isaiah 38","Revelation 8"]},"0607":{"family":["Deuteronomy 11","Psalms 95-96"],"secret":["Isaiah 39","Revelation 9"]},"0608":{"family":["Deuteronomy 12","Psalms 97-98"],"secret":["Isaiah 40","Revelation 10"]},"0609":{"family":["Deuteronomy 13-14","Psalms 99-101"],"secret":["Isaiah 41","Revelation 11"]},"0610":{"family":["Deuteronomy 15","Psalms 102"],"secret":["Isaiah 42","Revelation 12"]},"0611":{"family":["Deuteronomy 16","Psalms 103"],"secret":["Isaiah 43","Revelation 13"]},"0612":{"family":["Deuteronomy 17","Psalms 104"],"secret":["Isaiah 44","Revelation 14"]},"0613":{"family":["Deuteronomy 18","Psalms 105"],"secret":["Isaiah 45","Revelation 15"]},"0614":{"family":["Deuteronomy 19","Psalms 106"],"secret":["Isaiah 46","Revelation 16"]},"0615":{"family":["Deuteronomy 20","Psalms 107"],"secret":["Isaiah 47","Revelation 17"]},"0616":{"family":["Deuteronomy 21","Psalms 108-109"],"secret":["Isaiah 48","Revelation 18"]},"0617":{"family":["Deuteronomy 22","Psalms 110-111"],"secret":["Isaiah 49","Revelation 19"]},"0618":{"family":["Deuteronomy 23","Psalms 112-113"],"secret":["Isaiah 50","Revelation 20"]},"0619":{"family":["Deuteronomy 24","Psalms 114-115"],"secret":["Isaiah 51","Revelation 21"]},"0620":{"family":["Deuteronomy 25","Psalms 116"],"secret":["Isaiah 52","Revelation 22"]},"0621":{"family":["Deuteronomy 26","Psalms 117-118"],"secret":["Isaiah 53","Matthew 1"]},"0622":{"family":["Deuteronomy 27-28:19","Psalms 119:1-24"],"secret":["Isaiah 54","Matthew 2"]},"0623":{"family":["Deuteronomy 28:20ff","Psalms 119:25-48"],"secret":["Isaiah 55","Matthew 3"]},"0624":{"family":["Deuteronomy 29","Psalms 119:49-72"],"secret":["Isaiah 56","Matthew 4"]},"0625":{"family":["Deuteronomy 30","Psalms 119:73-96"],"secret":["Isaiah 57","Matthew 5"]},"0626":{"family":["Deuteronomy 31","Psalms 119:97-120"],"secret":["Isaiah 58","Matthew 6"]},"0627":{"family":["Deuteronomy 32","Psalms 119:121-144"],"secret":["Isaiah 59","Matthew 7"]},"0628":{"family":["Deuteronomy 33-34","Psalms 119:145-176"],"secret":["Isaiah 60","Matthew 8"]},"0629":{"family":["Joshua 1","Psalms 120-122"],"secret":["Isaiah 61","Matthew 9"]},"0630":{"family":["Joshua 2","Psalms 123-125"],"secret":["Isaiah 62","Matthew 10"]},"0701":{"family":["Joshua 3","Psalms 126-128"],"secret":["Isaiah 63","Matthew 11"]},"0702":{"family":["Joshua 4","Psalms 129-131"],"secret":["Isaiah 64","Matthew 12"]},"0703":{"family":["Joshua 5-6:5","Psalms 132-134"],"secret":["Isaiah 65","Matthew 13"]},"0704":{"family":["Joshua 6:6ff","Psalms 135-136"],"secret":["Isaiah 66","Matthew 14"]},"0705":{"family":["Joshua 7","Psalms 137-138"],"secret":["Jeremiah 1","Matthew 15"]},"0706":{"family":["Joshua 8","Psalms 139"],"secret":["Jeremiah 2","Matthew 16"]},"0707":{"family":["Joshua 9","Psalms 140-141"],"secret":["Jeremiah 3","Matthew 17"]},"0708":{"family":["Joshua 10","Psalms 142-143"],"secret":["Jeremiah 4","Matthew 18"]},"0709":{"family":["Joshua 11","Psalms 144"],"secret":["Jeremiah 5","Matthew 19"]},"0710":{"family":["Joshua 12-13","Psalms 145"],"secret":["Jeremiah 6","Matthew 20"]},"0711":{"family":["Joshua 14-15","Psalms 146-147"],"secret":["Jeremiah 7","Matthew 21"]},"0712":{"family":["Joshua 16-17","Psalms 148"],"secret":["Jeremiah 8","Matthew 22"]},"0713":{"family":["Joshua 18-19","Psalms 149-150"],"secret":["Jeremiah 9","Matthew 23"]},"0714":{"family":["Joshua 20-21","Acts 1"],"secret":["Jeremiah 10","Matthew 24"]},"0715":{"family":["Joshua 22","Acts 2"],"secret":["Jeremiah 11","Matthew 25"]},"0716":{"family":["Joshua 23","Acts 3"],"secret":["Jeremiah 12","Matthew 26"]},"0717":{"family":["Joshua 24","Acts 4"],"secret":["Jeremiah 13","Matthew 27"]},"0718":{"family":["Judges 1","Acts 5"],"secret":["Jeremiah 14","Matthew 28"]},"0719":{"family":["Judges 2","Acts 6"],"secret":["Jeremiah 15","Mark 1"]},"0720":{"family":["Judges 3","Acts 7"],"secret":["Jeremiah 16","Mark 2"]},"0721":{"family":["Judges 4","Acts 8"],"secret":["Jeremiah 17","Mark 3"]},"0722":{"family":["Judges 5","Acts 9"],"secret":["Jeremiah 18","Mark 4"]},"0723":{"family":["Judges 6","Acts 10"],"secret":["Jeremiah 19","Mark 5"]},"0724":{"family":["Judges 7","Acts 11"],"secret":["Jeremiah 20","Mark 6"]},"0725":{"family":["Judges 8","Acts 12"],"secret":["Jeremiah 21","Mark 7"]},"0726":{"family":["Judges 9","Acts 13"],"secret":["Jeremiah 22","Mark 8"]},"0727":{"family":["Judges 10-11:11","Acts 14"],"secret":["Jeremiah 23","Mark 9"]},"0728":{"family":["Judges 11:12ff","Acts 15"],"secret":["Jeremiah 24","Mark 10"]},"0729":{"family":["Judges 12","Acts 16"],"secret":["Jeremiah 25","Mark 11"]},"0730":{"family":["Judges 13","Acts 17"],"secret":["Jeremiah 26","Mark 12"]},"0731":{"family":["Judges 14","Acts 18"],"secret":["Jeremiah 27","Mark 13"]},"0801":{"family":["Judges 15","Acts 19"],"secret":["Jeremiah 28","Mark 14"]},"0802":{"family":["Judges 16","Acts 20"],"secret":["Jeremiah 29","Mark 15"]},"0803":{"family":["Judges 17","Acts 21"],"secret":["Jeremiah 30-31","Mark 16"]},"0804":{"family":["Judges 18","Acts 22"],"secret":["Jeremiah 32","Psalms 1-2"]},"0805":{"family":["Judges 19","Acts 23"],"secret":["Jeremiah 33","Psalms 3-4"]},"0806":{"family":["Judges 20","Acts 24"],"secret":["Jeremiah 34","Psalms 5-6"]},"0807":{"family":["Judges 21","Acts 25"],"secret":["Jeremiah 35","Psalms 7-8"]},"0808":{"family":["Ruth 1","Acts 26"],"secret":["Jeremiah 36 & 45","Psalms 9"]},"0809":{"family":["Ruth 2","Acts 27"],"secret":["Jeremiah 37","Psalms 10"]},"0810":{"family":["Ruth 3-4","Acts 28"],"secret":["Jeremiah 38","Psalms 11-12"]},"0811":{"family":["1 Samuel 1","Romans 1"],"secret":["Jeremiah 39","Psalms 13-14"]},"0812":{"family":["1 Samuel 2","Romans 2"],"secret":["Jeremiah 40","Psalms 15-16"]},"0813":{"family":["1 Samuel 3","Romans 3"],"secret":["Jeremiah 41","Psalms 17"]},"0814":{"family":["1 Samuel 4","Romans 4"],"secret":["Jeremiah 42","Psalms 18"]},"0815":{"family":["1 Samuel 5-6","Romans 5"],"secret":["Jeremiah 43","Psalms 19"]},"0816":{"family":["1 Samuel 7-8","Romans 6"],"secret":["Jeremiah 44","Psalms 20-21"]},"0817":{"family":["1 Samuel 9","Romans 7"],"secret":["Jeremiah 46","Psalms 22"]},"0818":{"family":["1 Samuel 10","Romans 8"],"secret":["Jeremiah 47","Psalms 23-24"]},"0819":{"family":["1 Samuel 11","Romans 9"],"secret":["Jeremiah 48","Psalms 25"]},"0820":{"family":["1 Samuel 12","Romans 10"],"secret":["Jeremiah 49","Psalms 26-27"]},"0821":{"family":["1 Samuel 13","Romans 11"],"secret":["Jeremiah 50","Psalms 28-29"]},"0822":{"family":["1 Samuel 14","Romans 12"],"secret":["Jeremiah 51","Psalms 30"]},"0823":{"family":["1 Samuel 15","Romans 13"],"secret":["Jeremiah 52","Psalms 31"]},"0824":{"family":["1 Samuel 16","Romans 14"],"secret":["Lamentations 1","Psalms 32"]},"0825":{"family":["1 Samuel 17","Romans 15"],"secret":["Lamentations 2","Psalms 33"]},"0826":{"family":["1 Samuel 18","Romans 16"],"secret":["Lamentations 3","Psalms 34"]},"0827":{"family":["1 Samuel 19","1 Corinthians 1"],"secret":["Lamentations 4","Psalms 35"]},"0828":{"family":["1 Samuel 20","1 Corinthians 2"],"secret":["Lamentations 5","Psalms 36"]},"0829":{"family":["1 Samuel 21-22","1 Corinthians 3"],"secret":["Ezekiel 1","Psalms 37"]},"0830":{"family":["1 Samuel 23","1 Corinthians 4"],"secret":["Ezekiel 2","Psalms 38"]},"0831":{"family":["1 Samuel 24","1 Corinthians 5"],"secret":["Ezekiel 3","Psalms 39"]},"0901":{"family":["1 Samuel 25","1 Corinthians 6"],"secret":["Ezekiel 4","Psalms 40-41"]},"0902":{"family":["1 Samuel 26","1 Corinthians 7"],"secret":["Ezekiel 5","Psalms 42-43"]},"0903":{"family":["1 Samuel 27","1 Corinthians 8"],"secret":["Ezekiel 6","Psalms 44"]},"0904":{"family":["1 Samuel 28","1 Corinthians 9"],"secret":["Ezekiel 7","Psalms 45"]},"0905":{"family":["1 Samuel 29-30","1 Corinthians 10"],"secret":["Ezekiel 8","Psalms 46-47"]},"0906":{"family":["1 Samuel 31","1 Corinthians 11"],"secret":["Ezekiel 9","Psalms 48"]},"0907":{"family":["2 Samuel 1","1 Corinthians 12"],"secret":["Ezekiel 10","Psalms 49"]},"0908":{"family":["2 Samuel 2","1 Corinthians 13"],"secret":["Ezekiel 11","Psalms 50"]},"0909":{"family":["2 Samuel 3","1 Corinthians 14"],"secret":["Ezekiel 12","Psalms 51"]},"0910":{"family":["2 Samuel 4-5","1 Corinthians 15"],"secret":["Ezekiel 13","Psalms 52-54"]},"0911":{"family":["2 Samuel 6","1 Corinthians 16"],"secret":["Ezekiel 14","Psalms 55"]},"0912":{"family":["2 Samuel 7","2 Corinthians 1"],"secret":["Ezekiel 15","Psalms 56-57"]},"0913":{"family":["2 Samuel 8-9","2 Corinthians 2"],"secret":["Ezekiel 16","Psalms 58-59"]},"0914":{"family":["2 Samuel 10","2 Corinthians 3"],"secret":["Ezekiel 17","Psalms 60-61"]},"0915":{"family":["2 Samuel 11","2 Corinthians 4"],"secret":["Ezekiel 18","Psalms 62-63"]},"0916":{"family":["2 Samuel 12","2 Corinthians 5"],"secret":["Ezekiel 19","Psalms 64-65"]},"0917":{"family":["2 Samuel 13","2 Corinthians 6"],"secret":["Ezekiel 20","Psalms 66-67"]},"0918":{"family":["2 Samuel 14","2 Corinthians 7"],"secret":["Ezekiel 21","Psalms 68"]},"0919":{"family":["2 Samuel 15","2 Corinthians 8"],"secret":["Ezekiel 22","Psalms 69"]},"0920":{"family":["2 Samuel 16","2 Corinthians 9"],"secret":["Ezekiel 23","Psalms 70-71"]},"0921":{"family":["2 Samuel 17","2 Corinthians 10"],"secret":["Ezekiel 24","Psalms 72"]},"0922":{"family":["2 Samuel 18","2 Corinthians 11"],"secret":["Ezekiel 25","Psalms 73"]},"0923":{"family":["2 Samuel 19","2 Corinthians 12"],"secret":["Ezekiel 26","Psalms 74"]},"0924":{"family":["2 Samuel 20","2 Corinthians 13"],"secret":["Ezekiel 27","Psalms 75-76"]},"0925":{"family":["2 Samuel 21","Galatians 1"],"secret":["Ezekiel 28","Psalms 77"]},"0926":{"family":["2 Samuel 22","Galatians 2"],"secret":["Ezekiel 29","Psalms 78:1-37"]},"0927":{"family":["2 Samuel 23","Galatians 3"],"secret":["Ezekiel 30","Psalms 78:38ff"]},"0928":{"family":["2 Samuel 24","Galatians 4"],"secret":["Ezekiel 31","Psalms 79"]},"0929":{"family":["1 Kings 1","Galatians 5"],"secret":["Ezekiel 32","Psalms 80"]},"0930":{"family":["1 Kings 2","Galatians 6"],"secret":["Ezekiel 33","Psalms 81-82"]},"1001":{"family":["1 Kings 3","Ephesians 1"],"secret":["Ezekiel 34","Psalms 83-84"]},"1002":{"family":["1 Kings 4-5","Ephesians 2"],"secret":["Ezekiel 35","Psalms 85"]},"1003":{"family":["1 Kings 6","Ephesians 3"],"secret":["Ezekiel 36","Psalms 86"]},"1004":{"family":["1 Kings 7","Ephesians 4"],"secret":["Ezekiel 37","Psalms 87-88"]},"1005":{"family":["1 Kings 8","Ephesians 5"],"secret":["Ezekiel 38","Psalms 89"]},"1006":{"family":["1 Kings 9","Ephesians 6"],"secret":["Ezekiel 39","Psalms 90"]},"1007":{"family":["1 Kings 10","Philippians 1"],"secret":["Ezekiel 40","Psalms 91"]},"1008":{"family":["1 Kings 11","Philippians 2"],"secret":["Ezekiel 41","Psalms 92-93"]},"1009":{"family":["1 Kings 12","Philippians 3"],"secret":["Ezekiel 42","Psalms 94"]},"1010":{"family":["1 Kings 13","Philippians 4"],"secret":["Ezekiel 43","Psalms 95-96"]},"1011":{"family":["1 Kings 14","Colossians 1"],"secret":["Ezekiel 44","Psalms 97-98"]},"1012":{"family":["1 Kings 15","Colossians 2"],"secret":["Ezekiel 45","Psalms 99-101"]},"1013":{"family":["1 Kings 16","Colossians 3"],"secret":["Ezekiel 46","Psalms 102"]},"1014":{"family":["1 Kings 17","Colossians 4"],"secret":["Ezekiel 47","Psalms 103"]},"1015":{"family":["1 Kings 18","1 Thessalonians 1"],"secret":["Ezekiel 48","Psalms 104"]},"1016":{"family":["1 Kings 19","1 Thessalonians 2"],"secret":["Daniel 1","Psalms 105"]},"1017":{"family":["1 Kings 20","1 Thessalonians 3"],"secret":["Daniel 2","Psalms 106"]},"1018":{"family":["1 Kings 21","1 Thessalonians 4"],"secret":["Daniel 3","Psalms 107"]},"1019":{"family":["1 Kings 22","1 Thessalonians 5"],"secret":["Daniel 4","Psalms 108-109"]},"1020":{"family":["2 Kings 1","2 Thessalonians 1"],"secret":["Daniel 5","Psalms 110-111"]},"1021":{"family":["2 Kings 2","2 Thessalonians 2"],"secret":["Daniel 6","Psalms 112-113"]},"1022":{"family":["2 Kings 3","2 Thessalonians 3"],"secret":["Daniel 7","Psalms 114-115"]},"1023":{"family":["2 Kings 4","1 Timothy 1"],"secret":["Daniel 8","Psalms 116"]},"1024":{"family":["2 Kings 5","1 Timothy 2"],"secret":["Daniel 9","Psalms 117-118"]},"1025":{"family":["2 Kings 6","1 Timothy 3"],"secret":["Daniel 10","Psalms 119:1-24"]},"1026":{"family":["2 Kings 7","1 Timothy 4"],"secret":["Daniel 11","Psalms 119:25-48"]},"1027":{"family":["2 Kings 8","1 Timothy 5"],"secret":["Daniel 12","Psalms 119:49-72"]},"1028":{"family":["2 Kings 9","1 Timothy 6"],"secret":["Hosea 1","Psalms 119:73-96"]},"1029":{"family":["2 Kings 10","2 Timothy 1"],"secret":["Hosea 2","Psalms 119:97-120"]},"1030":{"family":["2 Kings 11-12","2 Timothy 2"],"secret":["Hosea 3-4","Psalms 119:121-144"]},"1031":{"family":["2 Kings 13","2 Timothy 3"],"secret":["Hosea 5-6","Psalms 119:145-176"]},"1101":{"family":["2 Kings 14","2 Timothy 4"],"secret":["Hosea 7","Psalms 120-122"]},"1102":{"family":["2 Kings 15","Titus 1"],"secret":["Hosea 8","Psalms 123-125"]},"1103":{"family":["2 Kings 16","Titus 2"],"secret":["Hosea 9","Psalms 126-128"]},"1104":{"family":["2 Kings 17","Titus 3"],"secret":["Hosea 10","Psalms 129-131"]},"1105":{"family":["2 Kings 18","Philemon 1"],"secret":["Hosea 11","Psalms 132-134"]},"1106":{"family":["2 Kings 19","Hebrews 1"],"secret":["Hosea 12","Psalms 135-136"]},"1107":{"family":["2 Kings 20","Hebrews 2"],"secret":["Hosea 13","Psalms 137-138"]},"1108":{"family":["2 Kings 21","Hebrews 3"],"secret":["Hosea 14","Psalms 139"]},"1109":{"family":["2 Kings 22","Hebrews 4"],"secret":["Joel 1","Psalms 140-141"]},"1110":{"family":["2 Kings 23","Hebrews 5"],"secret":["Joel 2","Psalms 142"]},"1111":{"family":["2 Kings 24","Hebrews 6"],"secret":["Joel 3","Psalms 143"]},"1112":{"family":["2 Kings 25","Hebrews 7"],"secret":["Amos 1","Psalms 144"]},"1113":{"family":["1 Chronicles 1-2","Hebrews 8"],"secret":["Amos 2","Psalms 145"]},"1114":{"family":["1 Chronicles 3-4","Hebrews 9"],"secret":["Amos 3","Psalms 146-147"]},"1115":{"family":["1 Chronicles 5-6","Hebrews 10"],"secret":["Amos 4","Psalms 148-150"]},"1116":{"family":["1 Chronicles 7-8","Hebrews 11"],"secret":["Amos 5","Luke 1:1-38"]},"1117":{"family":["1 Chronicles 9-10","Hebrews 12"],"secret":["Amos 6","Luke 1:39ff"]},"1118":{"family":["1 Chronicles 11-12","Hebrews 13"],"secret":["Amos 7","Luke 2"]},"1119":{"family":["1 Chronicles 13-14","James 1"],"secret":["Amos 8","Luke 3"]},"1120":{"family":["1 Chronicles 15","James 2"],"secret":["Amos 9","Luke 4"]},"1121":{"family":["1 Chronicles 16","James 3"],"secret":["Obadiah 1","Luke 5"]},"1122":{"family":["1 Chronicles 17","James 4"],"secret":["Jonah 1","Luke 6"]},"1123":{"family":["1 Chronicles 18","James 5"],"secret":["Jonah 2","Luke 7"]},"1124":{"family":["1 Chronicles 19-20","1 Peter 1"],"secret":["Jonah 3","Luke 8"]},"1125":{"family":["1 Chronicles 21","1 Peter 2"],"secret":["Jonah 4","Luke 9"]},"1126":{"family":["1 Chronicles 22","1 Peter 3"],"secret":["Micah 1","Luke 10"]},"1127":{"family":["1 Chronicles 23","1 Peter 4"],"secret":["Micah 2","Luke 11"]},"1128":{"family":["1 Chronicles 24-25","1 Peter 5"],"secret":["Micah 3","Luke 12"]},"1129":{"family":["1 Chronicles 26-27","2 Peter 1"],"secret":["Micah 4","Luke 13"]},"1130":{"family":["1 Chronicles 28","2 Peter 2"],"secret":["Micah 5","Luke 14"]},"1201":{"family":["1 Chronicles 29","2 Peter 3"],"secret":["Micah 6","Luke 15"]},"1202":{"family":["2 Chronicles 1","1 John 1"],"secret":["Micah 7","Luke 16"]},"1203":{"family":["2 Chronicles 2","1 John 2"],"secret":["Nahum 1","Luke 17"]},"1204":{"family":["2 Chronicles 3-4","1 John 3"],"secret":["Nahum 2","Luke 18"]},"1205":{"family":["2 Chronicles 5-6:11","1 John 4"],"secret":["Nahum 3","Luke 19"]},"1206":{"family":["2 Chronicles 6:12ff","1 John 5"],"secret":["Habakkuk 1","Luke 20"]},"1207":{"family":["2 Chronicles 7","2 John 1"],"secret":["Habakkuk 2","Luke 21"]},"1208":{"family":["2 Chronicles 8","3 John 1"],"secret":["Habakkuk 3","Luke 22"]},"1209":{"family":["2 Chronicles 9","Jude 1"],"secret":["Zephaniah 1","Luke 23"]},"1210":{"family":["2 Chronicles 10","Revelation 1"],"secret":["Zephaniah 2","Luke 24"]},"1211":{"family":["2 Chronicles 11-12","Revelation 2"],"secret":["Zephaniah 3","John 1"]},"1212":{"family":["2 Chronicles 13","Revelation 3"],"secret":["Haggai 1","John 2"]},"1213":{"family":["2 Chronicles 14-15","Revelation 4"],"secret":["Haggai 2","John 3"]},"1214":{"family":["2 Chronicles 16","Revelation 5"],"secret":["Zechariah 1","John 4"]},"1215":{"family":["2 Chronicles 17","Revelation 6"],"secret":["Zechariah 2","John 5"]},"1216":{"family":["2 Chronicles 18","Revelation 7"],"secret":["Zechariah 3","John 6"]},"1217":{"family":["2 Chronicles 19-20","Revelation 8"],"secret":["Zechariah 4","John 7"]},"1218":{"family":["2 Chronicles 21","Revelation 9"],"secret":["Zechariah 5","John 8"]},"1219":{"family":["2 Chronicles 22-23","Revelation 10"],"secret":["Zechariah 6","John 9"]},"1220":{"family":["2 Chronicles 24","Revelation 11"],"secret":["Zechariah 7","John 10"]},"1221":{"family":["2 Chronicles 25","Revelation 12"],"secret":["Zechariah 8","John 11"]},"1222":{"family":["2 Chronicles 26","Revelation 13"],"secret":["Zechariah 9","John 12"]},"1223":{"family":["2 Chronicles 27-28","Revelation 14"],"secret":["Zechariah 10","John 13"]},"1224":{"family":["2 Chronicles 29","Revelation 15"],"secret":["Zechariah 11","John 14"]},"1225":{"family":["2 Chronicles 30","Revelation 16"],"secret":["Zechariah 12-13:1","John 15"]},"1226":{"family":["2 Chronicles 31","Revelation 17"],"secret":["Zechariah 13:2ff","John 16"]},"1227":{"family":["2 Chronicles 32","Revelation 18"],"secret":["Zechariah 14","John 17"]},"1228":{"family":["2 Chronicles 33","Revelation 19"],"secret":["Malachi 1","John 18"]},"1229":{"family":["2 Chronicles 34","Revelation 20"],"secret":["Malachi 2","John 19"]},"1230":{"family":["2 Chronicles 35","Revelation 21"],"secret":["Malachi 3","John 20"]},"1231":{"family":["2 Chronicles 36","Revelation 22"],"secret":["Malachi 4","John 21"]}}
"""

data = json.loads(json_data)

BOOK_ABBR_MAP = {
    "Genesis": "GEN", "Exodus": "EXO", "Leviticus": "LEV", "Numbers": "NUM", "Deuteronomy": "DEU",
    "Joshua": "JOS", "Judges": "JDG", "Ruth": "RUT", "1 Samuel": "1SA", "2 Samuel": "2SA", 
    "1 Kings": "1KI", "2 Kings": "2KI", "1 Chronicles": "1CH", "2 Chronicles": "2CH",
    "Ezra": "EZR", "Nehemiah": "NEH", "Esther": "EST", "Job": "JOB", "Psalms": "PSA", 
    "Proverbs": "PRO", "Ecclesiastes": "ECC", "Song of Songs": "SOS", "Isaiah": "ISA", 
    "Jeremiah": "JER", "Lamentations": "LAM", "Ezekiel": "EZE", "Daniel": "DAN", 
    "Hosea": "HOS", "Joel": "JOE", "Amos": "AMO", "Obadiah": "OBA", "Jonah": "JON", 
    "Micah": "MIC", "Nahum": "NAH", "Habakkuk": "HAB", "Zephaniah": "ZEP", "Haggai": "HAG", 
    "Zechariah": "ZEC", "Malachi": "MAL",
    "Matthew": "MAT", "Mark": "MAR", "Luke": "LUK", "John": "JOH", "Acts": "ACT", 
    "Romans": "ROM", "1 Corinthians": "1CO", "2 Corinthians": "2CO", "Galatians": "GAL", 
    "Ephesians": "EPH", "Philippians": "PHI", "Colossians": "COL", 
    "1 Thessalonians": "1TH", "2 Thessalonians": "2TH", "1 Timothy": "1TI", "2 Timothy": "2TI", 
    "Titus": "TIT", "Philemon": "PHM", "Hebrews": "HEB", "James": "JAM", 
    "1 Peter": "1PE", "2 Peter": "2PE", "1 John": "1JN", "2 John": "2JN", 
    "3 John": "3JN", "Jude": "JUD", "Revelation": "REV"
}

def parse_reading(reading_str):
    # Remove split verses like ":1-38", ":39ff"
    # Logic:
    # 1. Split by ' & ' (and)
    # 2. Split by ' ' to get Book Name vs Chapter
    # 3. Handle dash ranges "9-10" or "11-12:21"
    
    # Pre-clean "&"
    sub_readings = []
    if " & " in reading_str:
        parts = reading_str.split(" & ")
        # e.g. "Jeremiah 36 & 45"
        # part 0: "Jeremiah 36" -> Full
        # part 1: "45" -> Just chapter
        base_book = None
        for p in parts:
            if any(b in p for b in BOOK_ABBR_MAP.keys()):
                 # This is a full book+chapter
                 sub_readings.append(p)
                 # Keep book name for next part if needed?
                 # Extract book name
                 for bk in BOOK_ABBR_MAP.keys():
                     if p.startswith(bk):
                         base_book = bk
                         break
            else:
                # Just chapter? e.g. "45"
                if base_book:
                    sub_readings.append(f"{base_book} {p}")
                else:
                    # Should not happen in standard mcheyne unless complex
                    sub_readings.append(p)
    else:
        sub_readings = [reading_str]
        
    final_codes = []
    
    for item in sub_readings:
        # e.g. "Exodus 11-12:21", "Luke 1:1-38", "Psalms 119:1-24"
        # We only want CHAPTERS for linking.
        # If "Luke 1:1-38", chapter is 1.
        # If "Luke 1:39ff", chapter is 1. (Duplicate is fine)
        # If "Genesis 9-10", chapters are 9, 10.
        
        # Extract Book Name
        book_name = ""
        rest = ""
        # Match longest book name first
        sorted_books = sorted(BOOK_ABBR_MAP.keys(), key=len, reverse=True)
        for bk in sorted_books:
            if item.startswith(bk):
                book_name = bk
                rest = item[len(bk):].strip() # "11-12:21"
                break
        
        if not book_name:
            continue
            
        code = BOOK_ABBR_MAP[book_name]
        
        # Parse chapter part
        # "11-12:21" -> 11, 12
        # "1"
        # "119:1-24" -> 119
        
        # Split by dash to check for range
        tokens = rest.split('-')
        
        start_token = tokens[0].strip() # "11" or "1:39ff" or "1"
        
        # Get start chapter
        start_ch_str = start_token.split(':')[0].split(' ')[-1] # Handle potentially weird spaces? " 11"
        start_ch = int(start_ch_str)
        
        end_ch = start_ch
        
        if len(tokens) > 1:
            end_token = tokens[1].strip() # "12:21", "24", "10"
            # Does end token have colon?
            end_ch_str = end_token.split(':')[0]
            # Is it a number?
            if end_ch_str.isdigit():
                end_ch = int(end_ch_str)
            else:
                # Could be "38" from "1:1-38".
                # If "1:1-38", start is 1. End token is "38".
                # If 38 is > 1? "Luke 1" has 80 verses.
                # It's ambiguous if "1-2" vs "1:1-2".
                # Context: "Psalms 1-2" -> Ch 1, 2.
                # "Luke 1:1-38" -> Ch 1.
                # Difference is colon.
                
                # If start_token has colon, dash likely means verse range -> Single Chapter.
                # If start_token NO colon, dash likely means Chapter range -> Multiple Chapters.
                pass
                
        # Refined Logic
        has_colon = ':' in start_token
        
        chapters = []
        if has_colon:
            # "1:1-38", "12:22ff", "119:121-144"
            # start_token is "1:1" or "1:39ff" or "119:121"
            parts = start_token.split(':')
            ch_num = int(parts[0])
            start_verse = parts[1]
            
            verse_range = start_verse
            
            # Check if there was a dash that we split off
            if len(tokens) > 1:
                # tokens[1] could be "38" (end verse) or "144"
                # or could be "13:5" (end chapter:verse - unlikely for single reading item in JSON usually)
                end_part = tokens[1]
                if ':' not in end_part:
                     # It is a continuing verse range for the same chapter
                     verse_range = f"{start_verse}-{end_part}"
            
            chapters.append((ch_num, verse_range))
        else:
            # "1", "1-2", "9-10"
            if len(tokens) > 1:
                # Same logic as before for chapter ranges
                end_part = tokens[1]
                end_ch_maybe = int(end_part.split(':')[0])
                for x in range(start_ch, end_ch_maybe + 1):
                    chapters.append((x, None))
            else:
                 chapters.append((start_ch, None))
                
        for ch_info in chapters:
            ch = ch_info[0]
            v_range = ch_info[1]
            if v_range:
                final_codes.append(f"{code}{ch}:{v_range}")
            else:
                final_codes.append(f"{code}{ch}")
            
    return final_codes

# Build Schedule
lines = []
lines.append("SCHEDULE = {")

for k, v in data.items():
    # k = "0101"
    readings = []
    # Combine family and secret
    raw_list = v['family'] + v['secret']
    
    for r in raw_list:
        parsed = parse_reading(r)
        readings.extend(parsed)
        
    readings_str = ", ".join([f'"{x}"' for x in readings])
    lines.append(f'    "{k}": [{readings_str}],')
    
lines.append("}")

with open("mccheyne_schedule_correct.py", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
    
print("Successfully parsed and created mccheyne_schedule_correct.py")
