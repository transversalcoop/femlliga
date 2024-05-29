import datetime
import requests

from .utils import cache


def extract_data(response, origin):
    if response["status"] != 200:
        raise Exception("Bad response")

    return [
        {
            "name": o["properties"]["name"],
            "lat": o["geometry"]["coordinates"][1],
            "lng": o["geometry"]["coordinates"][0],
            "origin": origin,
        }
        for o in response["response"]
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
