import spacy
import json
from spacy.training import offsets_to_biluo_tags
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot
from sklearn.metrics import *
import numpy
import random
import numpy as np
from sklearn import metrics
from sklearn.metrics import f1_score
import pprint
import math

from scipy import spatial


from sklearn.preprocessing import LabelEncoder


def calculate_cosine_distance(a, b):
    cosine_distance = float(spatial.distance.cosine(a, b))
    return cosine_distance


def calculate_cosine_similarity(a, b):
    cosine_similarity = 1 - calculate_cosine_distance(a, b)
    return cosine_similarity



def load_data(file):
    with open (file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def write_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
nlp = spacy.load("output_ocidw/model-best")

docs = load_data("ocidw_data.json")
 
# print(docs)   
random.shuffle(docs)
docs=docs[1:1000]
def get_cleaned_label(label: str):
    if "-" in label:
        return label.split("-")[1]
    else:
        return label
    
def create_total_target_vector(docs):
    target_vector = []
    for doc in docs:
        # print (doc)
        new = nlp.make_doc(doc[0])
        entities = doc[1]["entities"]
        bilou_entities = offsets_to_biluo_tags(new, entities)
        final = []
        for item in bilou_entities:
            final.append(get_cleaned_label(item))
        target_vector.extend(final)
    return target_vector

def create_prediction_vector(text):
    return [get_cleaned_label(prediction) for prediction in get_all_ner_predictions(text)]

def create_total_prediction_vector(docs: list):
    prediction_vector = []
    for doc in docs:
        prediction_vector.extend(create_prediction_vector(doc[0]))
    return prediction_vector

def get_all_ner_predictions(text):
    doc = nlp(text)
    entities = [(e.start_char, e.end_char, e.label_) for e in doc.ents]
    bilou_entities = offsets_to_biluo_tags(doc, entities)
    return bilou_entities    
def get_model_labels():
    labels = list(nlp.get_pipe("ner").labels)
    labels.append("O")
    return sorted(labels)
def get_dataset_labels():
    return sorted(set(create_total_target_vector(docs)))

def getTP(y_true,y_pred,entity):
    TP=0
    for i in range(0,len(y_true)):
        if y_true[i] == y_pred[i] and y_true[i] == entity :
          TP+=1
    return TP

def getFN(y_true,y_pred,entity):
    FN=0
    for i in range(0,len(y_true)):
        if y_true[i] ==entity and y_pred[i] != entity:
          FN+=1
    return FN    
def getFP(y_true,y_pred,entity):
    FP=0
    for i in range(0,len(y_true)):
        if y_true[i] !=entity and y_pred[i] == entity:
          FP+=1
    return FP    

classes = sorted(set(create_total_target_vector(docs)))
y_true = create_total_target_vector(docs)
y_pred = create_total_prediction_vector(docs)
# print (y_true)
# print (y_pred)
le = LabelEncoder()
le.fit(y_true)
y_true1 = le.transform(y_true)
y_pred1 = le.transform(y_pred)
# print(y_true1)
print(len(y_true1))
sum=0
for i in y_true1:
    sum+=i
print(sum/len(y_true1))    
# print(y_pred1)

all_labels=sorted(set(y_true))
all_labels1=all_labels[1:]
print(y_true)
print(len(y_true))
dict={}

for ent in all_labels1:
    # print(ent,"Total Instances Present: ",tp+fn)
    # print("TP"+'\t'+'FP'+'\t'+'FN')
    # print("PRECISION"+'\t'+"RECALL"+'\t'+"F1SCORE")
    # acc=0.97
    inner={}
    tp=getTP(y_true,y_pred,ent)
    fp=getFP(y_true,y_pred,ent)
    fn=getFN(y_true,y_pred,ent)
    print("Entity: ",ent,"  Total Instances Present: ",tp+fn)
    print("TP"+'\t'+'FP'+'\t'+'FN')
    inner['Entity']=ent
    # inner['Total Instances Present']=tp+fn
    # inner['True Positive']=tp
    # inner['False Positive']=fp
    # inner['False Negative']=fn
   

    




    precision=tp/(tp+fp)
    recall=tp/(tp+fn)
    f1score=(2*precision*recall)/(precision+recall)
    # acc+=f1score
    f1score="{:.2f}".format(f1score)
    precision="{:.2f}".format(precision)
    recall="{:.2f}".format(recall)
    inner['Precision']=precision
    inner['Recall']=recall
    inner['F1 score']=f1score
    dict[ent]=inner
    
    print(tp,'\t',fp,'\t',fn)
    print('PRECISION\t'+'RECALL'+'\t'+'F1SCORE')
    print(precision,'\t\t',recall,'\t',f1score)
    print()
    

print('Cosine Similarity: ',calculate_cosine_similarity(y_true1,y_pred1))                 
print('Mean Squared Error: ',mean_squared_error(y_true1, y_pred1))
# print(f1_score(y_true, y_pred))
print('Classification Report: \n ',metrics.classification_report(y_true, y_pred))

dict['Cosine Similarity']=calculate_cosine_similarity(y_true1,y_pred1)
dict['Root Mean Squared Error']=mean_squared_error(y_true1, y_pred1)
# =metrics.classification_report(y_true, y_pred)

# dict['Classification Report']=out_dict
string=[]
string.append(json.dumps(dict,indent=4))
st=""
# print(string)
fh=open('catalog_metrics.txt','w')
for i in string:
    fh.write(i+'\n')
fh.close()    





