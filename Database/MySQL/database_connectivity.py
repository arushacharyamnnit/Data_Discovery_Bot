import mysql.connector
import json
def load_data(file):
     with open(file,"r",encoding="utf-8") as f:
       data=json.load(f)
     return data
def DataUpdate(user_id,user_input_query,entities,input_time,bot_response_time,successful):
     # print(job) 
     print('Esatablishing db connection..')
     mydb = mysql.connector.connect(
          host="localhost",
           user="root",
            passwd="",
            database="user"
     )

     
     # returns JSON object as 
     # a dictionary
     data = load_data("D:/DataDiscovery_Bot/DataDiscovery_Bot/Database/MySQL/table.json")
     # print(data)
     mycursor = mydb.cursor()
     print('Record to be inserted: ',user_id,user_input_query,input_time,bot_response_time,successful)

     # Inserting data to bot performance metrics table
     sql='INSERT INTO {table_name} ({col1},{col2},{col3},{col4},{col5}) VALUES (%s,%s,%s,%s,%s);'.format(table_name=data['bot_performance_metrics'],
     col1=data['user_id'],col2=data['user_query_input'],col3=data['query_input_time'],col4=data['bot_response_time'],col5=data['successful'])
     val=(user_id,user_input_query,input_time,bot_response_time,successful,)
     mycursor.execute(sql,val)
     # print(obj)
     mydb.commit()
     print('Fetching the id of last query inserted')
     q_id=mycursor.lastrowid
     print(q_id)
     # print(entities)
     print('Fetching entity id from entities table and then inserting the mapping of query id and entitiy id in matcher table')
     for ent in entities:
          sql_fetch='SELECT {col1} FROM {table_name2} where {col2}="{0}";'.format(ent,col1=data['entity_id'],table_name2=data['entities'],col2=data['entity_name'])
          mycursor.execute(sql_fetch)
          ent_id=mycursor.fetchall()
          ent_id=ent_id[0][0]
          # print(ent_id,ent)
          sql_insert='INSERT INTO {table_name3} ({col1},{col2}) VALUES (%s,%s);'.format(table_name3=data['query_entity_matcher'],
          col1=data['query_id'],col2=data['entity_id'])
          val=(q_id,ent_id,)
          mycursor.execute(sql_insert,val)
          mydb.commit()
     return q_id     

def DataUpdate_feedback(id,option):
     data = load_data("D:/DataDiscovery_Bot/DataDiscovery_Bot/Database/MySQL/table.json")
     mydb = mysql.connector.connect(
          host="localhost",
           user="root",
            passwd="",
            database="user"
     )
     print("Feedback of user (Yes/No on basis of statisfaction of the bot response) is being inserted to bot performance metrics..")
     # print(id,option)

     mycursor = mydb.cursor()
     sql='UPDATE {table_name} SET {col1}=%s WHERE {col2}=%s;'.format(table_name=data['bot_performance_metrics'],col1=data['Feedback'],col2=data['query_id'])
     val=(option,int(id),)
     mycursor.execute(sql,val)
     # print(obj)
     mydb.commit()

def DataUpdate_comment(id,comment):
     data = load_data("D:/DataDiscovery_Bot/DataDiscovery_Bot/Database/MySQL/table.json")
     mydb = mysql.connector.connect(
          host="localhost",
           user="root",
            passwd="",
            database="user"
     )
     print("Feedback comments is being inserted to bot performance metrics..")

     mycursor = mydb.cursor()
     sql='UPDATE {table_name} SET {col1}=%s WHERE {col2}=%s;'.format(table_name=data['bot_performance_metrics'],col1=data['Comments'],col2=data['query_id'])
     val=(comment,int(id),)
     mycursor.execute(sql,val)
     # print(obj)
     mydb.commit()


          


     
