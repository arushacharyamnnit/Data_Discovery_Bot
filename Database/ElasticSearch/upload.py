import elasticsearch
import os
import sys
from elasticsearch import Elasticsearch,helpers
import pandas as pd
import numpy as np
import json
def load_data(file):
    with open(file,"r",encoding="utf-8") as f:
        data=json.load(f)
    return data
train = load_data(r"jobRuns.json")
lst=train['results']

es = Elasticsearch([{'host':'localhost','port':'9200'}])
es.indices.delete(index="test1",ignore=[400,404])
es.indices.create(index="test1",ignore=400)
# es = helpers.bulk(es,lst[0]['items'],index="test1")
for i in lst[0]['items']:
    res=es.index(index='test1',doc_type='_doc',body=i)
