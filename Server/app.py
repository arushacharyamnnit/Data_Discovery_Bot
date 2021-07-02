from imports import *


app = Flask(__name__)
env_path= Path('.')/'.env'
load_dotenv(dotenv_path=env_path)


# Making connection with slack
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

    

client=slack.WebClient(token=os.environ['SLACK_TOKEN'])

QID=0

BOT_ID = client.api_call("auth.test")['user_id']


DefaultText="Sorry, we could not process your request!"

es = Elasticsearch([{'host':'localhost','port':'9200'}])
dict_index_fields = {}
indices_names=['test1','test','ocidw','ocidw_ent','glossary2']
for index in indices_names: 
    mapping = es.indices.get_mapping(index)
    dict_index_fields[index] = []
    for field in mapping[index]['mappings']['properties']:
        dict_index_fields[index].append(field)
dict_index_fields['test1'].remove('owner')
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/slack/feedback', methods=['POST'])
def feedback():
    print('feedback post request is being hit')
    global QID
    id=""
    option=""
    comment=""
    payload = json.loads(request.form["payload"])
    # pprint.pprint(payload)
    if "actions" in payload:
     print('user response to feedback question taken and passed to database' )
     option=payload["actions"][0]["selected_option"]["text"]["text"]
     id=payload["actions"][0]["selected_option"]["value"]
     
     if option=='Yes':
         QID=int(id)
     else:
         QID=int(id)-1    
     print(id)
     response = client.chat_delete(
     channel=payload["channel"]["id"],
     ts=payload["message"]["ts"]
     )
     DataUpdate_feedback(QID,option)
    
    # option=payload["actions"][0]["selected_option"]["text"]["text"]
    # print(option)
    if "payload" in request.form:
        payload = json.loads(request.form["payload"])
       
        
        

    if payload["type"] == "block_actions": 
    
      # Open a new modal by a global shortcut
      try:
        api_response = client.views_open(
          trigger_id=payload["trigger_id"],
          view={
            "type": "modal",
            "callback_id": "modal-id",
            "title": {
              "type": "plain_text",
              "text": "Feedback Info: "
            },
            "submit": {
              "type": "plain_text",
              "text": "Submit"
            },
            "close": {
              "type": "plain_text",
              "text": "Cancel"
            },
            "blocks": [
              {
                "type": "input",
                "block_id": "b-id",
                "label": {
                  "type": "plain_text",
                  "text": "Comments: ",
                },
                "element": {
                  "action_id": "a-id",
                  "type": "plain_text_input",
                }
              }
            ]
          }
        )
        return make_response("")
      except SlackApiError as e:
        code = e.response["error"]



        return make_response("")

    if payload["type"] == "view_submission":
      print('user feedback info is taken and passed to database' )  
      # Handle a data submission request from the modal
      submitted_data = payload["view"]["state"]["values"]
      comment=submitted_data["b-id"]["a-id"]["value"]
      print(comment)  # {'b-id': {'a-id': {'type': 'plain_text_input', 'value': 'your input'}}}
    #   print(QID)
      DataUpdate_comment(QID,comment)
    #   return make_response("")
    # print("coming?")
    
    return make_response("")


def ParseOutput(channel_id,output,flag,Counter,final_time):
    string=""
    
    for msg in output:
        string+=msg+'\n'

    if(Counter==0):
        client.chat_postMessage(channel=channel_id,text=DefaultText)
        flag=0
        final_time=time.time()

    if string=="" and flag:
        client.chat_postMessage(channel=channel_id,text=DefaultText)
        flag=0
        final_time=time.time()

    if string!="":  
        print('Output: ',string)
        client.chat_postMessage(channel=channel_id,text=string)
        final_time=time.time()    

    return flag,final_time


def FeedbackController(q_id,channel_id,resp):
    resp[0]["blocks"][0]["accessory"]["options"][0]["value"]=str(q_id)
    resp[0]["blocks"][0]["accessory"]["options"][1]["value"]=str(q_id+1)
    client.chat_postMessage(channel=channel_id,attachments=resp)        



msg_id = []

# @slack_event_adapter_feedback.on('block_actions')
# def block_actions(payload1):
    # print(payload1)
resp=[
		{
            
			"color": "#f2c744",
           
			"blocks": [
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "Were you satisfied with the results?"
					},
					"accessory": {
						"type": "radio_buttons",
						"options": [
							{
								"text": {
									"type": "plain_text",
									"text": "Yes",
									"emoji": True
								},
								"value": "q"
							},
							{
								"text": {
									"type": "plain_text",
									"text": "No",
									"emoji": True
								},
								"value": "value-2"
							}
						],
						"action_id": "radio_buttons-action"
					}
				}
			]
            
		}
	]

	


# Slack event
@slack_event_adapter.on('message')
def message(payload):
    flag=1
    event=payload.get('event',{})
    # print(payload["trigger_id"])

# Every user in the channel has its unindexique user id.
# and our bot will reply to every message which the users will send,
# so to avoid the response of bot to its own message and avoiding infinite loop
    if BOT_ID!=event.get('user'):
        mid = event.get('client_msg_id')
        # print(mid)
        msg_id.append(mid)
        count = msg_id.count(mid)
        if count <=1:
            channel_id=event.get('channel')
            user_id=event.get('user')
            initial_time=time.time()
            final_time=0
            user_input=event.get('text')


            user_input=str(user_input)

            # print(type(user_input))
            if user_input=="None":
                return make_response("")
            subr='<@'+BOT_ID+'>'
            # print(subr)
            subr=str(subr)
            user_input=re.sub(subr,'',str(user_input))
            

            print('User input fetched by Api: ', user_input)
    
            Queryhandler=QueryHandler()
            
            user_input=Queryhandler.PreprocessQuery(user_input)
            counter,string_id=Queryhandler.KeyWordExtractor(user_input)
            Modelloader=ModelLoader(dict_index_fields)
            ElasticSearchquery=ElasticSearchQuery()

            if(counter>1):
                client.chat_postMessage(channel=channel_id,text="Please choose only one keyword in your query for successful run") 
                return make_response("")
            #  If no keywords in the query    
            if(string_id==""):
                client.chat_postMessage(channel=channel_id,text="Please include either one of the keywords from 'catalog', 'job' or 'glossary' in your query for successful run of the bot")
                return make_response("")
            global QID
            QID=0


            if string_id=='job':
                print('Job model loaded...')
        

                
                lst=Modelloader.ExtractJobNamesAndAttributes(user_input)
                
                
                
                Counter,output,db_attributes=ElasticSearchquery.FetchJobResults(lst)

              
                # if(Counter==0):
                #    client.chat_postMessage(channel=channel_id,text="Sorry, we could not process your request!")
                #    final_time=time.time()
                #    flag=0

                
                flag,final_time=ParseOutput(channel_id,output,flag,Counter,final_time)
                if flag:
                    successful=1
                else:
                    successful=0
                response_time=final_time-initial_time
                print('Response Time: ', response_time)
                print('Updating Bot performance Metrics...')
                q_id=DataUpdate(user_id,user_input,db_attributes,initial_time,response_time,successful) # To update bot performance metrics table
                print('query_id: ',q_id)
                

                FeedbackController(q_id,channel_id,resp)

            elif string_id=='catalog':

                AttributeName,EntityName,Attributes,EntityAttributes=Modelloader.ExtractCatalogAndAttributes(user_input)
                
                
                output=ElasticSearchquery.FetchCatalogResults(AttributeName,EntityName,Attributes,EntityAttributes)

                for i in EntityAttributes:
                       Attributes.append(i)

                flag,final_time=ParseOutput(channel_id,output,flag,1,final_time)
                if flag:
                    successful=1
                else:
                    successful=0
                response_time=final_time-initial_time
                print('Response Time: ', response_time)
                print('Updating Bot performance Metrics...')
                q_id=DataUpdate(user_id,user_input,Attributes,initial_time,response_time,successful) # To update bot performance metrics table
                print('query_id: ',q_id)
                

                FeedbackController(q_id,channel_id,resp)        
               


            else:
                if string_id=='glossary':
                    print('Glossary model loaded...')
                # user_input=sp.spell_correct(user_input)['spell_corrected_text']


                
                lst=Modelloader.ExtractGlossaryNamesAndAttributes(user_input)
                print(lst)
                
                Counter,output,db_attributes=ElasticSearchquery.FetchGlossaryResults(lst)
                
                flag,final_time=ParseOutput(channel_id,output,flag,Counter,final_time)
                if flag:
                    successful=1
                else:
                    successful=0
                response_time=final_time-initial_time
                print('Response Time: ', response_time)
                print('Updating Bot performance Metrics...')
                q_id=DataUpdate(user_id,user_input,db_attributes,initial_time,response_time,successful) # To update bot performance metrics table
                print('query_id: ',q_id)
                

                FeedbackController(q_id,channel_id,resp)    
            return Response(),200    

                
@app.route('/NLP-metrics',methods=['POST'])
def NLP_metrics():
    data=request.form
    category=data['text']
    channel_id=data.get('channel_id')
    if(category=='job'):
        string=""
        fh=open('../NLP model/NLP_metrics.txt','r')
        for x in fh:
            x=x[:len(x)-1]
            string+=x+'\n'
        fh.close()
        client.chat_postMessage(channel=channel_id,text=string)
    elif category=='catalog':
        client.chat_postMessage(channel=channel_id,text="catalog")
    elif category=='glossary':
        client.chat_postMessage(channel=channel_id,text="glossary")
    else:
        client.chat_postMessage(channel=channel_id,text="Invalid parameter")

    return Response(),200


@app.route('/Bot-metrics',methods=['POST'])
def Bot_metrics():
    data=request.form
    channel_id=data.get('channel_id')
    res=metrics()
    res=json.dumps(res,indent=4)
    client.chat_postMessage(channel=channel_id,text=res)
    return Response(),200


@app.route('/Update-elasticsearch',methods=['POST'])
def Update_elasticsearch():
    data=request.form
    channel_id=data.get('channel_id')
    dict_index_fields={}
    for index in indices_names: 
        mapping = es.indices.get_mapping(index)
        dict_index_fields[index] = []
        for field in mapping[index]['mappings']['properties']:
            dict_index_fields[index].append(field)
    dict_index_fields['test1'].remove('owner')
    client.chat_postMessage(channel=channel_id,text="Updated elastic search...")
    return Response(),200        
            


if __name__=="__main__":
    app.run(debug=True,port=5000)    




