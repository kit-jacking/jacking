from classes.node import Node
from classes.graph import Graph
from algorithms.a_star import *
from classes.node import Node
from classes.graph import Graph
from algorithms.algorithms import *
from algorithms.a_star import *
from example_graphs import *

from flask import Flask, render_template, request, json, jsonify
import requests
from requests.structures import CaseInsensitiveDict
from urllib import parse
from rtree import index
from pyproj import transform, Proj


app = Flask(__name__)


# Load graphs and create spatial index
print('Indexing Halinow...')
graph_halinow, gdf_halinow, node_start_halinow, node_end_halinow = create_example_graph_from_file(r'geometries\halinow.geojson')
idx_halinow = index.Index()
for i, node in enumerate(graph_halinow.nodes):
    idx_halinow.insert(i, (node.x, node.y, node.x, node.y), Node)
print('Indexing Mazury...')    
graph_mazury, gdf_mazury, node_start_mazury, node_end_mazury = create_example_graph_from_file(r'geometries\mazury.geojson')
idx_mazury = index.Index()
for i, node in enumerate(graph_mazury.nodes):
    idx_mazury.insert(i, (node.x, node.y, node.x, node.y), Node)
print('Finished')


# Default action when webpage is opened - return html file
@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/halinow')
def halinow():
    return render_template('halinow.html')
    
@app.route('/mazury')
def mazury():
    return render_template('mazury.html')
    
@app.route('/polska')
def polska():
    return render_template('polska.html') 

# getAddressInput() function redirects here when "Wyznacz trasę" button is clicked. 
@app.route('/getNodesFromAddress', methods=['GET', 'POST'])
def  getNodesFromAddress():
    #graph_halinow, gdf_halinow, node_start_halinow, node_end_halinow = create_example_graph_from_file(r'geometries\halinow.geojson')
    #graph_mazury, gdf_mazury, node_start_mazury, node_end_mazury = create_example_graph_from_file(r'geometries\mazury.geojson')
    
    
    api_key = request.form.get('APIKey')
    region = request.form.get('mode')
    
    if int(region) == 0:
        nav_graph = graph_halinow
        gdf = gdf_halinow
        idx = idx_halinow
        
    elif int(region) == 1:
        nav_graph = graph_mazury
        gdf = gdf_mazury
        idx = idx_mazury

    # Parse Address From from input box to URL format
    address_from = parse.quote(request.form.get('addressFrom'))
    url_from = f"https://api.geoapify.com/v1/geocode/search?text={address_from}&country=Poland&apiKey={api_key}"
    print(url_from)
    
    # Parse Address From from input box to URL format
    address_to = parse.quote(request.form.get('addressTo'))
    url_to = f"https://api.geoapify.com/v1/geocode/search?text={address_to}&country=Poland&apiKey={api_key}"
    print(url_to)
    
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    # Get response from geocode engine and extract lat and lon from it
    resp = requests.get(url_to, headers=headers)
    if resp.status_code == 200:
        response_json = resp.json()['features'][0]['properties']
        lat_from, lon_from = response_json['lat'], response_json['lon']
        print(lat_from, lon_from)
    else:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}
    
    
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    # Get response from geocode engine and extract lat and lon from it
    resp = requests.get(url_from, headers=headers)
    if resp.status_code == 200:
        response_json = resp.json()['features'][0]['properties']
        lat_to, lon_to = response_json['lat'], response_json['lon']
        print(lat_from, lon_from)
    else:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}    
    print(address_from)
    print(address_to)
    print(api_key)
    # Nearest node search
    # for i, node in enumerate(nav_graph.nodes):
    #   idx.insert(i, (node.x, node.y, node.x, node.y), Node)
        
    hit1 = list(idx.nearest((lon_from, lat_from, lon_from, lat_from), 1))[0]
    start_node = nav_graph.nodes[hit1]
    print("---------------------")
    print(hit1)
    
    hit2 = list(idx.nearest((lon_to, lat_to, lon_to, lat_to), 1))[0]
    finish_node = nav_graph.nodes[hit2]
    print(hit2)
    
    def distance(node: Node) -> float:
        return distance_between_nodes(node, finish_node)
        
    #print(star_node)
    #print(finish_node)
    
    output = a_star(start_node, finish_node, distance, False)
    #print('start')
    #print(output)
    path_gdf = output.get_path_gdf(gdf)
    #path_gdf.to_file("output.json", driver="GeoJSON")
    #print(path_gdf.to_json()) 
    #print('end')
    nav_graph.clear()
    return jsonify(path_gdf.to_json())

if __name__ == '__main__':
    app.run(debug=False, port=5500)
#  
#path =  '{"type": "FeatureCollection","features": [{"type": "Feature","properties": {}, "geometry": {"coordinates": [[ 21.346229178758932,  52.22848751411718], [21.356740593289715, 52.2250019332337],[21.354488147318705, 52.22238756799925], [ 21.360336603523393,52.220354066400716],[ 21.360750902377276,52.220871831603006],[21.361188187667693,   52.22116158852941 ] ],"type": "LineString"}}]}'
#return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
