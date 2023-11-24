from classes.node import Node
from classes.graph import Graph

from flask import Flask, render_template, request, json
import requests
from requests.structures import CaseInsensitiveDict
from urllib import parse
from example_graphs import *

app = Flask(__name__)


# Default action when webpage is opened - return html file
@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/halinow')
def halinow():
    nav_graph = example_graph_shapefile(r'C:\Users\qattr\Desktop\CODE\GitHub\PAG2\jacking\shapefiles\Halinow Highways\Halinow Highways.shp')
    print('Loaded')
    return render_template('halinow.html')
    
@app.route('/mazury')
def mazury():
    return render_template('mazury.html')
    
@app.route('/polska')
def polska():
    return render_template('polska.html') 

# getAddressInput() function redirects here when "Wyznacz trasę" button is clicked. 
@app.route('/getNodesFromAddress', methods=['GET', 'POST'])
def getNodesFromAddress():
    api_key = request.form.get('APIKey')
    # Parse Address From from input box to URL format
    address_from = parse.quote(request.form.get('addressFrom'))
    url_from = f"https://api.geoapify.com/v1/geocode/search?text={address_from}&country=Poland&apiKey={api_key}"
    
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    # Get response from geocode engine and extract lat and lon from it
    resp = requests.get(url_from, headers=headers)
    if resp.status_code == 200:
        response_json = resp.json()['features'][0]['properties']
        lat_from, lon_from = response_json['lat'], response_json['lon']
    else:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}
    
    # Parse Address From from input box to URL format
    address_to = parse.quote(request.form.get('addressTo'))
    url_to = f"https://api.geoapify.com/v1/geocode/search?text={address_to}&country=Poland&apiKey={api_key}"
    
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    # Get response from geocode engine and extract lat and lon from it
    resp = requests.get(url_to, headers=headers)
    if resp.status_code == 200:
        response_json = resp.json()['features'][0]['properties']
        lat_to, lon_to = response_json['lat'], response_json['lon']
    else:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}
    
    
    # print(lat_from, lon_from)
    # print(lat_to, lon_to)
    
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == '__main__':
    app.run(debug=True, port=5500)