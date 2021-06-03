from binascii import crc32, unhexlify

def get_luck(uid, date):
    seed = uid + date.year + date.month + date.day
    width = seed.bit_length()
    width += 8 - ((width % 8) or 8)
    fmt = '%%0%dx' % (width // 4)
    s = unhexlify(fmt % seed)
    luck_level = crc32(s) % 5 + 1
    luck_text = '今日人品：{}{}'.format('★' * luck_level, '☆' * (5 - luck_level))
    return luck_text

from csv import reader
def get_radical(word):
    dict_path = 'assets/xinhua.csv'
    with open(dict_path, newline='', encoding='utf-8') as f:
        word_table = reader(f)
        radical_dict = {}
        for line in word_table:
            radical_dict[line[0]] = line[1]
    if word in radical_dict:
        return radical_dict[word]
    else:
        return None

from zhdate import ZhDate
from datetime import datetime
def get_luck_v2(uid, date, name):

    gans = '甲乙丙丁戊己庚辛壬癸'
    zhis = '子丑寅卯辰巳午未申酉戌亥'

    lunar_date = ZhDate.from_datetime(date)
    year_gan = (lunar_date.lunar_year - 4) % 10
    year_zhi = (lunar_date.lunar_year - 4) % 12
    month_gan = (year_gan * 2 + lunar_date.lunar_month + 1) % 10
    month_zhi = (lunar_date.lunar_month + 1) % 12
    day_gan = (date - datetime(1970,2,13)).days % 10
    day_zhi = (date - datetime(1970,2,13)).days % 12
    hour_zhi = (date.hour + 1) // 2 % 12
    hour_gan = ((day_gan) % 5 * 2 + hour_zhi) % 10

    name_scores = {"金":0, "木":0, "水":0, "火":0, "土":0}
    for word in name:
        radical = get_radical(word)
        if radical == None:
            continue
        if radical == '金' or radical == '钅':
            name_scores['金'] += 1
        if radical == '木':
            name_scores['木'] += 1
        if radical == '水' or radical == '氵':
            name_scores['水'] += 1
        if radical == '火':
            name_scores['火'] += 1
        if radical == '土':
            name_scores['土'] += 1

    max_score = max(name_scores[i] for i in name_scores)
    if max_score == 0:
        max_xing = '信息不足'
    else:
        max_xing = '、'.join(i for i in name_scores if name_scores[i] == max_score)

    ganzhi_text = '今日干支：{}{}年 {}{}月 {}{}日 {}{}时'.format(
    gans[year_gan],zhis[year_zhi],gans[month_gan],zhis[month_zhi],gans[day_gan],zhis[day_zhi],gans[hour_gan],zhis[hour_zhi])
    wuxing_text = '所属五行：{}'.format(max_xing)

    text = '\n'.join([ganzhi_text, wuxing_text,get_luck(uid, date)])

    return text