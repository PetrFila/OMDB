import requests
try:
    from .api_key import omdb
except ImportError:
    raise SystemExit("""
An OMDB API Key is required to run this application. search/api_key.py should be created in with the template:

omdb = {
    'url': 'http://www.omdbapi.com/',
    'api_key': '<API_KEY_KEYE>'
}
    """)


def get_title_from_OMDB(request):
    try:
        omdb_url = omdb['url']
        payload = {'apikey': omdb['api_key'],
                   't': request.POST['title'],
                   'type': request.POST['type'],
                   'plot': 'full'}
        r = requests.get(omdb_url, params=payload, timeout=3)
        r.raise_for_status()
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.HTTPError:
        return 'HTTP Error with the external API'

    except requests.exceptions.ConnectionError:
        return 'Connection Error to the external API'

    except requests.exceptions.Timeout:
        return 'Connection Timeout to the external API'

    except requests.exceptions.RequestException:
        return 'Something went wrong'
