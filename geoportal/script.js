var map = L.map('map').setView([52.225, 21.357], 15);



var imageUrl = 'mapa.png';
var altText = 'Mapa Halinowa';
var latLngBounds = L.latLngBounds([[52.236589738, 21.376944963], [52.213842532, 21.336124121]]);

var imageOverlay = L.imageOverlay(imageUrl, latLngBounds, {
    opacity: 1,
    alt: altText,
    interactive: true
}).addTo(map);