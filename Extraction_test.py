from newspaper import Article


cnn = "https://edition.cnn.com/2025/05/21/africa/trump-resettling-south-africas-afrikaners-intl"
APnws = "https://apnews.com/article/trump-syria-saudi-arabia-sharaa-assad-sanctions-bb208f25cfedecd6446fd1626012c0fb"
wiki = "https://en.wikipedia.org/wiki/International_System_of_Units"

article = Article(cnn, language = "en")
article.download()
article.parse()

print(article.title)
print(article.text)