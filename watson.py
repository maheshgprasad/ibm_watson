import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from decouple import config

######### PARSE FROM ENV FILE ################
apikey = config('WATSON_API_KEY')
env_id = config('WATSON_ENVIRONMENT_ID')
w_service_url = config('WATSON_SERVICE_URL')
##############################################
## Assistant Config ##
auth = IAMAuthenticator(apikey)
assistant = AssistantV2(version='2021-06-14',authenticator=auth)
assistant.set_service_url(w_service_url)
##############################################

### Supportive functions ##

def json_extract(json_data = json , key = str):
    data = json.loads(json_data)
    value = data.get(key)
    return value

def nested_extract(json_data = json, lookup = str):
    json_data = json.dumps(json_data, indent=2)
    j_extract = json_extract(json_data, lookup)
    return j_extract

### Watson ##
# Start Session
def start_session(asst_id = str):
    session = assistant.create_session(assistant_id=asst_id).get_result()
    s_id = nested_extract(session, 'session_id')
    print(f"Session Created "+"| ID:  " + s_id)
    return s_id

# End Session
def close_session(asst_id = str, s_id = str):
  assistant.delete_session(assistant_id=asst_id, session_id=s_id).get_result()
  print("Session Closed"+ "| ID: " + s_id)

# Get Session ID (Scope: Global)
global session_id
session_id = start_session(env_id)

# Talk to watson
def watson(query = str):
    response = assistant.message(
        assistant_id=env_id,
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': query
        }
    ).get_result()
    response = nested_extract(response, 'output')  # Do not delete this if you dont know what you're doing
    response = nested_extract(response, 'generic') # Do not delete this if you dont know what you're doing
    watson_response = response[0]['text']          # Do not delete this if you dont know what you're doing
    return watson_response

################################################

def main(query = str):
    print(query)
    Continue = True
    while Continue is True:
        if ((query == "quit") or (query == "exit")):
            Continue = False
            print("Something Really Wrong")
            close_session(env_id, session_id)
        else:
            # print("Speaking to Watson")
            # Continue = False
            return watson(query)
    
# watson(query=input("you: "))

