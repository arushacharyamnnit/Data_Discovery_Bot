import pandas as pd
from spacy.matcher import PhraseMatcher
import numpy as np
import json
from pathlib import Path
# Load NLP Pkgs
import spacy
#from wordcloud import WordCloud, STOPWORDS
from spacy.util import minibatch, compounding

import matplotlib.pyplot as plt
import re
import random
from spacy.tokens import DocBin

from spello.model import SpellCorrectionModel
sp = SpellCorrectionModel(language='en')
sp.load('SpellModel/model.pkl')

# def load_data(file):
#     with open(file,"r",encoding="utf-8") as f:
#         data=json.load(f)
#     return data
# train = load_data(r"jobs.json") 
# lst=train['results']
# jobnames=[]
# for item in lst[0]['items']:
#     if item['job_name'] not in jobnames:
#       jobnames.append(item['job_name'].lower())

nlp = spacy.load('output_ocidw/model-last')

# owner=["owner","owns"]
# creator=["created","creator"]
# freq=["repeat interval","frequency"]
# typ=["type"]
# nxtr=["next run"]
# logdate=["log date"]
# status=["successful","status","failure"]
# jobaction=["action","description"]
# stt=["start date","scheduled date"]
# execu=["run duration","last run","previous run"]
# # lst=[owner,freq,typ,jobaction,stt]

# matcher = PhraseMatcher(nlp.vocab)
# patterns = [nlp.make_doc(text) for text in jobnames]
# matcher.add('job_name',patterns)
# patterns = [nlp.make_doc(text) for text in owner]
# matcher.add('owner',patterns)
# # patterns = [nlp.make_doc(text) for text in others]
# # matcher.add('o',patterns)
# patterns = [nlp.make_doc(text) for text in freq]
# matcher.add('repeat_interval',patterns)
# patterns = [nlp.make_doc(text) for text in typ]
# matcher.add('job_type',patterns)
# patterns = [nlp.make_doc(text) for text in jobaction]
# matcher.add('job_action',patterns)
# patterns = [nlp.make_doc(text) for text in stt]
# matcher.add('start_date',patterns)
# patterns = [nlp.make_doc(text) for text in execu]
# matcher.add('run_duration',patterns)
# patterns = [nlp.make_doc(text) for text in creator]
# matcher.add('job_creator',patterns)
# # patterns = [nlp.make_doc(text) for text in jd]
# # matcher.add('job_de',patterns)
# patterns = [nlp.make_doc(text) for text in nxtr]
# matcher.add('next_run_date',patterns)
# patterns = [nlp.make_doc(text) for text in logdate]
# matcher.add('log_date',patterns)
# patterns = [nlp.make_doc(text) for text in status]
# matcher.add('status',patterns)
while 1:
    print('Enter: ')
    ex=input()
    # ex = "owner and start date of purge_cloud_logger and dscs_audit_cleanup_unified"
    # ex=sp.spell_correct(ex)['spell_corrected_text']
    doc = nlp(ex)


    # matches = matcher(doc,as_spans=True)
    # for span in matches:
    #       print(span.text,span.label_)
    
    # print(ex)


    for ent in doc.ents:
        print(ent.text,ent.label_)