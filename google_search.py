from googleapiclient.discovery import build

import settings


def search(keyword):
    try:
        service = build('customsearch', 'v1', developerKey=settings.API_KEY, cache_discovery=False)
        response = service.cse().list(q=keyword, cx=settings.CSE_ID, num=settings.RESULTS_COUNT).execute()
    except Exception as e:
        print(e)
        result = ''
    else:
        result = response['items']
    return '\n'.join([ele['link'] for ele in result]) if result else result
