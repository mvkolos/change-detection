from .constants import GEOSERVER_URL, DEFAULT_WORKSPACE, GEOSERVER_LOGIN, GEOSERVER_PASSWORD
import requests


def post_geotiff(path, name):
    request = {
        "coverageStore": {
            "name": name,
            "workspace": DEFAULT_WORKSPACE,
            "enabled": "true",
            "type": "GeoTIFF",
            "url": '{path}/{name}.tif'.format(path, name)
        }
    }
    url = '{}/rest/workspaces/{}/coveragestores'.format(GEOSERVER_URL, DEFAULT_WORKSPACE)
    session = requests.Session()
    session.auth = (GEOSERVER_LOGIN, GEOSERVER_PASSWORD)
    session.headers('Content-Type', 'application/json')
    return session.post(url, request)



