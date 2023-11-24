var map = L.map('map', {
	//poziomy zooma
	minZoom: 4,
	maxZoom: 16,
	maxBounds: L.latLngBounds(L.latLng(51.3, 16), L.latLng(56,26)),
	zoomControl: false
}
).setView([53.8,21.2], 8)

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);