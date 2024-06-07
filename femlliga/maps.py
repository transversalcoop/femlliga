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
        "sobiraniaalimentariapv": {"key": "slug", "url": "https://mapa.sobiranialimentariapv.org/?id={}"},
        "pamapam": {"key": "id", "url": "https://pamapam.cat/directori/{}/"},
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


@cache(datetime.timedelta(days=1))
def get_pamapam_organizations():
    response = requests.post(
        "https://pamapam.cat/services/searchEntitiesGeojson",
        json={"text": "", "sectorIds": [], "refererDomain": None, "apiKey": None},
    )
    return extract_data(response.json(), "pamapam")


@cache(datetime.timedelta(days=1))
def get_sobiraniaalimentariapv_organizations():
    response = requests.get("https://mapa.sobiranialimentariapv.org/map_points/?l=ca")
    return extract_data(response.json(), "sobiraniaalimentariapv")
