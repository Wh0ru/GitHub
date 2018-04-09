import requests
from faker import Faker

class HtmlDownloader(object):

    def download(self,url):
        if url is None:
            return None
        user=Faker()
        headers={
            'User-Agent':user.user_agent()
        }
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.content.decode()
        return None