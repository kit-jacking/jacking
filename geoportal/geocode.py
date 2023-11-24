from classes.node import Node
from classes.graph import Graph
from algorithms.algorithms import *
from algorithms.a_star import *


from flask import Flask, render_template, request, json
import requests
from requests.structures import CaseInsensitiveDict
from urllib import parse
from example_graphs import *
from rtree import index
from pyproj import transform, Proj

app = Flask(__name__)

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
    
    # Coordinates transformation
    in_proj = Proj(init = 'EPSG:4326')
    out_proj = Proj(init = 'EPSG:2180')
    
    nav_graph, gdf, node_start, node_end = example_graph_shapefile(r'path')
    
    tr_lon_from, tr_lat_from = transform(in_proj, out_proj, lon_from, lat_from)
    tr_lon_to, tr_lat_to = transform(in_proj, out_proj, lon_to, lat_to)
    
    print('\n\n\n\n')
    print(node_start, node_end)
    print(tr_lon_from, tr_lat_from)
    print(tr_lon_to, tr_lat_to)
    
    # Nearest node search
    idx = index.Index()
    for i, node in enumerate(nav_graph.nodes):
        idx.insert(i, (node.x, node.y, node.x, node.y), Node)
        
    hit1 = list(idx.nearest((tr_lon_from, tr_lat_from, tr_lat_from,tr_lat_from), 1))[0]
    start_node = nav_graph.nodes[hit1]
    
    hit2 = list(idx.nearest((tr_lon_to, tr_lat_to, tr_lon_to, tr_lat_to), 1))[0]
    finish_node = nav_graph.nodes[hit2]
    
    def distance(node: Node) -> float:
        return distance_between_nodes(node, finish_node)
    
    output = a_star(start_node, finish_node, distance, False)
    # path_gdf = output.get_path_gdf(gdf)
    # path_gdf.to_file(r"path", driver="GeoJSON")
    
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == '__main__':
    app.run(debug=True, port=5500)