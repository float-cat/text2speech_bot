import re


def TextPreprocessing(text):
    text = re.sub(r"<script>[\w\W]*?<\/script>", "", text)
    text = re.sub(r"<button[\w\W]*?</button>", "", text)
    text = re.sub(r"(\<(/?[^>]+)>)", " ", text)
    text = re.sub(r"http[\w\W]*? ", " Здесь ссылка ", text)
    text = re.sub(r"\s+", " ", text)
    return text
