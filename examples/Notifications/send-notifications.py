import base64
import pymsteams
import json
import os

def send_notification(event, context):
    #get variables
    name = os.environ.get('NAME')
    status =os.environ.get('STATUS')
    failures = json.loads(os.environ.get('FAILURES'))
    print(failures)
    if (status == "Failed" ):
        myTeamsMessage = pymsteams.connectorcard("Webhook")
        
        myTeamsMessageSection = pymsteams.cardsection()
        myTeamsMessageSection.title("Argo Workflow")
        myTeamsMessageSection.text("Last build failed")
        myTeamsMessageSection.activityTitle("Argo Workflow Failed")
        myTeamsMessageSection.activityImage("https://avatars.githubusercontent.com/u/38220399?s=200&v=4")
        myTeamsMessageSection.addFact("Name:", name)
        myTeamsMessageSection.addFact("Status:", status)
        myTeamsMessageSection.addFact("Failures:", failures)
        myTeamsMessageSection.addFact("Check the issue on Argo:", "https://argocd:2746/workflows/argo-events/"+name)
        
        myTeamsMessage.addSection(myTeamsMessageSection)
        myTeamsMessage.send()
    else:
        print("Status not expected")