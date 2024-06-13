import datetime
import requests

from .utils import cache
from .models import Organization


def extract_data(response, origin):
    if response["status"] != 200:
        raise Exception("Bad response")

    orgs = []
    for o in response["response"]:
        org = {
            "name": o["properties"]["name"],
            "lat": o["geometry"]["coordinates"][1],
            "lng": o["geometry"]["coordinates"][0],
            "origin": origin,
        }
        org["url"] = get_url(origin, o["properties"])
        orgs.append(org)

    return orgs

def get_url(origin, o):
    maps = {
        "tornallom": {"key": "normalizedName", "url": "https://tornallom.org/ca/directori/{}/"},
    }
    try:
        return maps[origin]["url"].format(o[maps[origin]["key"]])
    except:
        pass

def get_femlliga_organizations():
    return [
        {
            "name": o.name,
            "lat": o.lat,
            "lng": o.lng,
            "origin": "femlliga",
        }
        for o in Organization.objects.all()
    ]

@cache(datetime.timedelta(days=1))
def get_tornallom_organizations():
    response = requests.post(
        "https://backend.tornallom.org/api/searchEntitiesGeojson?lang=ca",
        json={
            "text": "",
            "sectorIds": [],
            "entityStatusTypes": ["PUBLISHED"],
            "externalFilterTags": [],
        },
    )
    return extract_data(response.json(), "tornallom")
