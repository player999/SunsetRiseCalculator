#!/usr/bin/env python3

from math import pi, degrees, radians, sin, cos, sqrt, acos, floor

def julianDay(date):
	d = date["day"]
	month = date["month"]
	a = (14 - month) / 12
	y = date["year"] + 4800 - a
	m = month + 12 * a - 3
	jday = d + int((153 * m + 2) / 5) + int(365 * y) + int(y / 4) - int(y / 100) + int(y / 400) - 32045
	return jday

def meanSolarNoon(longitude, n):
	jstar = longitude / 360 + n
	return jstar

def solarMeanAnomaly(jstar):
	M = (357.5291 + 0.98560028 * jstar) % 360
	return M

def equationOfCenter(M):
	M = radians(M)
	C = 1.9148 * sin(M) + 0.02 * sin(2 * M) + 0.0003 * sin(3 * M)
	C = degrees(C)
	return C

def eclipticLongitude(M, C):
	return (M + C + 180 + 102.9372) % 360

def solarTransit(jstar, M, lambada):
	jt = jstar + 0.0053 * sin(radians(M)) - 0.0069 * sin(radians(lambada) * 2)
	return jt

def sunDeclinationSin(lambada):
	return sin(radians(lambada)) * sin(radians(23.44))

def hourAngle(latitude, decl):
	cosd = sqrt(1 - decl * decl)
	sind = decl
	ha = (sin(radians(-0.83)) - sin(radians(latitude)) * sind) / (cos(radians(latitude)) * cosd)
	ha = degrees(acos(ha))
	return ha

def gregorianTime(jd):
	jdn = floor(jd)
	a = jdn + 32044
	b = floor((4 * a + 3) / 146097)
	c = a - floor(146097 * b / 4)
	d = floor((4 * c + 3) / 1461)
	e = c - floor((1461 * d) / 4)
	m = floor((5 * e + 2) / 153)
	date = {}
	date["day"] = e - floor((153 * m + 2) / 5) + 1
	date["month"] = m + 3 - 12 * floor(m / 10)
	date["year"] = 100 * b + d - 4800 + floor(m / 10)

	decpart = jd - floor(jd)
	totalsecs = decpart * 60 * 60 * 24
	hours = floor(totalsecs / 3600)
	minutes = floor((totalsecs - hours * 3600) / 60)
	seconds = totalsecs - hours * 3600 - minutes * 60
	hours += 12 + 3
	if hours > 23:
		date["day"] += 1
		date["hours"] = hours - 24 + 1
	else:
		date["hours"] = hours + 1
	date["minutes"] = minutes + 1
	date["seconds"] = seconds + 1


	return date

def calculateSunSetRise(params):
	jday = julianDay(params["date"])
	n = jday - 2451545 + 0.0008
	jstar = meanSolarNoon(params["longitude"], n)
	M = solarMeanAnomaly(jstar)
	C = equationOfCenter(M)
	lambada = eclipticLongitude(M, C)
	jt = solarTransit(jstar, M, lambada)
	decl = sunDeclinationSin(lambada)
	ha = hourAngle(params["latitude"], decl)
	jsunrise = jt - ha / 360 + 2451545 - 0.0008
	jsunset = jt + ha / 360 + 2451545 - 0.0008

	return gregorianTime(jsunrise), gregorianTime(jsunset)


if __name__ == "__main__":
	params = {
		"latitude": 50.433300, # North
		"longitude": -30.5160000, # East
		"date": {
			"year": 2016,
			"month": 8, #August
			"day": 3
		}
	}
	print(calculateSunSeRise(params))