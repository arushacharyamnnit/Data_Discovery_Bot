import mysql.connector
def metrics():
    mydb = mysql.connector.connect(
          host="localhost",
           user="root",
            passwd="",
            database="user"
    )
    dict={}
    import json
    def load_data(file):
     with open(file,"r",encoding="utf-8") as f:
       data=json.load(f)
     return data
     
    data = load_data("D:/DataDiscovery_Bot/DataDiscovery_Bot/Database/MySQL/table.json")

    # print('HELLO')
    mycursor = mydb.cursor()
    sql_success='SELECT COUNT(*) FROM {table_name} WHERE {col1}=1;'.format(table_name=data['bot_performance_metrics'],col1=data['successful'])
    mycursor.execute(sql_success)
    one=mycursor.fetchall()
    sql_fail='SELECT COUNT(*) FROM {table_name} WHERE {col1}=0;'.format(table_name=data['bot_performance_metrics'],col1=data['successful'])
    mycursor.execute(sql_fail)
    zero=mycursor.fetchall()

    sql_resp='SELECT AVG({col1}) FROM {table_name};'.format(table_name=data['bot_performance_metrics'],col1=data['bot_response_time'])
    mycursor.execute(sql_resp)
    resp=mycursor.fetchall()

    sql_satisfied='SELECT COUNT(*) FROM {table_name} WHERE {col1}="Yes";'.format(table_name=data['bot_performance_metrics'],col1=data['Feedback'])
    mycursor.execute(sql_satisfied)
    yes=mycursor.fetchall()
    sql_unsatisfied='SELECT COUNT(*) FROM {table_name} WHERE {col1}="No";'.format(table_name=data['bot_performance_metrics'],col1=data['Feedback'])
    mycursor.execute(sql_unsatisfied)
    no=mycursor.fetchall()

    dict['Successful Queries']=one[0][0]
    dict['Unsuccessful Queries']=zero[0][0]
    dict['Average of bot response time']=resp[0][0]
    dict['Queries where user was satisfied with the response']=yes[0][0]
    dict['Queries where user was not satisfied with the response']=no[0][0]

    mydb.commit()
    return dict
