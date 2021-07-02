from spello.model import SpellCorrectionModel 
import json

sp = SpellCorrectionModel(language='en') 

def load_data(file):
  with open(file,"r",encoding="utf-8") as f:
    data=json.load(f)
  return data


train = load_data("train_data.json")

train_data=[]
for text, _ in train:
    train_data.append(text)

print(train_data)

sp.train(train_data)

# print(sp.spell_correct('gve the jb onwer of purge cloud logger'))

sp.save(model_save_dir='SpellModel')