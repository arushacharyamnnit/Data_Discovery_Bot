import spacy
import json
import pprint
from ElasticSearchConnection import *

# from QuerySearch import*
class ElasticSearchQuery:
    
    def __init__(self):
        pass

    def QueryJobStatic(self,jobnames,attributes):
       
        attributes.append('job_name')
        body={
            "_source":attributes,
            "query":{
                "terms":{
                    "job_name":jobnames}}}
        return body


    def QueryJobDynamic1(self,jobnames,attributes):
       
        attributes.append('job_name')
        body={
            "_source":attributes,
            "query":{
                "bool":{
                    "must":[{
                        "terms":{
                            "job_name":jobnames}},
                        {"match":{"status":"SUCCEEDED"}}]
                    }
                },
                    "sort":[{"log_date":{"order":"desc"}}],"size":1
            }
        return body


    def QueryJobDynamic2(self,jobnames,attributes):
       
        attributes.append('job_name')
        body={
            "_source":attributes,
                "query":{
                    "bool":{
                    "must":[{
                        "terms":{
                            "job_name":jobnames
                            }
                        }]
                    }
                },"sort":[{"log_date":{"order":"desc"}}],
                "size":1
                }
        return body

    def QueryCatalog1(self,attribute_name,attributes,entity_name):
        
       attributes.append('Attribute Name')
       if entity_name!=[]:
           attributes.append('Entity Name')
       if entity_name!=[]:    
            body={
            "_source":attributes,
                "query":{
                  "bool":{
                    "must":[
                       { "terms":{"Attribute Name":attribute_name}},
                       {"terms":{"Entity Name":entity_name}}]}}}
            return body
       else:
            body={
             "_source":attributes,
              "query":{
                "bool":{
                 "must":[
                   {"terms":{"Attribute Name":attribute_name}}]}}}
            return body

    def QueryCatalog2(self,entity_name,entity_attributes):
       
       entity_attributes.append('Entity Name')
       body={
        "_source":entity_attributes,
        "query":{
            "terms":{
                "Entity Name":entity_name
            }
        }
    }
       return body

    def QueryGlossary(self,name,attributes):
        attributes.append('Name')
        body={
        "_source":attributes,
        "query":{
            "match":{"Name":name}
            }
        }
        return body
    
    def FetchJobResults(self,JobAndAttributes):
        
        NonEmptyJobNames=0
        AllAttributes=[]
        FetchedResults=[]
        
        for item in JobAndAttributes:
            JobName=item['jobname']
            
            if(JobName!=[]):
                NonEmptyJobNames+=1

            StaticAttributes=item['att']
            DynamicAttributes=item['att1']

            AllAttributes.extend(StaticAttributes)
            AllAttributes.extend(DynamicAttributes)

            print('Jobname: ',JobName)
            print('Static job details: ',StaticAttributes)
            print('Dynamic job details: ',DynamicAttributes)
            print('Fetching data from elastic search...') 
            if StaticAttributes!=[]:
                # To fetch job details from elastic search
                body = self.QueryJobStatic(JobName,StaticAttributes)
                res = es.search(index='test',doc_type='_doc',body=body)
                # print('Data fetched from elastic search: ')
                # pprint.pprint(res)
                for i in res['hits']['hits']:
                   FetchedResults.append(json.dumps(i['_source'],indent=4))
            body1={}
            if DynamicAttributes!=[]:
                # To fetch execution details from elastic search
                if (all(x in DynamicAttributes for x in ['status', 'run_duration'])):
                    body1=self.QueryJobDynamic2(JobName,DynamicAttributes)

                elif 'run_duration' in DynamicAttributes:
                    body1=self.QueryJobDynamic1(JobName,DynamicAttributes)

                elif 'status' in DynamicAttributes or 'log_date' in DynamicAttributes :
                    body1=self.QueryJobDynamic2(JobName,DynamicAttributes) 

                else:
                    body1=self.QueryJobStatic(JobName,DynamicAttributes)
                res1 = es.search(index='test1',doc_type='_doc',body=body1)
                # print('Data fetched from elastic search: ')
                # pprint.pprint(res1)
                for i in res1['hits']['hits']:
                    FetchedResults.append(json.dumps(i['_source'],indent=4))
        
        return NonEmptyJobNames,FetchedResults,AllAttributes

    def FetchCatalogResults(self,AttributeName,EntityName,Attributes,EntityAttributes):
        
        FetchedResults=[]
        if Attributes!=[]:        
            attr_body = self.QueryCatalog1(AttributeName,Attributes,EntityName)
            res = es.search(index='ocidw',doc_type='_doc',body=attr_body)
            # print(res)
            print('Data fetched from elastic search: ',res)
            for i in res['hits']['hits']:
                FetchedResults.append(json.dumps(i['_source'],indent=4))

        if EntityAttributes!=[]:
            ent_body=self.QueryCatalog2(EntityName,EntityAttributes)
            # print('body1: ',body1)
            res1 = es.search(index='ocidw_ent',doc_type='_doc',body=ent_body)
            print('Data fetched from elastic search: ',res1)
            for i in res1['hits']['hits']:
                FetchedResults.append(json.dumps(i['_source'],indent=4))
        
    
        return FetchedResults

    def FetchGlossaryResults(self,GlossaryAndAttributes):
        
        NonEmptyGlossaryNames=0
        AllAttributes,FetchedResults=[],[]
        
        for item in GlossaryAndAttributes:
            names=item['name']
            if(names!=[]):
                NonEmptyGlossaryNames+=1

            attributes=item['att']
            
            AllAttributes.extend(attributes)
            print('Name: ',names)
            print('details: ',attributes)

            print('Fetching data from elastic search...') 
            for name in names:
                if attributes!=[]:
                    body = self.getbody5(name,attributes)
                    res = es.search(index='glossary2',doc_type='_doc',body=body)
                    print('Data fetched from elastic search: ')
                    pprint.pprint(res)
                    for i in res['hits']['hits']:
                        FetchedResults.append(json.dumps(i['_source'],indent=4))
            
        return NonEmptyGlossaryNames,FetchedResults,AllAttributes


