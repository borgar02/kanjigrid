import re
import unicodedata
import collections

from . import data

unit_tuple = collections.namedtuple("unit", "idx value avg_interval count")

cjk_re = re.compile("CJK (UNIFIED|COMPATIBILITY) IDEOGRAPH")
def isKanji(unichar):
    return bool(cjk_re.match(unicodedata.name(unichar, "")))

def scoreAdjust(score):
    score += 1
    return 1 - 1 / (score * score)

def addUnitData(units, unitKey, i, card, kanjionly):
    validKey = data.ignore.find(unitKey) == -1 and (not kanjionly or isKanji(unitKey))
    if validKey:
        if unitKey not in units:
            unit = unit_tuple(0, unitKey, 0.0, 0)
            units[unitKey] = unit
        units[unitKey] = addDataFromCard(units[unitKey], i, card)

def addDataFromCard(unit, new_idx, card):
    if card.type > 0:
        newTotal = (unit.avg_interval * unit.count) + card.ivl
        new_count = unit.count + 1
        avg_interval = newTotal / new_count
        return unit_tuple(unit.idx, unit.value, avg_interval, new_count)

    if new_idx < unit.idx or unit.idx == 0:
        return unit_tuple(new_idx, unit.value, unit.avg_interval, unit.count)

    return unit

def hsvrgbstr(h, s=0.8, v=0.9):
    _256 = lambda x: round(x*256)
    i = int(h*6.0)
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i % 6
    if i == 0: return "#%0.2X%0.2X%0.2X" % (_256(v), _256(t), _256(p))
    if i == 1: return "#%0.2X%0.2X%0.2X" % (_256(q), _256(v), _256(p))
    if i == 2: return "#%0.2X%0.2X%0.2X" % (_256(p), _256(v), _256(t))
    if i == 3: return "#%0.2X%0.2X%0.2X" % (_256(p), _256(q), _256(v))
    if i == 4: return "#%0.2X%0.2X%0.2X" % (_256(t), _256(p), _256(v))
    if i == 5: return "#%0.2X%0.2X%0.2X" % (_256(v), _256(p), _256(q))

def get_background_color(avg_interval, config_interval, count, missing = False):
    if count != 0:
        return hsvrgbstr(scoreAdjust(avg_interval / config_interval)/2)
    elif missing:
        return "#EEE"
    else:
        return "#FFF"

def get_font_css(config):
    if config.lang == "ja":
        return config.jafontcss
    if config.lang ==  "zh":
        return config.zhfontcss
    if config.lang ==  "zh-Hans":
        return config.zhhansfontcss
    if config.lang ==  "zh-Hant":
        return config.zhhantfontcss
    if config.lang ==  "ko":
        return config.kofontcss
    if config.lang ==  "vi":
        return config.vifontcss
    
