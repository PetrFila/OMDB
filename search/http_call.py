import requests
from .api_key import omdb


def get_title_from_OMDB(request):

    payload = {'apikey': omdb['api_key'],
               't': request.GET['title'],
               'type': request.GET['type'],
               'plot': 'full'}

    if request.GET['type'] == '':
        payload.pop('type')

    try:
        omdb_url = omdb['url']
        r = requests.get(omdb_url, params=payload, timeout=3)
        r.raise_for_status()
        if r.status_code == 200:
            return r.json()

    except NameError as ne:
        return str(ne).capitalize()

    except ImportError as ie:
        return str(ie).capitalize()

    except FileNotFoundError as fe:
        return str(fe).capitalize()

    except requests.exceptions.HTTPError:
        return 'HTTP Error with the external API'

    except requests.exceptions.ConnectionError:
        return 'Connection Error to the external API'

    except requests.exceptions.Timeout:
        return 'Connection Timeout to the external API'

    except requests.exceptions.RequestException:
        return 'Something went wrong'
