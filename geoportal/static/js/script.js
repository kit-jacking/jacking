function round_distance(distance)
{
	if (distance >= 1000)
	{
		console.log(distance/1000);
		console.log((distance % 1000)/1000);
		console.log(Math.round((distance % 1000)/100))
		return Math.round((distance / 1000) - (distance % 1000)/1000) + ',' + Math.round((distance % 1000)/100) + ' km';
	}
	else
	{
		return Math.round(distance) + ' m';
	}
}