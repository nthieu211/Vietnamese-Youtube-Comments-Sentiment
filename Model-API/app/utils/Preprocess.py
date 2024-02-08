import regex as re
import emoji
import py_vncorenlp
import os

# Start VnCoreNLP
vncorenlp_path = os.path.join(os.path.dirname(__file__), "vncorenlp")
if not os.path.exists(os.path.join(vncorenlp_path, "VnCoreNLP-1.2.jar")):
    raise FileNotFoundError(f"Not found VnCoreNLP at {vncorenlp_path}")
rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=vncorenlp_path)


# Remove HTML code
def remove_HTML_URL(text):
    html = re.compile(r"<[^>]+>")
    text = html.sub("", text).replace("\r", " ")
    text = re.sub(r"\S*(https|http)?:\S*", "", text)  # Remove URL
    return text


# Standardize unicode
def convert_unicode(text):
    char1252 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ"
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ"
    char1252 = char1252.split("|")
    charutf8 = charutf8.split("|")

    dic = {}
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return re.sub(
        r"à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ",
        lambda x: dic[x.group()],
        text,
    )


# Standardize accent typing
vowels_to_ids = {}
vowels_table = [
    ["a", "à", "á", "ả", "ã", "ạ", "a"],
    ["ă", "ằ", "ắ", "ẳ", "ẵ", "ặ", "aw"],
    ["â", "ầ", "ấ", "ẩ", "ẫ", "ậ", "aa"],
    ["e", "è", "é", "ẻ", "ẽ", "ẹ", "e"],
    ["ê", "ề", "ế", "ể", "ễ", "ệ", "ee"],
    ["i", "ì", "í", "ỉ", "ĩ", "ị", "i"],
    ["o", "ò", "ó", "ỏ", "õ", "ọ", "o"],
    ["ô", "ồ", "ố", "ổ", "ỗ", "ộ", "oo"],
    ["ơ", "ờ", "ớ", "ở", "ỡ", "ợ", "ow"],
    ["u", "ù", "ú", "ủ", "ũ", "ụ", "u"],
    ["ư", "ừ", "ứ", "ử", "ữ", "ự", "uw"],
    ["y", "ỳ", "ý", "ỷ", "ỹ", "ỵ", "y"],
]

for i in range(len(vowels_table)):
    for j in range(len(vowels_table[i]) - 1):
        vowels_to_ids[vowels_table[i][j]] = (i, j)


def is_valid_vietnamese_word(word):
    chars = list(word)
    vowel_indexes = -1
    for index, char in enumerate(chars):
        x, y = vowels_to_ids.get(char, (-1, -1))
        if x != -1:
            if vowel_indexes == -1:
                vowel_indexes = index
            else:
                if index - vowel_indexes != 1:
                    return False
                vowel_indexes = index
    return True


def standardize_word_typing(word):
    if not is_valid_vietnamese_word(word):
        return word
    chars = list(word)
    dau_cau = 0
    vowel_indexes = []
    qu_or_gi = False

    for index, char in enumerate(chars):
        x, y = vowels_to_ids.get(char, (-1, -1))
        if x == -1:
            continue
        elif x == 9:  # check qu
            if index != 0 and chars[index - 1] == "q":
                chars[index] = "u"
                qu_or_gi = True
        elif x == 5:  # check gi
            if index != 0 and chars[index - 1] == "g":
                chars[index] = "i"
                qu_or_gi = True

        if y != 0:
            dau_cau = y
            chars[index] = vowels_table[x][0]

        if not qu_or_gi or index != 1:
            vowel_indexes.append(index)

    if len(vowel_indexes) < 2:
        if qu_or_gi:
            if len(chars) == 2:
                x, y = vowels_to_ids.get(chars[1])
                chars[1] = vowels_table[x][dau_cau]
            else:
                x, y = vowels_to_ids.get(chars[2], (-1, -1))
                if x != -1:
                    chars[2] = vowels_table[x][dau_cau]
                else:
                    chars[1] = (
                        vowels_table[5][dau_cau]
                        if chars[1] == "i"
                        else vowels_table[9][dau_cau]
                    )
            return "".join(chars)
        return word

    for index in vowel_indexes:
        x, y = vowels_to_ids[chars[index]]
        if x == 4 or x == 8:  # ê, ơ
            chars[index] = vowels_table[x][dau_cau]
            return "".join(chars)

    if len(vowel_indexes) == 2:
        if vowel_indexes[-1] == len(chars) - 1:
            x, y = vowels_to_ids[chars[vowel_indexes[0]]]
            chars[vowel_indexes[0]] = vowels_table[x][dau_cau]
        else:
            x, y = vowels_to_ids[chars[vowel_indexes[1]]]
            chars[vowel_indexes[1]] = vowels_table[x][dau_cau]
    else:
        x, y = vowels_to_ids[chars[vowel_indexes[1]]]
        chars[vowel_indexes[1]] = vowels_table[x][dau_cau]
    return "".join(chars)


def standardize_sentence_typing(text):
    words = text.lower().split()
    for index, word in enumerate(words):
        cw = re.sub(r"(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)", r"\1/\2/\3", word).split("/")
        if len(cw) == 3:
            cw[1] = standardize_word_typing(cw[1])
        words[index] = "".join(cw)
    return " ".join(words)


# Normalize acronyms
# !wget https://gist.githubusercontent.com/nguyenvanhieuvn/7d9441c10b3c2739499fc5a4d9ea06fb/raw/df939245b3e841b62af115be4dcb3516dadc9fc5/teencode.txt

replace_list = {
    "ô kêi": "ok",
    "okie": "ok",
    "o kê": "ok",
    "okey": "ok",
    "ôkê": "ok",
    "ô kê": "ok",
    "oki": "ok",
    "oke": "ok",
    "okay": "ok",
    "okê": "ok",
    "tks": "cảm ơn",
    "thks": "cảm ơn",
    "thanks": "cảm ơn",
    "ths": "cảm ơn",
    "thank": "cảm ơn",
    "kg": "không",
    "not": "không",
    "k": "không",
    "kh": "không",
    "kô": "không",
    "hok": "không",
    "ko": "không",
    "khong": "không",
    "kp": "không phải",
    "he he": "cười",
    "hehe": "cười",
    "hihi": "cười",
    "haha": "cười",
    "hjhj": "cười",
    "thick": "thích",
    "huhu": "khóc",
    "cute": "dễ thương",
    "cc": "chửi tục",
    "cặc": "chửi tục",
    "dm": "chửi tục",
    "dmm": "chửi tục",
    "dume": "chửi tục",
    "dma": "chửi tục",
    "vl": "chửi tục",
    "sz": "cỡ",
    "size": "cỡ",
    "wa": "quá",
    "wá": "quá",
    "qá": "quá",
    "đx": "được",
    "dk": "được",
    "dc": "được",
    "đk": "được",
    "đc": "được",
    "vs": "với",
    "j": "gì",
    "“": " ",
    "time": "thời gian",
    "m": "mình",
    "mik": "mình",
    "r": "rồi",
    "bjo": "bao giờ",
    "very": "rất",
    "nk": "nó",
    "authentic": "chuẩn chính hãng",
    "aut": "chuẩn chính hãng",
    "auth": "chuẩn chính hãng",
    "date": "hạn sử dụng",
    "hsd": "hạn sử dụng",
    "store": "cửa hàng",
    "sop": "cửa hàng",
    "sốp": "cửa hàng",
    "shop": "cửa hàng",
    "sp": "sản phẩm",
    "product": "sản phẩm",
    "hàg": "hàng",
    "sgk": "sách giáo khoa",
    "cv": "công việc",
    "ship": "giao hàng",
    "delivery": "giao hàng",
    "síp": "giao hàng",
    "order": "đặt hàng",
    "gud": "tốt",
    "wel done": "tốt",
    "good": "tốt",
    "gút": "tốt",
    "tot": "tốt",
    "nice": "tốt",
    "perfect": "rất tốt",
    "quality": "chất lượng",
    "chất lg": "chất lượng",
    "excelent": "hoàn hảo",
    "bt": "bình thường",
    "bth": "bình thường",
    "sad": "tệ",
    "por": "tệ",
    "poor": "tệ",
    "bad": "tệ",
    "beautiful": "đẹp tuyệt vời",
    "dep": "đẹp",
    "xau": "xấu",
    "sấu": "xấu",
    "thik": "thích",
    "iu": "yêu",
    "fake": "giả mạo",
    "quickly": "nhanh",
    "quick": "nhanh",
    "fast": "nhanh",
    "fresh": "tươi",
    "delicious": "ngon",
    "dt": "điện thoại",
    "fb": "facebook",
    "face": "facebook",
    "ks": "khách sạn",
    "nv": "nhân viên",
    "nt": "nhắn tin",
    "ib": "nhắn tin",
    "tl": "trả lời",
    "trl": "trả lời",
    "rep": "trả lời",
    "fback": "feedback",
    "fedback": "feedback",
    "sd": "sử dụng",
    "sài": "xài",
    "^_^": "cười",
    ":)": "cười",
    ":))": "cười",
    ":)))": "cười",
    "=))": "cười",
    "=)))": "cười",
    ":(": "buồn",
    ":((": "buồn",
    ":(((": "buồn",
    "❤️": "yêu thích",
    "👍": "thích",
    "🎉": "chúc mừng",
    "😀": "cười",
    "😍": "yêu thích",
    "😂": "cười lớn",
    "🤣": "cười lớn",
    "🤗": "vỗ tay",
    "😙": "cười",
    "🙂": "cười",
    "😔": "buồn",
    "😓": "buồn",
    "T_T": "khóc",
    "😭": "khóc lớn",
    "😡": "giận dữ",
    "🤬": "giận dữ",
    "🤡": "mặt chú hề",
    "😩": "thất vọng",
    "😞": "thất vọng",
    "😢": "xúc động",
    "⭐": "star",
    "*": "star",
    "🌟": "star",
}

with open(
    os.path.join(os.path.dirname(__file__), "teencode.txt"), encoding="utf-8"
) as f:
    for pair in f.readlines():
        key, value = pair.split("\t")
        replace_list[key] = value.strip()


def normalize_acronyms(text):
    words = []
    for word in text.strip().split():
        if word.lower() not in replace_list.keys():
            words.append(word)
        else:
            words.append(replace_list[word.lower()])
    return emoji.demojize(" ".join(words))  # Remove Emojis


# Word segmentation & Tokenize
def word_segmentation(text):
    return rdrsegmenter.word_segment(text)


def text_preprocess(text):
    text = convert_unicode(text)
    text = standardize_sentence_typing(text)
    text = normalize_acronyms(text)
    text = re.sub(
        r"[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]",
        " ",
        text,
    )  # Remove unnecessary character
    text = re.sub(r"\s+", " ", text).strip()  # Remove spacing > 1
    text = word_segmentation(text)  # required for PhoBERT
    text = " ".join(text)  # return 1 string
    return text
