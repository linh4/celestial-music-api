from skyfield.api import Topos, load
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

def lambda_handler(event, context):
    data =  MusicGenerator(event['lat'], event['long'], event['planet']).execute()
    return {
        'statusCode': 200,
        'body': data
    }

class MusicGenerator:
    planets = [
        'sun',
        'moon',
        'mercury',
        'venus',
        'earth',
        'mars',
        'jupiter',
        'saturn',
        'uranus',
        'neptune',
        'pluto'
   ]

    def __init__(self, lat, long, planet):
        self.lat = str(lat)
        self.long = str(long)
        self.planet = planet.lower()

    def execute(self):
        if self.planet == 'all':
            return list(map(lambda planet: self.find_notes(planet), self.planets))
        else:
            return self.find_notes(self.planet)

    def find_notes(self, planet):
        ra, dec = SkyfieldAdapter(self.lat, self.long, planet).execute()
        notes = {'ra_note': Note(ra, 'ascension').generate(), 'dec_note': Note(dec, 'declination').generate()}
        return {planet: notes}


class SkyfieldAdapter:
    bodies = {
        'sun': 'sun',
        'moon': 'moon',
        'mercury': 'mercury',
        'venus': 'venus',
        'earth': 'earth',
        'mars': 'mars',
        'jupiter': 'jupiter barycenter',
        'saturn': 'saturn barycenter',
        'uranus': 'uranus barycenter',
        'neptune': 'neptune barycenter',
        'pluto': 'pluto barycenter'
    }

    def __init__(self, lat, long, planet):
        planets = load('de421.bsp')
        self.lat = self.topos_lat(lat)
        self.long = self.topos_long(long)
        self.planet = planets[self.bodies[planet]]
        self.earth = planets['earth']

    def location(self):
        return self.earth + Topos(self.lat, self.long)

    def topos_lat(self, lat):
        if lat[0] == '-':
            return lat[1:] + ' S'
        else:
            return lat + ' N'

    def topos_long(self, long):
        if long[0] == '-':
            return long[1:] + ' W'
        else:
            return long + ' E'

    def time(self):
        ts = load.timescale()
        return ts.now()

    def execute(self):
        apparent = self.location().at(self.time()).observe(self.planet).apparent()
        ra, dec, distance = apparent.radec()
        return (ra, dec)

class Note:
    def __init__(self, measurement, type):
        self.measurement = measurement
        self.type = type
        self.tonic = 261.63

    def generate(self):
        if self.type == 'ascension':
            return self.calc_ascension()
        else:
            return self.calc_declination()

    def calc_ascension(self):
        hours = round(self.measurement.hours)
        scale_degree = hours % 12
        note = self.tonic * (1.059463)** scale_degree
        return note

    def calc_declination(self):
        degrees = round(self.measurement.degrees)
        scale_degree = degrees % 12
        if degrees < 0:
            note = self.tonic * (1.059463) ** (-1 * scale_degree)
        else:
            note = self.tonic * (1.059463) ** scale_degree
        return note


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>Running!</h1></body></html>")

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length)
        json_data = json.loads(post_data)
        data = lambda_handler(json_data, {})
        self.wfile.write(json.dumps(data))

def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
