import requests

from urllib.parse import urlencode, quote_plus
from requests import Session


def exact_search(url: str, query: str, session: Session, debug=False, full_url=False):
    # headers = {'accept': 'application/json'}

    if full_url:
        resp = session.get(query)
        resp.raise_for_status()

        resp_json = resp.json().get('data')['products']

        return resp_json

    params = {
        'query': query,
        'debug': debug,
    }
    # user_request = 'http://exactmatch-common.wbxsearch-internal.svc.k8s.wbxsearch-dl/v2/search?'

    response = session.get(url, params=params)

    response.raise_for_status()

    response_json = response.json()

    return response_json


def get_exact_batch(url: str, session: Session, human_queries: list[str]) -> dict:
    json_body = {'query': human_queries}

    # url = (
    #     'http://proxy-search.wbxsearch-internal.svc.k8s.wbxsearch-dp/'
    #     'exactmatch/v2batch/search'
    # )

    response = session.post(url=url, json=json_body)

    response.raise_for_status()

    response_json = response.json()

    return response_json
