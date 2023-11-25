var blueStyle = 
{
	radius: 5,
	color: "darkblue",
	opacity: 3,
	fillOpacity: 1
};

var start = '1'

var map = L.map('map', {
	//poziomy zooma
	minZoom: 13,
	maxZoom: 16,
	maxBounds: L.latLngBounds(L.latLng(52.20, 21.28), L.latLng(52.25,21.43)),
	zoomControl: false
}
).setView([52.225, 21.357], 15); // Halinów
// ).setView([54.10512373644716,21.96490637704919], 15) // Mazury

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


// Input boxes
var addressFrom = '';
var addressTo = '';
var APIKey = '';
function getAddressInput(mode) {
	addressFrom = document.getElementsByNgitame('inpAddressFrom')[0].value
	addressTo = document.getElementsByName('inpAddressTo')[0].value
	APIKey = document.getElementsByName('inpAPIKey')[0].value
	console.log(addressFrom)
	console.log(addressTo)
	console.log(APIKey)
	console.log(mode)

	// Call Python function
	$.ajax({
		type: "POST",
		url: "/getNodesFromAddress",
		data: {addressFrom: `${addressFrom}`, addressTo: `${addressTo}`, APIKey: `${APIKey}`, mode:mode},
		success: function(response) {
			console.log(response);
			var path = JSON.parse(response);
			console.log(path );
            L.geoJSON(path, {}).addTo(map);
			
		},
		error: function(xhr,status,error) {
			alert(`Wystąpił błąd - wpisano niepoprawny adres\nError ${xhr.status}`);
		}
		
	})
}
