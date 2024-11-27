import requests
from typing import Optional

class GoogleImageSearch:
    def __init__(self, api_key: str, search_engine_id: str):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        
    def search_image(self, query: str) -> Optional[str]:
        """Search for an image and return its URL"""
        try:
            url = 'https://www.googleapis.com/customsearch/v1'
            params = {
                'q': query,
                'key': self.api_key,
                'cx': self.search_engine_id,
                'searchType': 'image',
                'num': 1
            }

            response = requests.get(url, params=params)
            data = response.json()

            if 'items' in data:
                return data['items'][0]['link']
            return None
        except Exception as e:
            print(f"Image search error: {e}")
            return None