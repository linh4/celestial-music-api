# Music API
This is a python script which serves musical frequency data based on the right ascension and declination between a user and a specific planets. Running the index file will start a server on `http://localhost:8000/`.
This server responds to post requests which send data (including the user's latitude, longitude and desired planet) in this JSON format.

```json
{
	"planet": "pluto",
	"lat": "40.7128",
	"long": "-74.0060"
}
```
The response JSON looks like the below.
```json
{
  "body": {
    "pluto": {
      "ra_note": 415.3114413142119,
      "dec_note": 233.08587314585617
    }
  },
  "statusCode": 200
}
```

You can also request all planetary data by passing `all` as the planet name.
```json
{
	"planet": "all",
	"lat": "40.7128",
	"long": "-74.0060"
}
```
The response JSON looks like the below.
```json
{
  "body": [
    {
      "sun": {
        "ra_note": 466.1712480663438,
        "dec_note": 155.56625344625252
      }
    }, {
      "moon": {
        "ra_note": 277.18730469,
        "dec_note": 293.66969338878147
        }
    }, {
      "mercury": {
        "ra_note": 466.1712480663438,
        "dec_note": 138.59380046840704
      }
    }, {
      "venus": {
        "ra_note": 370.0004966027867,
        "dec_note": 220.00378790562402
      }
    }, {
      "earth": {
        "ra_note": 392.00183613227824,
        "dec_note": 174.61718438712094
      }
    }, {
      "mars": {
        "ra_note": 293.66969338878147,
        "dec_note": 493.8911889901128
      }
    }, {
      "jupiter": {
        "ra_note": 349.2339955267779,
        "dec_note": 233.08587314585617
      }
    }, {
      "saturn": {
        "ra_note": 392.00183613227824,
        "dec_note": 233.08587314585617
      }
    }, {
      "uranus": {
        "ra_note": 293.66969338878147,
        "dec_note": 493.8911889901128
      }
    }, {
      "neptune": {
        "ra_note": 493.8911889901128,
        "dec_note": 196.00112754415827
      }
    }, {
      "pluto": {
        "ra_note": 415.3114413142119,
        "dec_note": 233.08587314585617
      }
    }
  ],
  "statusCode": 200
}
```

# Installation

To run this code locally:
- clone this repo
- confirm your python version by running `python --version`
- if you are running Python 2.7.10, you are set. If not, YOLO.
- install PIP package manager by running `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py` then `python get-pip.py`
- Install packages with `pip install skyfield`
- Now run the code with `python index.py`
