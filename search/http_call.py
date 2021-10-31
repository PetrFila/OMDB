import requests


def get_title_from_OMDB(request):
    try:
        omdb_url = 'http://www.omdbapi.com/'
        payload = {'apikey': '2f18a196',
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
