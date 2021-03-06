# -*- coding: utf-8 -*-
"""ValueMomentumStrategy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GnDMnJe9hC1E4eUlwuF6O73WCikwK_Vt

https://developer-beta.morningstar.com/apis/getting-started/morningstar-apis

This link has all the documentation for using Morningtar's API - If you guys find any other resources throw it in here.

# **Morningstar Authorization**
"""

#pip install requests --upgrade --no-cache-dir

import requests, json, base64

USERNAME = #
PASSWORD = #

def getEncodedCredentials():
  # return 'ci5iaWxsaW5nc2xleUB2dC5lZHU6TURTZWVkMjExMiE='
  combined_credentials = USERNAME + ":" + PASSWORD
  credentials_bytes = combined_credentials.encode('ascii')
  base64_credentials = base64.b64encode(credentials_bytes)
  raw_string = str(base64_credentials)
  return raw_string.split("'")[1] # Remove unncessary crap
getEncodedCredentials()

#Authorization Token
#https://developer-beta.morningstar.com/apis/getting-started/authorization-tokens-api/1.0.0
#Use link above to create token then format curl command to requests
#Username: r.billingsley@vt.edu 
#Password: MDSeed2112!

#I feel like there should be an easier way to do this then having to go to the website every time

import requests, json, base64

headers = {
    'accept': '*/*',
    'Authorization': 'Basic ' + getEncodedCredentials()
}

auth_resp = requests.post('https://www.us-api.morningstar.com/token/oauth', headers=headers)

#Shows access token created
auth_resp_content = auth_resp.json()
auth_resp_content

#takes bytes and turns it intostring used for authorization
def getAuth():
  access_token = auth_resp_content["access_token"]
  token_type = auth_resp_content["token_type"]
  return token_type + (' ') + access_token
getAuth()

"""# **Morningstar Screener API - CANNOT GET ALL DATA - REFER TO MORNINGSTAR EXCEL DATA - KEEP FOR REFERENCE**
Screeener Pull Data
https://developer-beta.morningstar.com/apis/investment-analysis/screener-us/1.0.0/openapi-specification

Documentation: https://developer-beta.morningstar.com/apis/investment-analysis/screener-us/1.0.0/documentation
"""

#Use this box for trying to automate the authroization process for the screener

import requests
#Old Fashion Way of pulling data
headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1EY3hOemRHTnpGRFJrSTRPRGswTmtaRU1FSkdOekl5TXpORFJrUTROemd6TWtOR016bEdOdyJ9.eyJodHRwczovL21vcm5pbmdzdGFyLmNvbS9tc3Rhcl9pZCI6IjkzNjYyNkUxLTcxNTctNDJFQi1BOTM1LTk4QTk5NThBMzNEOSIsImh0dHBzOi8vbW9ybmluZ3N0YXIuY29tL2VtYWlsIjoiZWNkZW1vQG1haWxpbmF0b3IuY29tIiwiaHR0cHM6Ly9tb3JuaW5nc3Rhci5jb20vcm9sZSI6WyJBUEcuQW5hbHl0aWNzIiwiQVBHLlJpc2tNb2RlbCIsIkRldlMuQURFV2ViU2VydmljZXMiLCJFQy5BUEkuUmVwb3J0IiwiRUMuQVBJLlJlcG9ydC5QcmVzZW50YXRpb25TdHVkaW9Qb3J0Zm9saW8iLCJFQy5BUEkuVXNlckRhdGEuQWRtaW4iLCJFQy5BUEkuVXNlckRhdGEuQWR2aXNvciIsIkVDLkFQSS5Vc2VyRGF0YS5Vc2VyIiwiRUMuU2VydmljZS5Db25maWd1cmF0aW9uIiwiRUMuU2VydmljZS5EYXRhQWRhcHRlciIsIkVDVVMuQVBJLkF1dG9jb21wbGV0ZSIsIkVDVVMuQVBJLlJldGlyZW1lbnRQbGFuIiwiRUNVUy5BUEkuU2NyZWVuZXIiLCJFQ1VTLkFQSS5TZWN1cml0aWVzIiwiRmluYW5jaWFsUGxhbm5pbmcuRXh0ZXJuYWxQb3J0YWwiLCJGaW5hbmNpYWxQbGFubmluZy5Hb2FsQnJpZGdlIiwiRmluYW5jaWFsUGxhbm5pbmcuUG9ydGFsQWNjb3VudEFnZ3JlZ2F0aW9uIiwiRmluYW5jaWFsUGxhbm5pbmcuUG9ydGFsQ2FzaEZsb3dBbmFseXNpcyIsIkZpbmFuY2lhbFBsYW5uaW5nLlBvcnRhbEludmVzdG9yIiwiRnVuZFByb2R1Y3Rpb24uQXBpIiwiTGljZW5zZS5EV01DbGllbnRBY2NvdW50QW5hbHlzaXMiLCJMaWNlbnNlLlJpc2tNb2RlbEFkdmFuY2VkIiwiT0NSLkFQSSIsIlBBQVBJVjEuQWxsIiwiUEFBUElWMS5CZW5jaG1hcmsiLCJQQUFQSVYxLkNvcmUiLCJQQUFQSVYxLkh5cG8iLCJQQUFQSVYxLklEUiIsIlBBQVBJVjEuSW1wb3J0IiwiUEFBUElWMS5QZXJmb3JtYW5jZSIsIlBBQVBJVjEuUHJlbWl1bS5FU0ciLCJQQUFQSVYxLlByZW1pdW0uUmlza1Njb3JlIiwiUEFBUElWMS5SZXBvcnQiLCJQQUFQSVYxLlhyYXkiLCJQZXJzb25hLkRpcmVjdEZvckFzc2V0TWFuYWdlbWVudCIsIlBTLkFwaSIsIlJlc2VhcmNoQXBpLmVxdWl0eS5hZHZpc29yX3F1YWxfcmVwb3J0IiwiUmVzZWFyY2hBcGkuZXF1aXR5LmNvbXBhbnlfcmVwb3J0IiwiUmVzZWFyY2hBcGkuZXF1aXR5LmVuaGFuY2VkX3F1YW50X3JlcG9ydCIsIlJlc2VhcmNoQXBpLmVxdWl0eS5tb2F0X2ZyYW1ld29ya19yZXBvcnQiLCJSZXNlYXJjaEFwaS5lcXVpdHkucXVhbnRfcmVwb3J0IiwiUmVzZWFyY2hBcGkuZXF1aXR5LnN0b2NrX2FuYWx5c3Rfbm90ZSIsIlJlc2VhcmNoQXBpLmVxdWl0eS50aGVtYXRpY19yZXBvcnQiLCJSZXNlYXJjaEFwaS5lcXVpdHkudmFsdWF0aW9uX21vZGVsIiwiUmVzZWFyY2hBcGkuZnVuZC5jYXJib25fcmVwb3J0IiwiUmVzZWFyY2hBcGkuZnVuZC5lc2dfcmVwb3J0IiwiUmVzZWFyY2hBcGkuZnVuZC5ldGZfcmVwb3J0IiwiUmVzZWFyY2hBcGkuZnVuZC5nZnJfcmVwb3J0IiwiUmVzZWFyY2hBcGkuZnVuZC50YXJnZXRfZGF0ZV9yZXBvcnQiLCJQU1dFQiBBZG1pbiIsIkRpcmVjdCBJREMgQm9uZCBVc2VycyIsIkxpY2Vuc2UuQVBHUmlza01vZGVsIiwiUG9ydGZvbGlvIEFuYWx5c2lzIFVzZXIiXSwiaHR0cHM6Ly9tb3JuaW5nc3Rhci5jb20vY29tcGFueV9pZCI6ImNiYTc3OWFjLTA3OGEtNDZlNy1hZDMxLWQzODI5ZTdmM2E0OSIsImh0dHBzOi8vbW9ybmluZ3N0YXIuY29tL2ludGVybmFsX2NvbXBhbnlfaWQiOiJDbGllbnQwIiwiaHR0cHM6Ly9tb3JuaW5nc3Rhci5jb20vZGF0YV9yb2xlIjpbIkNCLkZ1bmRTdWl0YWJpbGl0eSIsIkVDLkRhdGEuQVUuRXhjaGFuZ2VUcmFkZWRGdW5kcyIsIkVDLkRhdGEuQVUuU3RvY2tzIiwiRUMuUmVwb3J0LkZhY3RzaGVldCIsIkVDLlJlcG9ydC5GdW5kQW5hbHlzdCIsIkVDLlJlcG9ydC5GdW5kRHVlRGlsaWdlbmNlIiwiRUMuUmVwb3J0LkludmVzdG1lbnRDb21wYXJlIiwiRUMuUmVwb3J0LlN0b2NrQW5hbHlzdCIsIkVDLlJlcG9ydC5TdG9ja0FuYWx5c3QuUXVhbnQiLCJFQy5SZXBvcnQuU3RvY2tEdWVEaWxpZ2VuY2UiLCJFQ1VTLkRhdGEuQ2FuYWRhLkJvbmRzIiwiRUNVUy5EYXRhLkNhbmFkYS5DbG9zZWRFbmRGdW5kcyIsIkVDVVMuRGF0YS5DYW5hZGEuRXhjaGFuZ2VUcmFkZWRGdW5kcyIsIkVDVVMuRGF0YS5DYW5hZGEuSGVkZ2VGdW5kcyIsIkVDVVMuRGF0YS5DYW5hZGEuT3BlbkVuZEZ1bmRzIiwiRUNVUy5EYXRhLkNhbmFkYS5Qb29sZWRGdW5kcyIsIkVDVVMuRGF0YS5DYW5hZGEuU2VncmVnYXRlZEZ1bmRzIiwiRUNVUy5EYXRhLkNhbmFkYS5TdG9ja3MiLCJFQ1VTLkRhdGEuVVMuNTI5UGxhbnMiLCJFQ1VTLkRhdGEuVVMuNTI5UG9ydGZvbGlvcyIsIkVDVVMuRGF0YS5VUy5CZW5jaG1hcmtzIiwiRUNVUy5EYXRhLlVTLkJvbmRzIiwiRUNVUy5EYXRhLlVTLkNJVHMiLCJFQ1VTLkRhdGEuVVMuQ2xvc2VkRW5kRnVuZHMiLCJFQ1VTLkRhdGEuVVMuRXhjaGFuZ2VUcmFkZWRGdW5kcyIsIkVDVVMuRGF0YS5VUy5HUlBBIiwiRUNVUy5EYXRhLlVTLkhlZGdlRnVuZHMiLCJFQ1VTLkRhdGEuVVMuSW5zdXJhbmNlRnVuZHMiLCJFQ1VTLkRhdGEuVVMuSkFOTkVZIiwiRUNVUy5EYXRhLlVTLkpBTk5FWS5BZHZpc2VyIiwiRUNVUy5EYXRhLlVTLkpBTk5FWS5BZHZpc2VyTVNQIiwiRUNVUy5EYXRhLlVTLkpBTk5FWS5KQ00iLCJFQ1VTLkRhdGEuVVMuSkFOTkVZLlBpb25lZXIiLCJFQ1VTLkRhdGEuVVMuTW9uZXlNYXJrZXQiLCJFQ1VTLkRhdGEuVVMuTW9ybmluZ3N0YXJJbmRleGVzIiwiRUNVUy5EYXRhLlVTLk9mZnNob3JlTXV0dWFsRnVuZHMiLCJFQ1VTLkRhdGEuVVMuT3BlbkVuZEZ1bmRzIiwiRUNVUy5EYXRhLlVTLlNlcGFyYXRlQWNjb3VudHMiLCJFQ1VTLkRhdGEuVVMuU3RvY2tzIiwiRUNVUy5EYXRhLlVTLlVuaXRJbnZlc3RtZW50VHJ1c3QiLCJFQ1VTLkRhdGEuVVMuVkFDb250cmFjdHMiLCJFQ1VTLkRhdGEuVVMuVmFyaWFibGVMaWZlIiwiRUNVUy5EYXRhLlVTLlZBU3ViYWNjb3VudHMiLCJQQUFQSVYxLkVTRy5DYXJib24iLCJQQUFQSVYxLkVTRy5DYXJib24uRXF1aXR5IiwiUEFBUElWMS5FU0cuRVNHUmlzayIsIlBBQVBJVjEuRVNHLkVTR1Jpc2suRXF1aXR5IiwiUEFBUElWMS5FU0cuRVVTRkRSIiwiUEFBUElWMS5FU0cuRVVUYXhvbm9teSIsIlBBQVBJVjEuRVNHLlByb2R1Y3RJbnZvbHZlbWVudCIsIlBBQVBJVjEuRVNHLlByb2R1Y3RJbnZvbHZlbWVudC5FcXVpdHkiLCJRUy5NYXJrZXRzIiwiUVMuUHVsbHFzIiwiU0FMLlNlcnZpY2UiXSwiaHR0cHM6Ly9tb3JuaW5nc3Rhci5jb20vbGVnYWN5X2NvbXBhbnlfaWQiOiJjYmE3NzlhYy0wNzhhLTQ2ZTctYWQzMS1kMzgyOWU3ZjNhNDkiLCJodHRwczovL21vcm5pbmdzdGFyLmNvbS9jb25maWdfaWQiOiJFQ0RFTU9fRUMiLCJodHRwczovL21vcm5pbmdzdGFyLmNvbS9yb2xlX2lkIjpbImRjZjE5NjQwLWJjOGYtNDQxOS05Zjk0LTFhMDIwNTI0MDc3YyIsIjhmZWNjNWVmLWEyNTYtNGUwMi05Nzc2LTIxYWFmOTA5MDZlNiIsImVmNTVmZDE5LTAxZGItNDgwMy04MWMxLTVkZTBjZjJmMmIxOSIsIjQxNjM3MzE4LTMzMzctNDRjMC04OTkyLTZlMWViZDE0NjgxZCIsIjMyMmVlYjg2LTg1YWYtNDk0Ny1iMDVkLTc5Nzg2NDY3ZDE2YiIsImYyOTQ2NjQ2LTJmZDItNDhkNS1hNjQzLTg0ZDBkMjYxZTFmNyIsImMwNjY3ZDdhLWY1ODctNGZkNy1hYWRhLWEyNWYwZDcxOWFmYyIsIjVjZjBlMjk0LTk0MmYtNDIyNS1iMDkyLWM4YmI5MjQxZDA1NiIsImRjMzE3ZDk4LTExMDAtNDIzZi05NTNmLWZmNGRiNzgzNTAxOCIsImNiMGRmYmQ3LWI4OTQtNDJlZC1hZDNkLTA2NzBiNjFkNWIxNSIsIjlmZGI3ZTU1LTk4MjAtNGRmYy05ZDk5LTA3YTJiN2JiZDYzZSIsIjE3ZGZjZjM1LTBjODctNGQ0YS1hODg4LTI2N2NhMTk4ZTcxOSIsImQzNzBkYzRhLWM3ZjktNDMyNy04OGRmLTMyODNmNDVlZDJiYyIsIjZhNjg4ODBhLTE2ZjctNDFiOC1hMmViLThmZTUyMzM1OTIxYyJdLCJodHRwczovL21vcm5pbmdzdGFyLmNvbS9wcm9kdWN0IjpbIkRJUkVDVCIsIlBTIl0sImh0dHBzOi8vbW9ybmluZ3N0YXIuY29tL2NvbXBhbnkiOlt7ImlkIjoiY2JhNzc5YWMtMDc4YS00NmU3LWFkMzEtZDM4MjllN2YzYTQ5IiwicHJvZHVjdCI6IkRJUkVDVCJ9XSwiaHR0cHM6Ly9tb3JuaW5nc3Rhci5jb20vdWltX3JvbGVzIjoiQ1dQX0FEVklTT1IsRE9UX0NPTV9GUkVFLE1EX01FTUJFUl8xXzEiLCJpc3MiOiJodHRwczovL2xvZ2luLXByb2QubW9ybmluZ3N0YXIuY29tLyIsInN1YiI6ImF1dGgwfDkzNjYyNkUxLTcxNTctNDJFQi1BOTM1LTk4QTk5NThBMzNEOSIsImF1ZCI6WyJodHRwczovL2F1dGgwLWF3c3Byb2QubW9ybmluZ3N0YXIuY29tL21hYXMiLCJodHRwczovL3VpbS1wcm9kLm1vcm5pbmdzdGFyLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2NDYwNjc3NzEsImV4cCI6MTY0NjA3MTM3MSwiYXpwIjoiaVFrV3hvYXBKOVB4bDhjR1pMeWFYWnNiWFY3OWc2NG0iLCJzY29wZSI6Im9wZW5pZCIsImd0eSI6InBhc3N3b3JkIn0.DQbcnYmL0EwK6cbPF4VhSqVc9lJepfge_0Gyc3bLBgIydF8IPg762L_edtoL23GbXEGXt56w4WmYrdNe02tbmTbohP6-j3rPDgCMSeHBsBkFpKxf4uWqOZsFbBkHZZ2CeRyuKKoH8YkuignN6SRkTUUwFeX8lGZNVRUG4fIznjHnZrwoQ-s8i9_0D77mWnQ8zKnsEAZW-HAavZ2OOnSTl20FrjN-xZoHnOGC1imxT7_iTgi5-MkCD_30uIHFsHPAbVRv2Zfp-Eo-D9kFnjCXLvA5W5Xsj472gJrQknmQ7RHkrNzJ5oo7t0-KYctIfH_fmIJwY3bDutIofw9V4d3ZQg'
}

#Still Need: FCF T12M, Total Assets of last Q, Net Income of last Q, FCF of last Q, Operating Cash Flow T12M
#Pulled: Net Income T12M,  Market Cap,  Beta, Closed Price

params = (
    ('results', '100' ), #Number of stocks that return
    #('sort', 'marketCap'),
    #('dir', 'asc'),
    #('stdFilters', 'true'),
    #('securityDataPoints', 'securities.list'),
    ('universe', 'STUSA'),
    ('securityDataPoints', 'legalName|ticker|closePriceMarkets|priceEarningsRatio|pbRatio|priceSalesRatio|dividendYield|marketCap|returnM12|stbm5y|stnittm|fcfmktcap|stfhg|gicssector|stgg|pegRatio|totrevy|totrevcumqtr1|strttm|stpg|returnOnAssets|returnOnEquity|statn1y|cfpsttm|stso|debtEquityRatio|stgmy1|roicYear1'),
    #('filters', 'marketCap:{"min":"1","max":"500"}}')
)

screener_resp = requests.get('https://www.us-api.morningstar.com/ec/v1/screener', headers=headers, params=params)
screener_resp

from numpy import MachAr
import pandas as pd

screenData = screener_resp.json()
SDS = screenData["securities"]["s"]
SDS

SDSDF = pd.DataFrame.from_dict(SDS)
#SDSDF = SDSDF.set_index('ticker')
SDSDF = SDSDF.rename(columns={'stbm5y' : 'Beta5Y', 
                              'stnittm' : 'NetIncomeTTM', 
                              'fcfmktcap' : 'FCF/MarketCap',
                              'stfhg' : 'FinancialHealthGrade',
                              'stgg' : 'GrowthGrade',
                              'marketCap' : 'MarketCap',
                              'totrevy' : 'TotalRevenueFY1',
                              'totrevcumqtr1' : 'TotalRevenueLastQ',
                              'strttm' : 'TotalRevenueTTM',
                              'stpg' : 'ProfitabilityGrade',
                              'returnOnAssets' : 'returnOnAssetsTTM',
                              'returnOnEquity' : 'returnOnEquityTTM',
                              'statn1y' : 'AssetTurnoverFY1',
                              'cfpsttm' : 'CashFlow/ShareTTM',
                              'stso' : 'SharesOutstanding',
                              'stgmy1' : 'GrossMargin%FY1',
                              'roicYear1' : 'Gross Margin % 1 Yr - FY1'

})


SDSDF[['MarketCap', 'FCF/MarketCap', 'returnOnEquityTTM', 'returnOnAssetsTTM', 'CashFlow/ShareTTM', 'SharesOutstanding']] = SDSDF[['MarketCap', 'FCF/MarketCap', 'returnOnEquityTTM', 'returnOnAssetsTTM', 'CashFlow/ShareTTM', 'SharesOutstanding']].astype('float')

SDSDF[['FCF/MarketCap', 'returnOnEquityTTM', 'returnOnAssetsTTM']] = SDSDF[['FCF/MarketCap', 'returnOnEquityTTM', 'returnOnAssetsTTM']] * 0.01 #Changing from % to decimal
#SDSDF[['MarketCap']] = SDSDF[['MarketCap']] * 1000000 #Changing from (mil) to dollar

# Probably Inacurate 
SDSDF['FCF'] = SDSDF['MarketCap'] * SDSDF['FCF/MarketCap']
SDSDF['CashFlowTTM'] = SDSDF['SharesOutstanding'] * SDSDF['CashFlow/ShareTTM'] 

SDSDF

"""# **Pull SP500 Tickers - Use to make sure SP500 Holdings are upt to date**"""

#pulls list of s&p500 tickers and puts it into excel sheet that will be used to pull data from morningstar

import pandas as pd

def get_sp500():
	sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	sp500_tickers = sp500_tickers[0]

	tickers = sp500_tickers['Symbol'].values.tolist()
	return tickers

sp500_tickers = get_sp500()

sp500tickersdf = pd.DataFrame()

sp500tickersdf = sp500tickersdf.append(sp500_tickers)

sp500tickersdf = sp500tickersdf.rename(columns={0 : 'tickers'})

sp500tickersdf = sp500tickersdf.set_index('tickers')

#sp500tickersdfT = sp500tickersdf.T

#sp500tickersdf.to_excel('SP500_tickers.xlsx')

#from google.colab import files

#files.download("SP500_tickers.xlsx")

#Downloads straight to computer

range(len(sp500tickersdf))

sp500tickersdf

"""# **TDAmeritrade API**"""

import pandas as pd
import requests
import json
from datetime import datetime

td_consumer_key = '81O0HHNVHPMJABUCA975UFRPMPSKJXVG'

endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'

full_url = endpoint.format(stock_ticker='MMM',periodType='year',period=1,frequencyType='daily',frequency=1)

page = requests.get(url=full_url,
                    params={'apikey' : td_consumer_key})

info = json.loads(page.content)

#Makes DF from content pulled
edinfo = info['candles']
edinfoDF = pd.DataFrame.from_dict(edinfo)
infoDF = pd.DataFrame.from_dict(info)
comboDF = pd.concat([infoDF, edinfoDF], axis=1)

#convert epoch time to datetime
DateTime = comboDF.datetime

for time in range(len(comboDF)):
  seconds = DateTime[time]
  Date = datetime.fromtimestamp(seconds/1000).strftime("%m/%d/%Y")
  comboDF.loc[comboDF.index[time], 'Date'] = Date

#daily return calculation
Close = comboDF.close
Open = comboDF.open

for yut in range(len(comboDF)):
  close = Close[yut]
  open = Open[yut]
  dailyret = (close - open) / (open)
  comboDF.loc[comboDF.index[yut], 'Daily Return'] = dailyret

#data cleaning DF
cleanCDF = comboDF.drop(['high','low','volume','candles','empty','open','close','datetime'], axis = 1)
cleanCDF = cleanCDF.set_index('Date')

symbol = cleanCDF.symbol[0]
cleanCDF=cleanCDF.rename(columns = {'Daily Return':symbol})

finaltestCDF = cleanCDF.drop('symbol', axis=1)

finaltestCDF

#for loop to collect data from every stock in S&P
import pandas as pd
import requests
import json
from datetime import datetime

td_consumer_key = '81O0HHNVHPMJABUCA975UFRPMPSKJXVG'

endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'

a={}
for i in range(0,100):
  tickers = sp500tickersdf.index
  Ticker = tickers[i]
  full_url = endpoint.format(stock_ticker=Ticker,periodType='year',period=1,frequencyType='daily',frequency=1)
  page = requests.get(url=full_url,
                    params={'apikey' : td_consumer_key})
  content = json.loads(page.content)
  a[i] = pd.DataFrame.from_dict(content)

a

import pandas as pd
import requests
import json
from datetime import datetime

td_consumer_key = '81O0HHNVHPMJABUCA975UFRPMPSKJXVG'

endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'

b={}
for i in range(100,200):
  tickers = sp500tickersdf.index
  Ticker = tickers[i]
  full_url = endpoint.format(stock_ticker=Ticker,periodType='year',period=1,frequencyType='daily',frequency=1)
  page = requests.get(url=full_url,
                    params={'apikey' : td_consumer_key})
  content = json.loads(page.content)
  b[i] = pd.DataFrame.from_dict(content)

b

import pandas as pd
import requests
import json
from datetime import datetime

td_consumer_key = '81O0HHNVHPMJABUCA975UFRPMPSKJXVG'

endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'

ce={}
for i in range(200,300):
  tickers = sp500tickersdf.index
  Ticker = tickers[i]
  full_url = endpoint.format(stock_ticker=Ticker,periodType='year',period=1,frequencyType='daily',frequency=1)
  page = requests.get(url=full_url,
                    params={'apikey' : td_consumer_key})
  content = json.loads(page.content)
  ce[i] = pd.DataFrame.from_dict(content)

ce

from pandas.core.indexers import deprecate_ndim_indexing
import pandas as pd
import requests
import json
from datetime import datetime

td_consumer_key = '81O0HHNVHPMJABUCA975UFRPMPSKJXVG'

endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'

d={}
for i in range(300,400):
  tickers = sp500tickersdf.index
  Ticker = tickers[i]
  full_url = endpoint.format(stock_ticker=Ticker,periodType='year',period=1,frequencyType='daily',frequency=1)
  page = requests.get(url=full_url,
                    params={'apikey' : td_consumer_key})
  content = json.loads(page.content)
  d[i] = pd.DataFrame.from_dict(content)

d

import pandas as pd
import requests
import json
from datetime import datetime

td_consumer_key = '81O0HHNVHPMJABUCA975UFRPMPSKJXVG'

endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'

e={}
for i in range(400,500):
  tickers = sp500tickersdf.index
  Ticker = tickers[i]
  full_url = endpoint.format(stock_ticker=Ticker,periodType='year',period=1,frequencyType='daily',frequency=1)
  page = requests.get(url=full_url,
                    params={'apikey' : td_consumer_key})
  content = json.loads(page.content)
  e[i] = pd.DataFrame.from_dict(content)

e

import pandas as pd
import requests
import json
from datetime import datetime

td_consumer_key = '81O0HHNVHPMJABUCA975UFRPMPSKJXVG'

endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/pricehistory?periodType={periodType}&period={period}&frequencyType={frequencyType}&frequency={frequency}'

f={}
for i in range(500,504):
  tickers = sp500tickersdf.index
  Ticker = tickers[i]
  full_url = endpoint.format(stock_ticker=Ticker,periodType='year',period=1,frequencyType='daily',frequency=1)
  page = requests.get(url=full_url,
                    params={'apikey' : td_consumer_key})
  content = json.loads(page.content)
  f[i] = pd.DataFrame.from_dict(content)

f

#merging dicts together
z = {**a, **b, **ce, **d, **e, **f}
z

#data cleaning for event discreteness

EDSDDF = pd.DataFrame(index = finaltestCDF.index)

for w in range(0,504):
  infoDF = z[w]
  candleDF = z[w].candles.apply(pd.Series)
  comboDF = pd.concat([infoDF, candleDF], axis=1)
  #convert epoch time to datetime
  DateTime = comboDF.datetime
  for time in range(len(comboDF)):
    seconds = DateTime[time]
    Date = datetime.fromtimestamp(seconds/1000).strftime("%m/%d/%Y")
    comboDF.loc[comboDF.index[time], 'Date'] = Date
  #daily return calculation
  Close = comboDF.close
  Open = comboDF.open
  for yut in range(len(comboDF)):
    close = Close[yut]
    open = Open[yut]
    dailyret = ((close - open) / (open))
    comboDF.loc[comboDF.index[yut], 'Daily Return'] = dailyret
  #data cleaning DF
  cleanCDF = comboDF.drop(['high','low','volume','candles','empty','open','close','datetime'], axis = 1)
  cleanCDF = cleanCDF.set_index('Date')
  symbol = cleanCDF.symbol[0]
  cleanCDF=cleanCDF.rename(columns = {'Daily Return':symbol})
  finalCDF = cleanCDF.drop('symbol', axis=1)
  tickers = sp500tickersdf.index
  Ticker = tickers[w]
  EDSDDF.loc[finalCDF.index, Ticker] = finalCDF[Ticker]

EDSDDF

"""# **Event Discretness**
https://alphaarchitect.com/2015/11/23/frog-in-the-pan-identifying-the-highest-quality-momentum-stocks/

arg1:num eventdiscreteness over arg2:num tolerance arg3:num
arg1 eventdiscreteness arg2 tolerance arg3 measures how many days the arg1 moves in the same direction as the overall trend, minus the number of days it moves against. All moves with absolute value smaller than arg3 are not counted.

Take closing price over a period and count the number of days its moving in an upward trend - the number of days it goes in the opposite direction
"""

import math
import numpy as np
import operator
import functools

EDList = EDSDDF['MMM'].tolist()
EDList
CumDR = np.prod(EDList)
CumDR = CumDR - 1
if CumDR > 0:
  SignCumDR = 1
else:
  SignCumDR = -1

pos_count, neg_count = 0, 0
for num in EDList:
  if num > 0:
    pos_count += 1
  if num < 0:
    neg_count += 1

DID = SignCumDR * (neg_count - pos_count)
DID

#EDDFT = EDDF.T
#EDDFTRI = EDDFT.reset_index()
#EDDFTRI

#multiply daily returns together
#if positive then use 1
#if negative use -1

"""# **Morningstar Excel Data**

**Going to be doing most of this in jupytier notebook bc its easier with exporting and importing excel files - will update after completed.**

Documentation: 

*   https://morningstardirect.morningstar.com/clientcomm/ExcelAPICheatsheetMMDDYYYY.pdf
*   https://excelapi.morningstar.com/index.html
*https://morningstardirect.morningstar.com/clientcomm/Morningstar_Excel_Add-In_Reference-Guide.pdf

**Pulls Data from Excel Sheet**
"""

#Need to upload excel file to files table on left side of screen in order to import DF

import pandas as pd

SP500DF = pd.read_excel('SP500_Data.xlsx', 'SP500_Data')
SP500DF.columns = SP500DF.iloc[0]
SP500DF = SP500DF[1:]
SP500DF = SP500DF.reset_index(drop=True)

SP500DF

"""**Data Cleaning**"""

#replaces -N/A with NaN
SP500DF[['Net Income LY','Total Assets LY','Long Term Debt','Long Term Debt LY',
         'Current Ratio','Current Ratio LY','Shares Outstanding (Mil)','Shares Outstanding LY (Mil)',
         'Gross Margin % LY','Asset Turnover Ratio','Asset Turnover Ratio LY',
         'Gross Margin % TTM','Gross Margin % LQ','Total Debt / Total Equity LQ','Total Assets (Mil) LQ','ROA TTM','Operating Cash Flow TTM','Total Assets','Net Income TTM (Mil)','FCF TTM','Net Income LQ (Mil)','Beta 3Y Qtr-End','ROA % LY','ROIC % TTM','P/B Daily','P/E Daily','EV (Mil)']] = SP500DF[['Net Income LY','Total Assets LY','Long Term Debt','Long Term Debt LY','Current Ratio','Current Ratio LY','Shares Outstanding (Mil)','Shares Outstanding LY (Mil)','Gross Margin % LY','Asset Turnover Ratio','Asset Turnover Ratio LY','Gross Margin % TTM','Gross Margin % LQ','Total Debt / Total Equity LQ','Total Assets (Mil) LQ','ROA TTM','Operating Cash Flow TTM','Total Assets','Net Income TTM (Mil)','FCF TTM','Net Income LQ (Mil)','Beta 3Y Qtr-End','ROA % LY','ROIC % TTM','P/B Daily','P/E Daily','EV (Mil)']].replace(['-N/A'],'NaN')

#turns data to float64
SP500DF[['ROA TTM','Operating Cash Flow TTM','Total Assets','Net Income LY','Total Assets LY',
         'Long Term Debt','Long Term Debt LY','Current Ratio','Current Ratio LY','Shares Outstanding (Mil)',
         'Shares Outstanding LY (Mil)','Gross Margin % LY','Asset Turnover Ratio',
         'Asset Turnover Ratio LY','Gross Margin % TTM','Gross Margin % LQ','Total Debt / Total Equity LQ','Net Income TTM (Mil)','FCF TTM','Net Income LQ (Mil)','Beta 3Y Qtr-End','ROA % LY','ROIC % TTM','P/B Daily','P/E Daily','EV (Mil)']] = SP500DF[['ROA TTM','Operating Cash Flow TTM','Total Assets','Net Income LY','Total Assets LY','Long Term Debt','Long Term Debt LY','Current Ratio','Current Ratio LY','Shares Outstanding (Mil)','Shares Outstanding LY (Mil)','Gross Margin % LY','Asset Turnover Ratio','Asset Turnover Ratio LY','Gross Margin % TTM','Gross Margin % LQ','Total Debt / Total Equity LQ','Net Income TTM (Mil)','FCF TTM','Net Income LQ (Mil)','Beta 3Y Qtr-End','ROA % LY','ROIC % TTM','P/B Daily','P/E Daily','EV (Mil)']].astype('float')
SP500DF

"""# **Standard Deviation - NEEDS Editing**"""

#calculating standard deviation and adding it to dataframe

#use log to normalize/transform the data

import math
import numpy as np
import operator
import functools
import statistics
import matplotlib.pyplot as plt

for yip in range(0,504):
  tickers = sp500tickersdf.index
  Ticker = tickers[yip]
  SDList = EDSDDF[Ticker].tolist()
  SDstdev = statistics.stdev(SDList)
  SP500DF.loc[SP500DF.index[yip], 'Standard Deviation'] = SDstdev

logSTDEV = np.log(SP500DF['Standard Deviation'])

fig7 = plt.figure()
ax7 = fig7.add_subplot(1, 1, 1)
n, bins, patches = ax7.hist(logSTDEV)
ax7.set_xlabel('Log of Standard Deviation of Daily Returns')
ax7.set_ylabel('Frequency')

#percentiles of standard deviations to find optimal stop loss

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics

STDEV = SP500DF['Standard Deviation']

#fig6 = plt.figure()
#ax6 = fig6.add_subplot(1, 1, 1)
#n, bins, patches = ax6.hist(STDEV)
#ax6.set_xlabel('Standard Deviation of Daily Returns')
#ax6.set_ylabel('Frequency')

SP500DF['STDEV PCT'] = STDEV.rank(pct=True)
STDEVPCT = SP500DF['STDEV PCT']
SP500DF['Optimal Stop Loss'] = ((STDEVPCT*100)/10) + 10

df1 = SP500DF[['tickers', 'Optimal Stop Loss']]
df1

"""# **Piotroski F Score - NEED TO DOUBLE CHECK DATA OF CALS**
One point assigned to F-Score for each true condition--0 weak to 9 strong.

Profitability
- Positive Return on Assets (ROA) 
    ROA T12M = [(Net Income T12M * 1) / (Average of Total Assets 1Q and 5Q) * 100] > 0
- Positive Operating Cash Flow
    CRROA T12M = [Operating Cash Flow T12M / Average of Total Assets 1Q and 5Q) * 100] > 0
- Current ROA higher than a year ago
    ROA T12M > ROA 251 Days Ago
- CFROA greater than ROA - Improved accruals
    CFROA T12M > ROA T12M
    
Funding
- Current Long Term Debt to Assets less than a year ago (gearing or leverage)
- Current Ratio is higher than a year ago - (current assets / current liabilities - improved liquidity or working capital)
- No increase in number of shares outstanding

Efficiency
- Higher Gross Margin than a year ago (Sales - Cost of Goods)
- Higher Asset Turnover Ratio than a year ago (Sales / Assets at start of year)
"""

#Formula Calculation of Piotroski F Scoce

#Calcs
SP500DF['LTDTA'] = (SP500DF['Long Term Debt'] / SP500DF['Total Assets']) * 100
SP500DF['LTDTA LY'] = (SP500DF['Long Term Debt LY'] / SP500DF['Total Assets LY']) * 100
SP500DF['Average Assets TTM'] = (SP500DF['Total Assets'] + SP500DF['Total Assets LY']) / 2
SP500DF['CFROA TTM'] = (SP500DF['Operating Cash Flow TTM'] / SP500DF['Average Assets TTM']) * 100

#ForLoop PFScore
for steps in range(len(SP500DF)):
  PFScore = 0
  ROA = SP500DF['ROA TTM']
  ROA = ROA[steps]
  if ROA > 0:
    PFScore += 1
  CFROA = SP500DF['CFROA TTM']
  CFROA = CFROA[steps]
  if CFROA > 0:
    PFScore += 1
  ROALY = SP500DF['ROA % LY']
  ROALY = ROALY[steps]
  if ROA > ROALY:
    PFScore += 1
  if CFROA > ROA:
    PFScore += 1
  LTDTA = SP500DF['LTDTA']
  LTDTA = LTDTA[steps]
  LTDTALY = SP500DF['LTDTA LY']
  LTDTALY = LTDTALY[steps]
  LTD = SP500DF['Long Term Debt']
  LTD = LTD[steps]
  if LTDTA < LTDTALY or LTD <= 0:
    PFScore += 1
  CR = SP500DF['Current Ratio']
  CR = CR[steps]
  CRLY = SP500DF['Current Ratio LY']
  CRLY = CRLY[steps]
  if CR > CRLY:
    PFScore += 1
  SO = SP500DF['Shares Outstanding (Mil)']
  SO = SO[steps]
  SOLY = SP500DF['Shares Outstanding LY (Mil)']
  SOLY = SOLY[steps]
  if SO <= SOLY:
    PFScore += 1
  GM = SP500DF['Gross Margin % TTM']
  GM = GM[steps]
  GMLY = SP500DF['Gross Margin % LY']
  GMLY = GMLY[steps]
  if GM > GMLY:
    PFScore += 1
  ATR = SP500DF['Asset Turnover Ratio']
  ATR = ATR[steps]
  ATRLY = SP500DF['Asset Turnover Ratio LY']
  ATRLY = ATRLY[steps]
  if ATR > ATRLY:
    PFScore += 1
  SP500DF.loc[SP500DF.index[steps], 'PiotroskiFScore'] = PFScore

SP500DF

#SP500DF[(SP500DF['PiotroskiFScore'] >= 7)]

"""# **Rank of Asset Turnover LQ across Industry where True > 65**

Need to create seperate dataframes for each industry of Asset Turnover LQ

*Hint* : Asset Turnover LQ = Asset Turnover Ratio

**Can't Pull GICS industries for some reason**
"""

ATRS = SP500DF[['tickers','Asset Turnover Ratio','Industry']]
ATRS["Industry"].value_counts()

import numpy as np

ATRI = [x for _, x in ATRS.groupby('Industry')]

for wet in range(len(ATRI)):
  ATRIDF = ATRI[wet]
  ATR = ATRIDF['Asset Turnover Ratio']
  ATRIDF['Asset Turnover Ratio Industry PCT'] = ATR.rank(pct=True)
  SP500DF.loc[ATRIDF.index, 'Asset Turnover Ratio Industry PCT'] = ATRIDF['Asset Turnover Ratio Industry PCT']

SP500DF

"""# **Value Strategy - Screener**

**Calculations**
"""

#(NetIncomeTTM - FCFTTM) / (TotalAssetsLQ) Calc
NetIncomeTTM = SP500DF['Net Income TTM (Mil)'] * 1000000
FCFTTM = SP500DF['FCF TTM']
TotalAssetsLQ = SP500DF['Total Assets (Mil) LQ'] * 1000000
SP500DF['TTMNIFCFTA'] = (NetIncomeTTM - FCFTTM) / (TotalAssetsLQ)

#(NetIncomeLQ - FCFLQ) / (TotalAssetsLQ) Calc
NetIncomeLQ = SP500DF['Net Income LQ (Mil)'] * 1000000
FCFLQ = SP500DF['FCF LQ (Mil)'] * 1000000
SP500DF['LQNIFCFTA'] = (NetIncomeLQ - FCFLQ) / (TotalAssetsLQ)

#(OperatingCashFlowTTM) / (RawClose) Calc
OCFTTM = SP500DF['Operating Cash Flow TTM']
RC = SP500DF['Price']
SP500DF['OCFRC'] = (OCFTTM) / (RC)

#(NetIncomeLQ) / (RawClose) Calc
SP500DF['NIRC'] = (NetIncomeLQ) / (RC)

#Make float
SP500DF[['TTMNIFCFTA','LQNIFCFTA','OCFRC','NIRC','Beta 3Y Qtr-End']] = SP500DF[['TTMNIFCFTA','LQNIFCFTA','OCFRC','NIRC','Beta 3Y Qtr-End']].astype('float')

SP500DF

"""**Histograms of Rank Based Metrics**"""

#Histograms of metrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

TTMNIFCFTA = SP500DF['TTMNIFCFTA']
LQNIFCFTA = SP500DF['LQNIFCFTA']
OCFRC = SP500DF['OCFRC']
NIRC = SP500DF['NIRC']
Beta = SP500DF['Beta 3Y Qtr-End']

fig1 = plt.figure()
ax1 = fig1.add_subplot(1, 1, 1)
n, bins, patches = ax1.hist(TTMNIFCFTA)
ax1.set_xlabel('TTMNIFCFTA')
ax1.set_ylabel('Frequency')

fig2 = plt.figure()
ax2 = fig2.add_subplot(1, 1, 1)
n, bins, patches = ax2.hist(LQNIFCFTA)
ax2.set_xlabel('LQNIFCFTA')
ax2.set_ylabel('Frequency')

fig3 = plt.figure()
ax3 = fig3.add_subplot(1, 1, 1)
n, bins, patches = ax3.hist(OCFRC)
ax3.set_xlabel('OCFRC')
ax3.set_ylabel('Frequency')

fig4 = plt.figure()
ax4 = fig4.add_subplot(1, 1, 1)
n, bins, patches = ax4.hist(NIRC)
ax4.set_xlabel('NIRC')
ax4.set_ylabel('Frequency')

fig5 = plt.figure()
ax5 = fig5.add_subplot(1, 1, 1)
n, bins, patches = ax5.hist(Beta)
ax5.set_xlabel('Beta')
ax5.set_ylabel('Frequency')

"""**Percentiles of Rank Based Metrics**"""

#Percentilies of metrics
rank1 = TTMNIFCFTA.rank()
rank2 = LQNIFCFTA.rank()
rank3 = OCFRC.rank()
rank4 = NIRC.rank()
rank5 = Beta.rank()

#Percentages of atmosphere (505 stocks)
P97 = 505 * 0.97
P95 = 505 * 0.95
P05 = 505 * 0.05

SP500DF['TTMNIFCFTA PCT'] = rank1
SP500DF['LQNIFCFTA PCT'] = rank2
SP500DF['OCFRC PCT'] = rank3
SP500DF['NIRC PCT'] = rank4
SP500DF['Beta PCT'] = rank5

SP500DF

"""# **Value Strategy - Order By Ranking System**

**Calculations for Full Enviorment**
"""

ROICVS = SP500DF['ROIC % TTM']
FCFVS = SP500DF['FCF TTM']
EBITVS = SP500DF['EBIT TTM (Mil)']
EVVS = SP500DF['EV (Mil)']
EBITEVVS = EBITVS / EVVS
PBVS = SP500DF['P/B Daily'] * -1
PEVS = SP500DF['P/E Daily'] * -1

rROIC = ROICVS.rank(pct=True) * 1
rFCF = FCFVS.rank(pct=True) * 1
rEBITEV = EBITEVVS.rank(pct=True) * 1
rPB = PBVS.rank(pct=True) * 0.8
rPE = PEVS.rank(pct=True) * 1

SP500DF['ROIC % TTM Rank'] = rROIC
SP500DF['FCF TTM Rank'] = rFCF
SP500DF['EBIT / EV Rank'] = rEBITEV
SP500DF['P/B Daily Rank'] = rPB
SP500DF['P/E Daily Rank'] = rPE

"""**Price to Book Rank System (Sector)**"""

PB = SP500DF[['tickers','P/B Daily','Sector']]

PBRS = [x for _, x in PB.groupby('Sector')]

for q in range(len(PBRS)):
  PBDF = PBRS[q]
  PBI = PBDF['P/B Daily'] * -1
  PBDF['P/B Daily Sector PCT'] = PBI.rank(pct=True) 
  SP500DF.loc[PBDF.index, 'P/B Daily Sector PCT'] = PBDF['P/B Daily Sector PCT'] * 0.8

SP500DF

"""**Price to Earnings Rank System (Sector)**"""

PE = SP500DF[['tickers','P/E Daily','Sector']]

PERS = [x for _, x in PE.groupby('Sector')]

for p in range(len(PERS)):
  PEDF = PERS[p]
  PEI = PEDF['P/E Daily'] * -1
  PEDF['P/E Daily Sector PCT'] = PEI.rank(pct=True)
  SP500DF.loc[PEDF.index, 'P/E Daily Sector PCT'] = PEDF['P/E Daily Sector PCT']

SP500DF[["tickers", "Asset Turnover Ratio Industry PCT", 'PiotroskiFScore','Gross Margin % LQ','Total Debt / Total Equity LQ','ROIC % TTM Rank','FCF TTM Rank','EBIT / EV Rank','P/B Daily Rank','P/E Daily Rank']]

"""**Screener FIlter**"""

#Still need event discreteness, asset turnover

SP500DFVS = SP500DF[
                     (SP500DF['PiotroskiFScore'] >= 7) 
                    & (SP500DF['Gross Margin % LQ'] > 7)
                    & (SP500DF['Sector'] != 'Financials')
                    #& (SP500DF['Sector'] != 'Utilities')
                    & (SP500DF['Total Debt / Total Equity LQ'] < 0.75)
                    #& (SP500DF['TTMNIFCFTA PCT'] < P97)
                    #& (SP500DF['LQNIFCFTA PCT'] < P97)
                    #& (SP500DF['OCFRC PCT'] > P05)
                    #& (SP500DF['NIRC PCT'] > P05)
                    #& (SP500DF['Beta PCT'] < P95)
                    & (SP500DF['Asset Turnover Ratio Industry PCT'] > 0.55)
]

SP500DFVS

"""**Final Rank System**"""

SP500DFVS['Total Rank'] = SP500DFVS['ROIC % TTM Rank'] + SP500DFVS['FCF TTM Rank'] + SP500DFVS['EBIT / EV Rank'] + SP500DFVS['P/B Daily Rank'] + SP500DFVS['P/E Daily Rank']
SP500DFVS.sort_values(by=['Total Rank'], ascending=False)

"""# **Backtesting**

Backtesting Research


*   https://towardsdatascience.com/backtest-your-trading-strategy-with-only-3-lines-of-python-3859b4a4ab44
*   https://codingandfun.com/backtesting-fundamental-trading-strategies-python/
*https://kernc.github.io/backtesting.py/

# **Notes**


*   Check with RB on correct formula for Piotroski F Score
*   Get correct inudstries pulled for every stock (should be 64 not 115)
*   Find the metric in the screener that is elminating most/double check metrics
*   Figure out best way to do event discretness 
*   Rank system needs fixing - for stocks accross sector, compare to number of stocks in sector, ame with across all, compare to all stocks
"""