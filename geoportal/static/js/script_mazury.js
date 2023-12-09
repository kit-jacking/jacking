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
	minZoom: 6,
	maxZoom: 16,
	maxBounds: L.latLngBounds(L.latLng(51.3, 16), L.latLng(56,26)),
	zoomControl: false
}
).setView([53.8,21.2], 8)

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var polyline = new L.Polyline([[0,0],[0,0]], {
	color: 'blue',
}).addTo(map);

L.control.zoom({
	zoomInTitle: 'Przybliż',
	zoomOutTitle: 'Oddal'
}).addTo(map);
var popup = L.popup([0,0], {content: '<p>Hello world!<br />This is a nice popup.</p>'});
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

			var path = JSON.parse(response.path);
			var coordinates = [];

			for (let i = 0; i < path.features.length; i++) {
				let obj = path.features[i].geometry.coordinates;
				coordinates.push([obj[1], obj[0]]);
			}

			polyline = new L.Polyline(coordinates, {
				color: 'blue',
				weight: 5
			});

			console.log(path.features.length)
			console.log(coordinates.length)
			console.log(coordinates.length / 2)
			
			let latlon = coordinates[Math.round(coordinates.length / 2)]
			console.log(latlon)
			popup = L.popup([latlon[0], latlon[1]], {content: '<center>' + 'Dystans: ' + Math.round(response.distance/1000) + ' km</center>'}).openOn(map);
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


