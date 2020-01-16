from googleapiclient.discovery import build

import settings


def search(keyword, number_of_results=settings.RESULTS_COUNT):
    """Searches the keyword using Google custom search API.

    :param keyword: Keyword needs to be search.
    :param number_of_results: Number of results to fetch defaults to defined in settings.
    :return: Links of searched results.
    """
    try:
        service = build('customsearch', 'v1', developerKey=settings.API_KEY, cache_discovery=False)
        response = service.cse().list(q=keyword, cx=settings.CSE_ID, num=number_of_results).execute()
    except Exception as e:
        print(e)
        result = ''
    else:
        result = response['items']
    return '\n'.join([ele['link'] for ele in result]) if result else result
