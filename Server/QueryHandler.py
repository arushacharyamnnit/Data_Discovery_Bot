import re
import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_sm')
matcher = PhraseMatcher(nlp.vocab)

KeyWordList=['job','catalog','glossary']

for keyword in KeyWordList:
    patterns=[nlp.make_doc(keyword)]
    matcher.add(keyword,patterns)



class QueryHandler:
    
    def __init__(self):
        pass

    def PreprocessQuery(self,user_input):
        
        user_input=re.sub('[!,*)(@#%&$?]','',user_input)
        user_input=re.sub(' +',' ',user_input)
        user_input=user_input.lstrip()
        user_input=user_input.rstrip()

        return user_input

    def KeyWordExtractor(self,user_input):

        doc=nlp(user_input)
        matches = matcher(doc)
        string_id=""
        
        KeyWordSet=set()
        for keyword in range(len(matches)):
            KeyWordSet.add(matches[keyword][0])
        DistinctKeyword=0
        
        if(len(matches)>0):
            DistinctKeyword=len(KeyWordSet)
            match_id = matches[0][0]
            string_id = nlp.vocab.strings[match_id]
        
        return DistinctKeyword,string_id
