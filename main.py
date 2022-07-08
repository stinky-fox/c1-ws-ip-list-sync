#!/bin/python

'''
Scripter: Stinky Fox
Version: 0.1
Purpose:
    
'''


'''
Import necessary libraries
'''
import requests
import json
import sys
import os


'''
Function that acts as a manager to other functions.
'''

def elCapitan():
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
Call AbuseIP DB API. Requires API Key and confidence level.
'''
def abusedbApiCaller(config):
    url = 'https://api.abuseipdb.com/api/v2/blacklist?'
    apiHeaders = {'Accept': 'application/json', 'Key': config['apiKey']}
    queryParameter = 'confidenceMinimum=' + str(config['confidenceLevel'])
    apiUrl = url + queryParameter
    try:
        callApi = requests.get(apiUrl, headers=apiHeaders)
        converted = json.loads(callApi.content)
        if type(converted['data']) is list and len(converted['data']) != 0:
            return(converted)
        else:
            print('Empty response received' + str(converted))
            sys.exit()
    except Exception as errText:
        print("An error occured:" + str(errText))
        sys.exit()

'''
Build IP Address list
'''

def buildList(rawData):
    stackedIpList = []
    for record in range(len(rawData['data'])):
        stackedIpList.append(rawData['data'][record][ipAddress])
    return(stackedIpList)

'''
Call C1WS API to update permanent ban IP list
'''

def c1wsApiCaller(c1wsApi,newIpList):
    convertedIpList = json.dumps(newIpList)
    apiEndpoint = 'https://workload.' + c1wsApi[region] + '.cloudone.trendmicro.com/api/iplists/' + str(c1wsApi['ipListId'])
    apiHeaders = {'Content-type': 'application/json', 'api-version': c1wsApi['apiVersion'], 'api-secret-key': c1wsApi['apiKey']}
    apiPayload = '{"items":' + convertedIpList + '}'
    try:
        callApi = requests.post(apiEndpoint, data=apiPayload, headers=apiHeaders)
        if callApi.status_code == 200:
            message = "Status code: " + str(runApi.status_code) + ". IP List with ID: " + str(c1wsApi['ipListId']) + " was updated as follows"
        else:
            message = "Status code: " + str(runApi.status_code) + ". IP List with ID: " + str(c1wsApi['ipListId']) + " wasn't updated"
        return(message)
    except Exception as errText:
        print("An error occured:" + str(errText))
        sys.exit()
