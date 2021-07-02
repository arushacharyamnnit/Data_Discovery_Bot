from ElasticSearchConnection import *
import spacy

nlp1 = spacy.load('../NLP model/output1/model-best')
nlp2 = spacy.load('../NLP model/output_ocidw/model-best')
nlp3=spacy.load('../NLP model/model-last')


class ModelLoader:
    
    def __init__(self,dict_index_fields):
        self.dict_index_fields=dict_index_fields

    
    def getFuzzy(self,name):
     
        name=name.lower()
        body={
            "query": {
               "fuzzy": {
                  "job_name": {
                      "value": name,
                       "fuzziness": "AUTO",
                    }
                }
            }
         }
        res = es.search(index='test',doc_type='_doc',body=body)

        if(res['hits']['hits']==[]):
            return name
        else:
            return res['hits']['hits'][0]['_source']['job_name']

    
    def getDictionary(self,JobNames,StaticAttributes,DynamicAttributes):

        ListofKeys=[['jobname',JobNames],['att',StaticAttributes],['att1',DynamicAttributes]]
        keys=[key for key in ListofKeys ]
        jobData={
            key[0]: key[1] for key in keys
        }
        return jobData
    
    def getGlossaryMap(self,GlossaryNames,GlossaryAttributes):
        
        ListofKeys=[['name',GlossaryNames],['att',GlossaryAttributes]]
        keys=[key  for key in ListofKeys ]
        GlosData={
            key[0]: key[1] for key in keys
        }
        return GlosData
    
    def ExtractJobNamesAndAttributes(self,user_input):
        
        doc = nlp1(user_input)         
        JobNames,StaticAttributes,DynamicAttributes,JobAndAttributes=[],[],[],[]

        for ent in doc.ents[::-1]:
            
            if(ent.label_=='job_name'):
                jname=self.getFuzzy(ent.text)
                if(StaticAttributes!=[] or DynamicAttributes!=[]):
                    JobAndAttributes.append(self.getDictionary(JobNames,StaticAttributes,DynamicAttributes))
                    JobNames,StaticAttributes,DynamicAttributes=[],[],[]
                    JobNames.append(jname.lower())
                else:
                    JobNames.append(jname.lower())
            else:
                if ent.label_ in self.dict_index_fields['test']:
                        StaticAttributes.append(ent.label_)
                if ent.label_ in self.dict_index_fields['test1']:
                        DynamicAttributes.append(ent.label_)
        JobAndAttributes.append(self.getDictionary(JobNames,StaticAttributes,DynamicAttributes))

        return JobAndAttributes 

    def ExtractCatalogAndAttributes(self,user_input):
        doc = nlp2(user_input)
        print('Catalog model loaded...')
        
        AttributeName,EntityName,Attributes,EntityAttributes=[],[],[],[]

        print('Fetching Entities...')
        for ent in doc.ents:
            print('Text: ',ent.text,'and Labels: ',ent.label_)
            if(ent.label_=="Entity Name"):
                EntityName.append(ent.text.lower())
            elif (ent.label_=="Attribute Name"):
                    AttributeName.append(ent.text.lower())
            else:
                if ent.label_ in self.dict_index_fields['ocidw']:
                    Attributes.append(ent.label_)
                if ent.label_ in self.dict_index_fields['ocidw_ent']:
                    EntityAttributes.append(ent.label_)

        return AttributeName,EntityName,Attributes,EntityAttributes 

    def ExtractGlossaryNamesAndAttributes(self,user_input):
        
        doc=nlp3(user_input)
        GlossaryNames,GlossaryAttributes,GlossaryAndAttributes=[],[],[]

        mapping={
            'DESCRIPTION': 'Description',
            'STATUS':'Status',
            'PATH':'_Parent Path_',
            'CREATOR':'Created by'
        }
        print('Fetching Entities...')
        for ent in doc.ents[::-1]:
            # print('Text: ',ent.text,' and Labels: ',ent.label_)

            if(ent.label_=='NAME'):
                if(GlossaryAttributes!=[]):
                    GlossaryAndAttributes.append(self.getGlossaryMap(GlossaryNames,GlossaryAttributes))
                    GlossaryNames=[]
                    GlossaryAttributes=[]
                    GlossaryNames.append(ent.text.lower())
                else:
                    GlossaryNames.append(ent.text.lower())
            else:
                label=mapping[ent.label_]
                if label in self.dict_index_fields['glossary2']:
                    GlossaryAttributes.append(label)

        GlossaryAndAttributes.append(self.getGlossaryMap(GlossaryNames,GlossaryAttributes))
        return GlossaryAndAttributes