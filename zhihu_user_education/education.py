import requests
from lxml import etree
# from faker import Faker
import threading
from proxy import *
from DataOutput import *

def get_follow(url,headers,follow_set,output):
    # p=Proxy()
    host='http:{}'
    threads=[]
    response=requests.get(url,headers=headers)
    content=response.content.decode()
    # print(content)
    html=etree.HTML(content)
    follow_urls=html.xpath(".//img[@class='Avatar Avatar--large UserLink-avatar']/parent::a/@href")
    for follow in follow_urls:
        if follow not in follow_set:
            follow_set.add(follow)
            follow2=host.format(follow)
            # f=threading.Thread(target=get_url,args=(follow2,follow_set,output))
            # threads.append(f)
            get_url(follow2,follow_set,output)
            # print(follow_set)
        else:
            pass
    # for t in threads:
    #     t.start()

def get_info(html,output):
    try:
        data={}
        data['school']=''.join(html.xpath(".//svg[@class='Icon Icon--education']/parent::div/parent::div/text()[1]"))
        data['username']=''.join(html.xpath(".//span[@class='ProfileHeader-name']/text()"))
        if data['school']:
            print(data['school'])
            print(data['username'])
            output.store_data(data)
            # output.output_end()
    except:
        pass

def get_url(url,follow_set,output):
    # p=Proxy()
    headers = {
        'Cookie':'*******',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        # 'Proxy-Authorization':p.auth
    }
    host_url = 'https://www.zhihu.com{}'
    response=requests.get(url,headers=headers)
    # print(response.headers)
    content = response.content.decode()
    # print(content)
    html = etree.HTML(content)
    follow_button1 = ''.join(html.xpath(".//a[@class='Button NumberBoard-item Button--plain'][1]/@href"))
    follow_button = host_url.format(follow_button1)
    # print(follow_button)
    get_info(html,output)
    get_follow(follow_button,headers,follow_set,output)

output=DataOutput()
follow_set=set()
root_url='https://www.zhihu.com/***/***'#个人主页
get_url(root_url,follow_set,output)
output.output_end()
