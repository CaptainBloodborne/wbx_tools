from requests import Session


def get_entry_by_query(url: str, data: str, session: Session, dsmp_token: str) -> list[dict] | dict:
    # match query_type:
    #     case 'by_query':
    #         url = os.environ.get('GET_BY_QUERY')
    #     case 'by_human_query':
    #         url = os.environ.get('GET_BY_HUMAN_QUERY')
    #     case 'by_norm_query':
    #         url = os.environ.get('GET_BY_NORM_QUERY')
    #     case _:
    #         url = os.environ.get('GET_BY_QUERY')

    response = session.get(
        url=f'{url}?query={data}',
        headers={
            'Authorization': f'Bearer {dsmp_token}',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; '
            'rv:108.0) Gecko/20100101 Firefox/108.0',
        },
    )

    response.raise_for_status()

    if response.status_code == 200:
        response_json = response.json()
        return response_json
    elif response.status_code in [404, 405]:
        return {}