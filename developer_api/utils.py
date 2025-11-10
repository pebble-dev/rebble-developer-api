from flask import request, abort, jsonify
from geopy.geocoders import Nominatim
from dateutil import parser

import beeline

ERROR_CODES = {
    400:	{"error": { "name": "INVALID_JSON", "details": { "message": "The submitted form is invalid." }}},
    404:	{"error": { "name": "NOT_FOUND", "details": { "message": "The endpoint wasn't found." }}},
    410:	{"error": { "name": "INVALID_PARAMS", "details": { "message": "The submitted form is invalid." }}},
    429:	{"error": { "name": "RATE_LIMIT_EXCEEDED", "details": { "message": "You exceeded the rate limit." }}},
    500:	{"error": { "name": "INTERNAL_SERVER_ERROR", "details": { "message": "The server failed processing your request." }}}
}

def api_error(code):
    response = jsonify(ERROR_CODES[code])
    response.status_code = code
    beeline.add_context_field('timeline.failure', ERROR_CODES[code]['error']['name'])
    return response

def geolocate(text):
    geolocator = Nominatim(user_agent="rebble-developer-api")
    location = geolocator.geocode(text)
    return [location.longitude, location.latitude] if not location is None else [None, None]

def parse_date(text):
    return parser.parse(text.split("(")[0].strip())
