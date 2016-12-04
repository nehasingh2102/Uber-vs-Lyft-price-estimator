from flask import Flask
import requests
import json
from flask import jsonify
from requests.auth import HTTPBasicAuth

app=Flask(__name__)

@app.route('/lyft')
def lyftapi():
	#response=requests.get("https://api.lyft.com/v1/lyft_cost?start_lat=37.7772&start_lng=-122.4233&end_lat=37.7972&end_lng=-122.4533")
    lyft_token_url = "https://api.lyft.com/oauth/lyft_token"
    lyft_token_headers = {'Content-Type':"application/json",'cache-control': "no-cache"}
    lyft_token=requests.post(lyft_token_url,headers=lyft_token_headers,auth=HTTPBasicAuth('I0hVtv9JvVOV', 'YPiHFSAzqn6fznMbB49uKfaNOz9dQ9W9'),json={'grant_type': "client_credentials", 'scope': "public"})
    lyft_token_data=lyft_token.json()
    access_lyft_token=lyft_token_data['access_lyft_token']
    lyft_cost_url="https://api.lyft.com/v1/lyft_cost?ride_type=lyft&start_lat=37.329825&start_lng=-121.904980&end_lat=37.335409&end_lng=-121.881093"
    lyft_cost_headers={'Authorization': "Bearer"+" "+access_lyft_token}
    lyft_cost=requests.get(lyft_cost_url,headers=lyft_cost_headers)
    lyft_cost_data=lyft_cost.json()
    return jsonify(lyft_cost_data)

@app.route('/uber')
def uberapi():
    uber_cost_url="https://api.uber.com/v1.2/estimates/price?start_latitude=37.329825&start_longitude=-121.904980&end_latitude=37.335409&end_longitude=-121.881093"
    uber_cost_headers={'Authorization': "Token ydBbvAErXYq192-9DDuxq_5moV41Nw752LR2tTcQ"}
    uber_cost=requests.get(uber_cost_url,headers=uber_cost_headers)
    uber_cost_data=uber_cost.json()
    return jsonify(uber_cost_data)
    
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

