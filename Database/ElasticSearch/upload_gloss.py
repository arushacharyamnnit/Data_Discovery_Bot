import elasticsearch
import os
import sys
from elasticsearch import Elasticsearch,helpers
import pandas as pd
import numpy as np
import json

df3=pd.read_csv('glossary.csv',error_bad_lines=False)
df3.insert(1, "glosName", "OCIDW")
df3=df3[1:]


df3.fillna("not defined", inplace=True)

     

df3=df3.to_dict('records')
es = Elasticsearch([{'host':'localhost','port':'9200'}])
# es.indices.delete(index="glossary",ignore=[400,404])
es = Elasticsearch([{'host':'localhost','port':'9200'}])

# es.indices.create(index="glossary1",ignore=400)


es = helpers.bulk(es,df3,index="glossary2")
