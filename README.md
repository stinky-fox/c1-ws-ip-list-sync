# About
Sync IP addresses from AbuseIPDB and Trend Micro Cloud One Workload Security IP List.

# Requirments:

- Active account on https://www.abuseipdb.com/ and API key. Note that free tier allows only a limited amount of queries per day.
- Active account on https://cloudone.trendmicro.com
- Serverless service or server with python

# Variables

This script is using variables for API Keys, Regions and other. The following variables must be defined:
ABUSEIPDB_APIKEY= Your AbuseIP DB API Key. 
ABUSEIPDB_CFDLVL= Confidence Level (more https://docs.abuseipdb.com/#blacklist-endpoint)
C1WS_APIKEY= Your Cloud One Workload Security API key
C1WS_IPLIST_ID= The ID of IP list you're trying to update. Can be extracted from URL or via the API
C1WS_REGION= Your Cloud One Workload Security Region

# Usage as a scheduled task on any server

By default, code is ready to publish and use in a serverless environment. If you want to run it on, for example, Linux server as Cron job - uncomment the last line first!

# AWS Lambda serverless notes
AWS Lambda is missing *requests* library. In order to use this code - create & upload .zip file containing *requests* library and use it as a Layer. Example can be found here: https://medium.com/brlink/how-to-create-a-python-layer-in-aws-lambda-287235215b79
