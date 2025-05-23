from newspaper import Article
from re import split

cnn = "https://edition.cnn.com/2025/05/21/africa/trump-resettling-south-africas-afrikaners-intl"
APnws = "https://apnews.com/article/trump-syria-saudi-arabia-sharaa-assad-sanctions-bb208f25cfedecd6446fd1626012c0fb"
wiki = "https://en.wikipedia.org/wiki/International_System_of_Units"


def extract_information(url):
    """Retrurns list of strings based on the main text of the article

    Args:
        url (string): url of article to extract

    Returns:
        tuple: title and cleaned list of phrases from the article
    """

    article = Article(url, language = "en")
    article.download()
    article.parse()

    title = article.title
    raw_text = article.text

    phrases_list = split(r"\n|\r|\.", raw_text)
    #take out empty spaces
    phrases_list = list(filter(('').__ne__, phrases_list))

    #joining abandoned ”
    i = 0
    for phrase in phrases_list:
        if len(phrase) == 1 and i > 0:
            phrases_list[i-1] = phrases_list[i-1]+phrase
            del phrases_list[i]
        i += 1

    return (title, phrases_list)


