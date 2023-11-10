var map = L.map('map', {
	//poziomy zooma
	minZoom: 14,
	maxZoom: 16,
	zoomControl: false
}
).setView([52.225, 21.357], 15);

L.control.zoom({
	zoomInTitle: 'Przybliż',
	zoomOutTitle: 'Oddal'
}).addTo(map);

var imageUrl_map = 'mapa.png';
var imageUrl_orto = 'mapa_orto.png';
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


var nodes = new L.geoJson(halinow_conjuctions).addTo(map);

map.on("zoomend", function() {
    var zoomlevel = map.getZoom();
    if (zoomlevel < 15) 
	{
        if (map.hasLayer(nodes)) 
		{
            map.removeLayer(nodes);
        }
    }
    if (zoomlevel >= 15) 
	{
        if (!map.hasLayer(nodes)) 
		{
            map.addLayer(nodes);
        }
    }
});