from flask import Flask
import requests
import json
from flask import jsonify
from flask import request
from requests.auth import HTTPBasicAuth
import numpy as np
from collections import OrderedDict
app=Flask(__name__)

location_counter=0
co_ordinates_dict=OrderedDict()

ubermatrix=[]
lyftmatrix=[]

@app.route('/form', methods=['POST'])
def form_matrix():
    global location_counter
    global co_ordinates_dict
    global ubermatrix
    global lyftmatrix
    
    obj=UbervsLyft()
    starting_location=request.form['starting_location']
    first_location=request.form['first']
    second_location=request.form['second']
    third_location=request.form['third']
    fourth_location=request.form['fourth']
    fifth_location=request.form['fifth']
    
    if starting_location:
        location_counter=location_counter+1
        starting_location_parameters=obj.url_parameters(starting_location)
        starting_location_coordinates=obj.get_coordinates(starting_location_parameters)
    
    if first_location:
        location_counter=location_counter+1
        first_location_parameters=obj.url_parameters(first_location)
        first_location_coordinates=obj.get_coordinates(first_location_parameters)
        
    if second_location:
        location_counter=location_counter+1
        second_location_parameters=obj.url_parameters(second_location)
        second_location_coordinates=obj.get_coordinates(second_location_parameters)
    
    if third_location:
        location_counter=location_counter+1
        third_location_parameters=obj.url_parameters(third_location)
        third_location_coordinates=obj.get_coordinates(third_location_parameters)
    
    if fourth_location:
        location_counter=location_counter+1
        fourth_location_parameters=obj.url_parameters(fourth_location)
        fourth_location_coordinates=obj.get_coordinates(fourth_location_parameters)
        
    if fifth_location:
        location_counter=location_counter+1
        fifth_location_parameters=obj.url_parameters(fifth_location)
        fifth_location_coordinates=obj.get_coordinates(fifth_location_parameters)
    
    co_ordinates_dict[starting_location]=starting_location_coordinates
    co_ordinates_dict[first_location]=first_location_coordinates
    co_ordinates_dict[second_location]=second_location_coordinates
    co_ordinates_dict[third_location]=third_location_coordinates
    co_ordinates_dict[fourth_location]=fourth_location_coordinates
    co_ordinates_dict[fifth_location]=fifth_location_coordinates
    
    for i in range(0,location_counter+1):
        lyftmatrix.append([])
        ubermatrix.append([])
    
    ubermatrix[0].append('')
    lyftmatrix[0].append('')
    
    for i in range(0,location_counter):
        ubermatrix[0].append(co_ordinates_dict.keys()[i])
        lyftmatrix[0].append(co_ordinates_dict.keys()[i])
    
    for i in range(0,location_counter):    
        ubermatrix[i+1].append(co_ordinates_dict.keys()[i])
        lyftmatrix[i+1].append(co_ordinates_dict.keys()[i])
        
    obj.lyft_cost()
    obj.uber_cost()
    """print lyftmatrix"""
    result_string=""
    result_string=obj.Djikstra()
    return result_string
    
    
class UbervsLyft:
    def __init__(self):
        pass
    
    def url_parameters(self,location):
        address=location.split()
        parameters=""
        for i in address:
            if not parameters:
                parameters=parameters+i
            else:
                parameters=parameters+"+"+i
        return parameters
        
    def get_coordinates(self, parameters):
        url="https://maps.googleapis.com/maps/api/geocode/json?address="+parameters
        geo_json=requests.get(url)
        geo_json=geo_json.json()
        geo_coord=geo_json['results']
        geo_co=geo_coord[0]['geometry']
        co=geo_co['location']
        coordinates=str(co['lat'])+","+str(co['lng'])
        return coordinates
            
    def lyft_cost(self):
        global location_counter
        global lyftmatrix
        global co_ordinates_dict
        
        lyft_token_url = "https://api.lyft.com/oauth/token"
        lyft_token_headers = {'Content-Type':"application/json",'cache-control': "no-cache"}
        lyft_token=requests.post(lyft_token_url,headers=lyft_token_headers,auth=HTTPBasicAuth('I0hVtv9JvVOV', 'YPiHFSAzqn6fznMbB49uKfaNOz9dQ9W9'),json={'grant_type': "client_credentials", 'scope': "public"})
        lyft_token_data=lyft_token.json()
        access_lyft_token=lyft_token_data['access_token']
        
        for i in range(0,location_counter):
            for j in range(0,location_counter):
                if i==j:
                    lyftmatrix[i+1].append(1000)
                    
                else:
                    start_co=co_ordinates_dict.values()[i]
                    start_co=start_co.split(',')
                    start_co_lat=start_co[0]
                    start_co_lng=start_co[1]
                    end_co=co_ordinates_dict.values()[j]
                    end_co=end_co.split(',')
                    end_co_lat=end_co[0]
                    end_co_lng=end_co[1]    
        
                    lyft_cost_url="https://api.lyft.com/v1/cost?ride_type=lyft&start_lat="+start_co_lat+"&start_lng="+start_co_lng+"&end_lat="+end_co_lat+"&end_lng="+end_co_lng
                    lyft_cost_headers={'Authorization': "Bearer"+" "+access_lyft_token}
                    lyft_cost=requests.get(lyft_cost_url,headers=lyft_cost_headers)
                    lyft_cost_data=lyft_cost.json()
                    lyft_cost_data=lyft_cost_data['cost_estimates']
                    max_cost=lyft_cost_data[0]['estimated_cost_cents_max']
                    max_cost=float(max_cost)/100
                    min_cost=lyft_cost_data[0]['estimated_cost_cents_min']
                    min_cost=float(min_cost)/100
                    lyft_cost=(max_cost+min_cost)/2
                    lyftmatrix[i+1].append(lyft_cost)
        return
        
    def uber_cost(self):
        global location_counter
        global ubermatrix
        global co_ordinates_dict
        
        for i in range(0,location_counter):
            for j in range(0,location_counter):
                if i==j:
                    ubermatrix[i+1].append(1000)
                    
                else:
                    start_co=co_ordinates_dict.values()[i]
                    start_co=start_co.split(',')
                    start_co_lat=start_co[0]
                    start_co_lng=start_co[1]
                    end_co=co_ordinates_dict.values()[j]
                    end_co=end_co.split(',')
                    end_co_lat=end_co[0]
                    end_co_lng=end_co[1]    
        
            
                    uber_cost_url="https://api.uber.com/v1.2/estimates/price?start_latitude="+start_co_lat+"&start_longitude="+start_co_lng+"&end_latitude="+end_co_lat+"&end_longitude="+end_co_lng
                    uber_cost_headers={'Authorization': "Token ydBbvAErXYq192-9DDuxq_5moV41Nw752LR2tTcQ"}
                    uber_cost=requests.get(uber_cost_url,headers=uber_cost_headers)
                    uber_cost_data=uber_cost.json()
                    uber_cost_data=uber_cost_data['prices']
                    for k in uber_cost_data:
                        uber_type=k.get('localized_display_name')
                        if uber_type=="uberX":
                            uber_estimate=k.get('estimate')
                    uber_average=uber_estimate.split('-')
                    uber_min_cost=""
                    uber_max_cost=""
                    for k in uber_average[0]:
                        if k=="$":
                            pass
                        else:
                            uber_min_cost=uber_min_cost+k
                    for k in uber_average[1]:
                        uber_max_cost=uber_max_cost+k
                    uber_cost=(float(uber_max_cost)+float(uber_min_cost))/2
                    ubermatrix[i+1].append(uber_cost)
        return 
        
    def Djikstra(self):
        global location_counter
        global ubermatrix
        global lyftmatrix
        global co_ordinates_dict
        lyft_total_cost=0
        uber_total_cost=0
        lyft_path=""
        uber_path=""
        final_string=""
        counter=0
        column=1
        row=1
        min_value=1000
        interim_value=-1
        while(counter<location_counter):
            for i in range(1,location_counter+1):
                if min_value>lyftmatrix[row][i]:
                    min_value=lyftmatrix[row][i]
                    interim_value=i
            if not lyft_path:
                lyft_path=lyftmatrix[row][0]+"-"+lyftmatrix[0][interim_value]
            else:
                lyft_path=lyft_path+"-"+lyftmatrix[0][interim_value]
            if min_value!=1000:
                lyft_total_cost=lyft_total_cost+min_value
            for j in range(1,location_counter+1):
                lyftmatrix[j][row]=1000
            column=row
            row=interim_value
            lyftmatrix[row][column]=1000
            min_value=1000
            counter=counter+1
        counter=0
        column=1
        row=1
        min_value=1000
        interim_value=-1
        while(counter<location_counter):
            for i in range(1,location_counter+1):
                if min_value>ubermatrix[row][i]:
                    min_value=ubermatrix[row][i]
                    interim_value=i
            if not uber_path:
                uber_path=ubermatrix[row][0]+"-"+ubermatrix[0][interim_value]
            else:
                uber_path=uber_path+"-"+ubermatrix[0][interim_value]
            if min_value!=1000:
                uber_total_cost=uber_total_cost+min_value
            for j in range(1,location_counter+1):
                ubermatrix[j][row]=1000
            column=row
            row=interim_value
            ubermatrix[row][column]=1000
            min_value=1000
            counter=counter+1
        final_string="By Lyft, Cost:"+str(lyft_total_cost)+"Path:"+lyft_path+"By Uber,Cost:"+str(uber_total_cost)+"Path:"+uber_path
        return final_string
     
            
        
""""@app.route('/lyft')
def lyftapi():
	#response=requests.get("https://api.lyft.com/v1/lyft_cost?start_lat=37.7772&start_lng=-122.4233&end_lat=37.7972&end_lng=-122.4533")
    lyft_token_url = "https://api.lyft.com/oauth/token"
    lyft_token_headers = {'Content-Type':"application/json",'cache-control': "no-cache"}
    lyft_token=requests.post(lyft_token_url,headers=lyft_token_headers,auth=HTTPBasicAuth('I0hVtv9JvVOV', 'YPiHFSAzqn6fznMbB49uKfaNOz9dQ9W9'),json={'grant_type': "client_credentials", 'scope': "public"})
    lyft_token_data=lyft_token.json()
    access_lyft_token=lyft_token_data['access_token']
    lyft_cost_url="https://api.lyft.com/v1/cost?ride_type=lyft&start_lat=37.329825&start_lng=-121.904980&end_lat=37.335409&end_lng=-121.881093"
    lyft_cost_headers={'Authorization': "Bearer"+" "+access_lyft_token}
    lyft_cost=requests.get(lyft_cost_url,headers=lyft_cost_headers)
    lyft_cost_data=lyft_cost.json()
    lyft_cost_data=lyft_cost_data['cost_estimates']
    max_cost=lyft_cost_data[0]['estimated_cost_cents_max']
    max_cost=float(max_cost)/100
    min_cost=lyft_cost_data[0]['estimated_cost_cents_min']
    min_cost=float(min_cost)/100
    lyft_cost=(max_cost+min_cost)/2
    return str(lyft_cost)

@app.route('/uber')
def uberapi():
    uber_cost_url="https://api.uber.com/v1.2/estimates/price?start_latitude=37.329825&start_longitude=-121.904980&end_latitude=37.335409&end_longitude=-121.881093"
    uber_cost_headers={'Authorization': "Token ydBbvAErXYq192-9DDuxq_5moV41Nw752LR2tTcQ"}
    uber_cost=requests.get(uber_cost_url,headers=uber_cost_headers)
    uber_cost_data=uber_cost.json()
    uber_cost_data=uber_cost_data['prices']
    for i in uber_cost_data:
        uber_type=i.get('localized_display_name')
        if uber_type=="uberX":
            uber_estimate=i.get('estimate')
    uber_average=uber_estimate.split('-')
    uber_min_cost=""
    uber_max_cost=""
    for i in uber_average[0]:
        if i=="$":
            pass
        else:
            uber_min_cost=uber_min_cost+i
    for i in uber_average[1]:
        uber_max_cost=uber_max_cost+i
    uber_cost=(float(uber_max_cost)+float(uber_min_cost))/2
    return str(uber_cost)"""
    
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

