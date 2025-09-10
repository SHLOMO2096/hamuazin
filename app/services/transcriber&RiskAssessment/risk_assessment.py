import decoder
import config_transcriber
from app.log.logger import Logger

logger = Logger.get_logger()

class RiskAssessment:
    """
    Class to perform risk assessment on a given text based on hostile and non-hostile word lists.
    """
    def __init__(self):
        self.hostile_words_coded = config_transcriber.HOSTILE_WORDS_CODED
        self.non_hostile_words_coded = config_transcriber.NON_HOSTILE_WORDS_CODED
        self.decoder_hostile = decoder.Decoder(self.hostile_words_coded)
        self.non_hostile_decoder = decoder.Decoder(self.non_hostile_words_coded)
        self.hostile_list = self.decoder_hostile.decode()
        self.not_hostile_list = self.non_hostile_decoder.decode()

        


        
    def finding_word_frequency(self, text:list, list_words:list):
        """
        Find the frequency of words from list_words in the given text.
        """
        frequency_text = 0
        for part in list_words:
            if " " in part:
                lst = part.split()
                for i in range(len(text)-1):
                    if lst[0] == text[i] and lst[1] == text[i+1]:
                        frequency_text += 1
                        lst.clear()
            else:
                if part in text:
                    frequency_text += 1
        return frequency_text



    def risk_assessment(self, text:str):
        """
        Perform risk assessment based on the frequency of hostile and non-hostile words.
        """
        text = text.lower().split()
        total_hostile_impressions = self.finding_word_frequency(text,self.hostile_list)
        total_non_hostile_impressions = self.finding_word_frequency(text,self.not_hostile_list)
        total_words = len(text)
        bds_percent = ((total_hostile_impressions *2) + total_non_hostile_impressions) / total_words * 100
        is_bds = bds_percent > 10
        if bds_percent > 10:
            bds_threat_level = "high"
        elif bds_percent < 3:
            bds_threat_level = "none"
        else:
            bds_threat_level = "medium"

        dict_assessment = {"bds_percent":bds_percent, "is_bds": is_bds, "bds_threat_level": bds_threat_level}
        return dict_assessment
        
