import elasticsearch
import os
import sys
from elasticsearch import Elasticsearch,helpers
import pandas as pd
import numpy as np
import json

# df3=pd.read_csv('glossary.csv',error_bad_lines=False)
# df3.insert(1, "glosName", "OCIDW")
# df3=df3[1:]

df1=pd.read_csv('ocidw.csv',error_bad_lines=False)
df1.drop(columns=df1.columns[-1], 
        axis=1, 
        inplace=True)
df1.fillna("not defined", inplace=True)
# df2=pd.read_csv('ocidw1.csv',error_bad_lines=False)
# df2.fillna("not defined", inplace=True)
# for columns in df1.columns:
#     df1[columns] = df1[columns].str.lower()
# for columns in df2.columns:
#     df2[columns] = df2[columns].str.lower()
# for columns in df3.columns:
#     df3[columns] = df3[columns].str.lower()        

df1=df1.to_dict('records')
# df2=df2.to_dict('records')
# df3=df3.to_dict('records')


es = Elasticsearch([{'host':'localhost','port':'9200'}])

es.indices.delete(index="ocidw",ignore=[400,404])
es.indices.create(index="ocidw",ignore=400)
# es.indices.create(index="ocidw_ent",ignore=400)
# es.indices.create(index="glossary",ignore=400)

es = helpers.bulk(es,df1,index="ocidw")
# es = helpers.bulk(es,df2,index="ocidw_ent")
# es = helpers.bulk(es,df3,index="glossary")
