from HtmlDownload import *
from DataOutput import *
from HtmlParser import *
from lxml import etree

class SpiderMan(object):
    def __init__(self):
        self.download=HtmlDownloader()
        self.parser=HtmlParser()
        self.output=DataOutput()

    def crawl(self,root_url):
        url_host='https://movie.douban.com{}'
        i=2
        while True:
            content=self.download.download(root_url)
            html=etree.HTML(content)
            max_link=int(''.join(html.xpath(".//span[@data-total-page]/@data-total-page")))
            next_link = ".//div[@class='paginator']/a[{}]/@href".format(i)
            next_links=''.join(html.xpath(next_link))
            details=html.xpath(".//div[@class='main-bd']/h2/a/@href")
            for detail in details:
                text=self.download.download(detail)
                datas=self.parser.parser(text)
                self.output.store_data(datas)
            root_url=url_host.format(next_links)
            i+=1
            if i>max_link:
                break
        self.output.output_end()

if __name__=='__main__':
    spider=SpiderMan()
    spider.crawl('https://movie.douban.com/review/best/')




