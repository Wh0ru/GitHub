import requests
from lxml import etree
from faker import Faker
import threading
'''
http://antiserver.kuwo.cn/anti.s?format=aac|mp3&rid=MUSIC_24720751&type=convert_url&response=res
http://antiserver.kuwo.cn/anti.s?format=aac|mp3&rid=MUSIC_15249349&type=convert_url&response=res
'''

def download_music(url,headers,name):
    root='{}.mp3'
    music_root=root.format(name)
    response=requests.get(url,headers=headers)
    with open(music_root, 'wb')as f:
        f.write(response.content)


faker=Faker()
bang_list=['酷我飙升榜','酷我华语榜','经典怀旧榜','夜店舞曲榜','网红新歌榜','热门影视榜','酷音乐流行榜']
for i in bang_list:
    print('{}:{}'.format(bang_list.index(i),i))
bang_index=input("Please input the number of bang:")
bang_name=bang_list[int(bang_index)]
# print(bang_name)
url="http://www.kuwo.cn/bang/content?name={}".format(bang_name)
# name='酷我华语榜'
i=0
thread=[]
music_url2='http://antiserver.kuwo.cn/anti.s?format=aac|mp3&rid=MUSIC_{}&type=convert_url&response=res'
headers={
    'User-Agent':faker.user_agent(),
}
response=requests.get(url,headers=headers)
content=response.content.decode()
html=etree.HTML(content)
music_list=html.xpath(".//ul[@class='listMusic']/li//div[@class='name']/a/@href")
# print(music_list)
music_names=html.xpath(".//ul[@class='listMusic']/li//div[@class='name']/a/text()")
for music,name in zip(music_list,music_names):
    if i==10:
        break
    music_id1=music.split('/')[4]
    music_id=music_id1.split('?')[0]
    music_url=music_url2.format(music_id)
    # print(music_id)
    # print(music_url)
    f=threading.Thread(target=download_music,args=(music_url,headers,name))
    # download_music(music_url,headers,name)
    thread.append(f)
    i+=1
for t in thread:
    t.start()