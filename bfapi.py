import requests
import json
import ssl
import urllib

ssl._create_default_https_context = ssl._create_unverified_context

endpoint = "https://api.betfair.com/exchange/betting/json-rpc/v1"
json_req='{"filter":{ "eventIds":[]}, "maxResults": 1}'
url = endpoint
header = { 'X-Application' : '1NsMIR9lZH78uGJv', 
		   'X-Authentication' : '86ofKB5LBxx+GAU0mM4JeJj8z7BGr2JfEhv6VHyIsTA=' ,
	       'content-type' : 'application/json'}


def call_api_ng(json_request):
	req = urllib.request.Request(url, json_request.encode('utf-8'), header)
	response = urllib.request.urlopen(req)
	jsonResponse = response.read()
	return jsonResponse.decode('utf-8')
'''

'''

def list_event_types():
	req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
	response = call_api_ng(req)
	loads = json.loads(response)
	results = loads['result']
	return results

'''
def list_event_types():
	req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
	response = call_api_ng(req)
	return json.loads(response)['result']
'''

#event_name e.g. 'Tennis', 'Soccer'
'''
def event_type_id(event_name):
	event_type_results = list_event_types()
	for event in event_type_results:
		event_type_name = event['eventType']['name']
		if(event_type_name == event_name):
			return event['eventType']['id']
'''

def event_type_id(event_name):
	event_type_results = list_event_types()
	for event in event_type_results:
		if(event['eventType']['name'] == event_name):
			return event['eventType']['id']

def list_market_catalogue(event_type_id):
	req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter": {"eventTypeIds": ["' + event_type_id + '"]},"maxResults": "1","marketProjection":["RUNNER_METADATA"]},"id": 1}'
	response = call_api_ng(req)
	return (json.loads(response))['result'][0]

def selection_id(list_market_catalogue_results):
		return list_market_catalogue_results['runners'][0]['selectionId']
		
def get_market_id(list_market_catalogue_results):
	return list_market_catalogue_results['marketId']

def get_market_book(market_id):
	req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params": {"marketIds":["' + market_id + '"],"priceProjection":{"priceData":["EX_BEST_OFFERS"]}}, "id": 1}'
	response = call_api_ng(req)
	return (json.loads(response))['result']
	
if __name__ == '__main__':
	print 'this code runs'
