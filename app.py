import json, requests, logging
from flask import Flask, request

logging.basicConfig(filename='webhook.log',level=logging.INFO)

EventAPI = 'https://insights-collector.newrelic.com/v1/accounts/<RPM ID (US)>/events'
InsertKey = '<Insert Key>'
EventType = 'Alerts'

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    body = request.data
    bodyParsed = json.loads(body)
    NRAccountID = str(bodyParsed['account_id'])
    NRAccountName = str(bodyParsed['account_name'])
    NRIncidentID = str(bodyParsed['incident_id'])
    NRConditionFamilyId = str(bodyParsed['condition_family_id'])
    NRConditionName = str(bodyParsed['condition_name'])
    NRCurrentState = str(bodyParsed['current_state'])
    NRDetails = str(bodyParsed['details'])
    NRDuration = str(bodyParsed['duration'])
    NREventType = str(bodyParsed['event_type'])
    try:
        NRLabels = bodyParsed['targets'][0]['labels']
        FlattenedLabels = flatten_json(str(NRLabels))
        labels = str(FlattenedLabels['']).replace('{', '').replace('}', '').replace("'", '')
        payload = [{
            "eventType": EventType, 
            "label_state": 'labels sent', 
            "account_id" : NRAccountID, 
            "labels_flattened": labels,
            "account_name": NRAccountName,
            "incident_id": NRIncidentID,
            "condition_family_id": NRConditionFamilyId,
            "condition_name": NRConditionName,
            "current_state": NRCurrentState,
            "details": NRDetails,
            "duration": NRDuration,
            "event_type": NREventType
        }]
    except:
        labelState = "no labels sent on incident ID: " + NRIncidentID
        logging.info(labelState)
        payload = [{"eventType": 'NrIntegrationError',"label_state": labelState, "account_id" : NRAccountID}]

    response = sendToInsights(payload)
    return response

def sendToInsights(payload):
    logging.debug(payload)
    response = requests.post(EventAPI, verify=True, headers={'Content-type':'application/octet-stream' ,'X-Insert-Key': InsertKey}, json=payload)
    logging.debug(response.text)
    return response.text

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)