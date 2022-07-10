#!/bin/python

'''
Scripter: Stinky Fox
Version: 0.1
Purpose:
    Query AbuseIPDB service via the provided API and later update IP List in Trend Micro Cloud One Workload Security.
    Initially designed to run in AWS Lambda or any other serverless but can be adjusted to run as a simple cron job.
    Requires free account on https://www.abuseipdb.com/ 
    Requires active subscription or trial account on https://cloudone.trendmicro.com
'''

#################### CODE BELOW THIS LINE #########################

'''
Import necessary libraries
'''
import requests
import json
import sys
import os


'''
Function to start the script
'''

def lambda_handler(event, context):
    c1wsConfig = {}
    c1wsConfig['apiKey'] = os.environ['C1WS_APIKEY']
    c1wsConfig['region'] = os.environ['C1WS_REGION']
    c1wsConfig['ipListId'] = os.environ['C1WS_IPLIST_ID']
    c1wsConfig['apiVersion'] = 'v1'
    
    abuseIpDbConfig = {}
    abuseIpDbConfig['apiKey'] = os.environ['ABUSEIPDB_APIKEY']
    abuseIpDbConfig['confidenceLevel'] = os.environ['ABUSEIPDB_CFDLVL']

    abusedbOutput = abusedbApiCaller(abuseIpDbConfig)
    newIpList = buildList(abusedbOutput)
    c1wsOutput = c1wsApiCaller(c1wsConfig,newIpList)

    print(c1wsOutput)

'''
Call AbuseIP DB API. 
Requires API Key and confidence level to be set.
Please follow AbuseIP DB for initital guide on Confidence Level.
'''
def abusedbApiCaller(config):
    url = 'https://api.abuseipdb.com/api/v2/blacklist?'
    apiHeaders = {'Accept': 'application/json', 'Key': config['apiKey']}
    queryParameter = 'confidenceMinimum=' + str(config['confidenceLevel'])
    apiUrl = url + queryParameter
    callApi = requests.get(apiUrl, headers=apiHeaders)
    converted = json.loads(callApi.content)
    try:
        callApi = requests.get(apiUrl, headers=apiHeaders)
        converted = json.loads(callApi.content)
    except Exception as errText:
        print("An error occured:" + str(errText))
        sys.exit()
    if 'errors' in converted:
        print('AbuseIP DB had returned an error: ' + str(converted['errors']))
        sys.exit()
    elif 'data' in converted:
        if type(converted['data']) is list and len(converted['data']) != 0:
            return(converted)
        else:
            print('Empty response in data field' + str(converted) + ". Abort!")
            sys.exit()
    else:
        print('Unknown use case, please inspect manually!')
        sys.exit()
'''
Separate function to extract IP Addresses from dictionary and build the list.
C1WS List maximum length is 32671 characters (32671/16=2041). 
This function extracts first 2040 IPs from abuseipdb report
'''

def buildList(rawData):
    stackedIpList = []
    for record in range(0, 2040):
        stackedIpList.append(rawData['data'][record]['ipAddress'])
    return(stackedIpList)

'''
Call C1WS API to update permanent ban IP list.
Requires IP List's ID (can be extracted from the URL or via any other API call).
'''

def c1wsApiCaller(c1wsApi,newIpList):
    convertedIpList = json.dumps(newIpList)
    apiEndpoint = 'https://workload.' + c1wsApi['region'] + '.cloudone.trendmicro.com/api/iplists/' + str(c1wsApi['ipListId'])
    apiHeaders = {'Content-type': 'application/json', 'api-version': c1wsApi['apiVersion'], 'api-secret-key': c1wsApi['apiKey']}
    apiPayload = '{"items":' + convertedIpList + '}'
    try:
        callApi = requests.post(apiEndpoint, data=apiPayload, headers=apiHeaders)
    except Exception as errText:
        print("An error occured:" + str(errText))
        sys.exit()
    if callApi.status_code == 200:
        message = "Status code: " + str(callApi.status_code) + ". IP List with ID: " + str(c1wsApi['ipListId']) + " was updated."
    else:
        message = "Status code: " + str(callApi.status_code) + ". IP List with ID: " + str(c1wsApi['ipListId']) \
            + " wasn't updated. Reason: " + str(callApi.content)
    return(message)


'''
Section to run script outside the serverless environment.
Uncomment lambda_handler('test', 'test') below.
'''
#lambda_handler('test', 'test')