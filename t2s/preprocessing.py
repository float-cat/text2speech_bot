import re


def TextPreprocessing(text):
    text = re.sub(r"<script[\w\W]*?<\/script>", "", text)
    text = re.sub(r"<button[\w\W]*?<\/button>", "", text)
    # delete html tags
    text = re.sub(r"(\<(\/?[^>]+)>)", " ", text)
    # delete links
    text = re.sub(r"http\S+", " ссылка ", text)
    # removing extra spaces
    text = re.sub(r"\s+", " ", text)
    return text
