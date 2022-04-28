import json
import boto3

    
#Function to update autoscaling groups
def update_auto_scaling_group(resource_id, MaxSize, MinSize, DesiredCapacity):
    #use boto3 function
    client = boto3.client('autoscaling',region_name='us-east-1')
    update_autoscaling = client.update_auto_scaling_group(
        AutoScalingGroupName= resource_id,
        MaxSize= int(MaxSize),
        MinSize= int(MinSize),
        DesiredCapacity= int(DesiredCapacity)
                    ) 
    return update_auto_scaling_group

def lambda_handler(event, context):
    #use boto3 function
    client = boto3.client('autoscaling',region_name='{}'.format(event['region']))
    
    #Special autoscaling groups
    ms_qa = "AutoScalingName"
    ms_uat = "AutoScalingName"
    ha_proxy = "AutoScalingName"

    
    #During the weekends we only scale-up those autoscaling groups, cost savings
    qa_weekends =  ["AutoScalingGroups",""]
    uat_weekends = ["AutoScalingGroups",""]
    
    if('{}'.format(event['Weekends']) == "yes"):
        #Scale UP during the weekends
        for i,b in zip(qa_weekends,uat_weekends):
            if('{}'.format(event['environment']) == "qa"):
                if(ms_qa == i):
                    update_autoscaling = update_auto_scaling_group(i,'{}'.format(event['MaxSizeQa']),'{}'.format(event['MinSizeQa']),'{}'.format(event['DesiredCapacityQa']))
                    print(update_autoscaling)
                else:
                    update_autoscaling = update_auto_scaling_group(i,'{}'.format(event['MaxSize']),'{}'.format(event['MinSize']),'{}'.format(event['DesiredCapacity']))
                    print(update_autoscaling)
            else:
                if(ms_uat == b):
                    update_autoscaling = update_auto_scaling_group(b,'{}'.format(event['MaxSizeUat']),'{}'.format(event['MinSizeUat']),'{}'.format(event['DesiredCapacityUat']))
                    print(update_autoscaling)
                else:
                    update_autoscaling = update_auto_scaling_group(b,'{}'.format(event['MaxSize']),'{}'.format(event['MinSize']),'{}'.format(event['DesiredCapacity']))
                    print(update_autoscaling)
    else:
        #Scale up during the week and scale down both during the weekend and week.
        # Get autoscaling groups by tags
        asg = client.describe_tags(
            Filters=[
                {
                    'Name': 'Value',
                    'Values': [
                       '{}'.format(event['environment']),
                              ],
                },
                    ],
        )
        
        #Get resource id to update autoscaling group
        resource_id = asg['Tags']
        for i in resource_id:
            resource_id = i["ResourceId"]
            
            #Down the environments
            if("{}".format(event['action']) == "down"):
                if(resource_id == ha_proxy ):
                    print("The instance " + resource_id + "should not be shut down.")
                else:
                #Update autoscaling group to down
                    update_autoscaling = update_auto_scaling_group(resource_id,'{}'.format(event['MaxSize']),'{}'.format(event['MinSize']),'{}'.format(event['DesiredCapacity']))
                    print(update_autoscaling)
            else:
                #Up microservices both QA and UAT
                if(ms_qa == resource_id):
                     update_autoscaling = update_auto_scaling_group(resource_id,'{}'.format(event['MaxSizeQa']),'{}'.format(event['MinSizeQa']),'{}'.format(event['DesiredCapacityQa']))
                     print(update_autoscaling)
                    
                elif(ms_uat == resource_id):
                    update_autoscaling = update_auto_scaling_group(resource_id,'{}'.format(event['MaxSizeUat']),'{}'.format(event['MinSizeUat']),'{}'.format(event['DesiredCapacityUat']))
                    print(update_autoscaling)
    
                else:
                    update_autoscaling = update_auto_scaling_group(resource_id,'{}'.format(event['MaxSize']),'{}'.format(event['MinSize']),'{}'.format(event['DesiredCapacity']))
                    print(update_autoscaling)



    