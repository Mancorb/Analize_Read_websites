from newspaper import Article
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from re import split
from random import randint
import os
import sys


class Text_tagger ():
    def __init__(self, url, limit_counter=-1):
       
        self.url = url
        self.limit_counter = limit_counter
        self.location = self._get_resource_path("light_emotion_model")

        try:

            self.model = AutoModelForSequenceClassification.from_pretrained(self.location)
            self.tokenizer = AutoTokenizer.from_pretrained(self.location)
        except Exception as e:
            raise RuntimeError(f"Error loading model/tokenizer from {self.location}: {e}")


        self.title = "Template"
        self.tags = {
                "anger" : ["loud","fast","high"],
                "fear" : ["medium","fast","high"],
                "joy" : ["medium","fast","high"],
                "sadness" : ["low","slow","low"],
                "neutral" : ["medium","medium","medium"],
                "disgust" : ["low","slow","low"],
                "surprise" : ["loud","fast","high"],
                "amusement" : ["medium","fast","medium"],
                "approval" : ["medium","fast","high"]
                }
        
        try:
            self._extract_information()
            self.labeled_text = self._process_information()
            self._export()
        except Exception as e:
            raise RuntimeError(f"Processing failed: {e}")
        

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


    def _get_resource_path(self,relative_path):
        """ Get absolute path to resource whether running as script or bundled exe """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  # PyInstaller extracts to this temp dir
        else:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    def _process_information(self):
        """Extract and return tokenized text with apropriate labels

        Returns:
            string: resulting text with labels included
        """

        #obtain general information of the page
        title, text_lst = self._extract_information()
        #prepare classifier
        classifier = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)
        result_txt=""
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

            if self.limit_counter and counter >= self.limit_counter:
                return result_txt

        return result_txt


    def _export(self):
        """Export the results to a txt file

        Raises:
            RuntimeError: Error in case of failure
        """
        if self.title: file_name = self.title + ".txt"
        else: file_name = "Transcript.txt"

        try:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(self.labeled_text)
        except Exception as e:
            raise RuntimeError(f"Text classification failed {e}")

if __name__ == "__main__":
    while True:
        try:
            url =  input("[+] Please paste the url of the website to scrap:\n->")

            limit = None

            print("[+] Begining Process...")

            Text_tagger(url, limit)

            print("[+] Process complete!!\n\n")

        except Exception as e:
            print(f"[!] Error\n{e}\n\n_______________________________\nTry again....\n\n\n")
            input("Press Enter to continue...")
    