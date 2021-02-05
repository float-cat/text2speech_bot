import re


def TextPreprocessing(text: str) -> (str):

    text = re.sub(r"<script[\w\W]*?<\/script>", "", text)
    text = re.sub(r"<button[\w\W]*?<\/button>", "", text)

    # remove html tags
    text = re.sub(r"(\<(\/?[^>]+)>)", " ", text)

    # remove links
    text = re.sub(r"http\S+", " ссылка ", text)

    # removing extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()
