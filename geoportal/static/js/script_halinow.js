var blueStyle = 
{
	radius: 5,
	color: "darkblue",
	opacity: 3,
	fillOpacity: 1
};

var start = 1

var map = L.map('map', {
	//poziomy zooma
	minZoom: 13,
	maxZoom: 16,
	maxBounds: L.latLngBounds(L.latLng(52.20, 21.28), L.latLng(52.25,21.43)),
	zoomControl: false
}
).setView([52.225, 21.357], 15);

L.control.zoom({
	zoomInTitle: 'Przybliż',
	zoomOutTitle: 'Oddal'
}).addTo(map);



var imageUrl_map = 'static/images/mapa.png';
var imageUrl_orto = 'static/images/mapa_orto.png';
var altText = 'Mapa Halinowa';
var latLngBounds = L.latLngBounds([[52.236589738, 21.376944963], [52.213842532, 21.336124121]]);

var map_car = L.imageOverlay(imageUrl_map, latLngBounds, {
    opacity: 1,
    alt: altText,
    interactive: true
}).addTo(map);

var map_orto = L.imageOverlay(imageUrl_orto, latLngBounds, {
    opacity: 1,
    alt: altText,
    interactive: true
});

var baseMaps = {
    "BDOT": map_car,
	"Ortofotomapa": map_orto	
};

var layerControl = L.control.layers(baseMaps).addTo(map);

var nodes = new L.geoJson
(
	halinow_conjuctions,
	{
		pointToLayer: function (feature, latlng) 
		{
				return L.circleMarker(latlng, blueStyle);
		},
		onEachFeature: onEachFeature
 	}
);



function onEachFeature(feature, layer) {
	layer.bindPopup(feature.id);
}

map.on("zoomend", function() {
    var zoomlevel = map.getZoom();
    if (zoomlevel < 16) 
	{
        if (map.hasLayer(nodes)) 
		{
            map.removeLayer(nodes);
        }
    }
    if (zoomlevel >= 16) 
	{
        if (!map.hasLayer(nodes)) 
		{
            map.addLayer(nodes);
        }
    }
	console.log(start);
});

nodes.on('click', function (e) {
	clickedMarker = e.target
	console.log(clickedMarker)
});
//var path_layer = L.geoJSON('{"type": "FeatureCollection","features": [{"type": "Feature","properties": {}, "geometry": {"coordinates": [],"type": "LineString"}}]}' ,{})
// Input boxes
var polyline = new L.Polyline([[0,0],[0,0]], {
	color: 'blue',
}).addTo(map);

function delay(time) {
  return new Promise(resolve => setTimeout(resolve, time));
}

var algorithm = "dijkstra";
var cost = "time";
var addressFrom = '';
var addressTo = '';
var APIKey = '';
function getAddressInput(mode) {
	console.log(algorithm);
	addressFrom = document.getElementsByName('inpAddressFrom')[0].value
	addressTo = document.getElementsByName('inpAddressTo')[0].value
	APIKey = document.getElementsByName('inpAPIKey')[0].value
	console.log(addressFrom)
	console.log(addressTo)
	console.log(APIKey)
	console.log(mode)
	
	delay(1000).then(() => console.log('ran after 1 second1 passed'));
	// Call Python function
	$.ajax({
		type: "POST",
		url: "/getNodesFromAddress",
		data: {addressFrom: `${addressFrom}`, addressTo: `${addressTo}`, APIKey: `${APIKey}`, mode:mode, algorithm: algorithm, cost: cost},
		success: function(response) {			
			console.log(response);
			
			if (start == 0)
			{
				map.removeLayer(polyline)
			}

			var path = JSON.parse(response);
			var coordinates = [];

			for (let i = 0; i < path.features.length; i++) {
				let obj = path.features[i].geometry.coordinates;
				coordinates.push([obj[1], obj[0]]);
			}

			polyline = new L.Polyline(coordinates, {
				color: 'blue',
				weight: 5
			});

			polyline.addTo(map);

			start = 0;
		},
		error: function(xhr,status,error) {
			alert(`Wystąpił błąd - wpisano niepoprawny adres\nError ${xhr.status}`);
		}		
	})
}

function algorithmFunction() {
	// Get the checkbox
	var checkBox = document.getElementById("Algorythm");
	// Get the output text

	// If the checkbox is checked, display the output text
	if (checkBox.checked == true)
	{
		console.log("A*");
		algorithm = "A*";	
	} 
	else 
	{
		console.log("dijkstra");
		algorithm = "dijkstra";
	}
}

function costFunction() {
	// Get the checkbox
	var checkBox = document.getElementById("cost");
	// Get the output text

	// If the checkbox is checked, display the output text
	if (checkBox.checked == true)
	{
		console.log("distance");
		cost = "distance";
	} 
	else 
	{
		console.log("time");
		cost = "time";
	}
}
