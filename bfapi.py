import requests
import json
import ssl
import urllib
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

#json parameters
endpoint = "https://api.betfair.com/exchange/betting/json-rpc/v1"
json_req='{"filter":{ "eventIds":[]}, "maxResults": 1}'
url = endpoint

def event_type_id(event_name):
	event_type_results = list_event_types()
	for event in event_type_results:
		if(event['eventType']['name'] == event_name):
			return event['eventType']['id']

def list_market_catalogue(event_type_id):
	req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter": {"eventTypeIds": ["' + event_type_id + '"]},"maxResults": "1","marketProjection":["RUNNER_METADATA"]},"id": 1}'
	response = call_api_ng(req)
	loads = json.loads(response)
	return loads['result'][0]

def get_selection_id(list_market_catalogue_results):
		return list_market_catalogue_results['runners'][0]['selectionId']
		
def get_market_id(list_market_catalogue_results):
	return list_market_catalogue_results['marketId']

def list_market_book(market_id):
	req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params": {"marketIds":["' + market_id + '"],"priceProjection":{"priceData":["EX_BEST_OFFERS",  "EX_TRADED"], "virtualise": "true"}}, "id": 1}'
	response = call_api_ng(req)
	loads = json.loads(response)
	return loads['result']

def call_api_ng(json_request):
	req = urllib.request.Request(url, json_request.encode('utf-8'), header)
	response = urllib.request.urlopen(req)
	jsonResponse = response.read()
	return jsonResponse.decode('utf-8')

def list_event_types():
	req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
	response = call_api_ng(req)
	loads = json.loads(response)
	results = loads['result']
	return results

def make_curl_call(username, password):
	headers = {
	'Accept': 'application/json',
	'X-Application': '1NsMIR9lZH78uGJv',
	}
	data = [
	('username', username),
	('password', password),
	]
	response = requests.post('https://identitysso.betfair.com/api/login', headers=headers, data=data, verify=False)
	return response.json()['token']

if __name__ == '__main__':
	token = make_curl_call('ccbeauchamp', 'aerodynamic224')
	header = {'X-Application' : '1NsMIR9lZH78uGJv', 
			  'X-Authentication' : token ,
			   'content-type' : 'application/json'}

	horse_event_id = event_type_id('Horse Racing')
	horse_market_catalogue = list_market_catalogue(horse_event_id)
	horse_selection_id = get_selection_id(horse_market_catalogue)
	horse_market_id = get_market_id(horse_market_catalogue)
	horse_market_book = list_market_book(horse_market_id)

	print("\n")
	print("\nmarket catalogue: \n", horse_market_catalogue)
	print("\nselection id: \n", horse_selection_id)
	print("\nmarket id: \n", horse_market_id)
	print("\nmarket book: \n", horse_market_book)
	