from newspaper import Article
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from re import split
from random import randint

cnn = "https://edition.cnn.com/2025/05/21/africa/trump-resettling-south-africas-afrikaners-intl"
APnws = "https://apnews.com/article/trump-syria-saudi-arabia-sharaa-assad-sanctions-bb208f25cfedecd6446fd1626012c0fb"
wiki = "https://en.wikipedia.org/wiki/International_System_of_Units"

class Text_tagger ():
    def __init__(self, url, limit_counter=-1):
       
        self.url = url
        self.limit_counter = limit_counter
        self.location = "./light_emotion_model"
        self.model = AutoModelForSequenceClassification.from_pretrained(self.location)
        self.tokenizer = AutoTokenizer.from_pretrained(self.location)
        self.title = "Template"
        self.tags = {
                "anger" : ["loud","fast","high"],
                "fear" : ["medium","fast","high"],
                "joy" : ["medium","fast","high"],
                "sadness" : ["low","slow","low"],
                "neutral" : ["medium","medium","medium"],
                "disgust" : ["low","slow","low"],
                "surprise" : ["loud","fast","high"]
                }
        
        
        self._extract_information()
        self.labeled_text = self._process_information()
        self._export()
        

    def _extract_information(self):
        """Retrurns list of strings based on the main text of the article

        Args:
            url (string): url of article to extract

        Returns:
            tuple: title and cleaned list of phrases from the article
        """

        article = Article(self.url, language = "en")
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


    def _process_information(self):

        #obtain general information of the page
        title, text_lst = self._extract_information()
        #prepare classifier
        classifier = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)

        # add a the title as the name of the file and the first part of the output text
        if title:
            result_txt = title+"\n\n"
            self.title = title
        
        #pause time in between phrases
        min_time = 1
        max_time = 7

        counter = 0
        for phrase in text_lst:

            result = classifier(phrase)[0] #obtain only the predicted tag
            tag = self.tags[result["label"]]

            #add text with properties to the final text
            properties = f'prosody volume="{tag[0]}" rate="{tag[1]}" pitch="{tag[2]}"'

            result_txt += f'<{properties}>\n{phrase}\n</prosody>'

            #add random ending sleep time
            result_txt += f'<break time="{randint(min_time,max_time)/10}s"/>\n'

            counter +=1

            if counter >= self.limit_counter:
                return result_txt

        return result_txt


    def _export(self):
        with open(self.title, "w", encoding="utf-8") as file:
            file.write(self.labeled_text)

Text_tagger(cnn, 3)