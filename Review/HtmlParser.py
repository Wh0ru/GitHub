from lxml import etree

class HtmlParser(object):
    def parser(self,html_cont):
        if html_cont is None:
            return
        soup=etree.HTML(html_cont)
        new_data=self._get_new_data(soup)
        return new_data

    def _get_new_data(self,response):
        i={}
        i['title']=''.join(response.xpath(".//span[@property='v:summary']/text()"))
        i['author']=''.join(response.xpath(".//span[@property='v:reviewer']/text()"))
        i['movie']=''.join(response.xpath(".//header[@class='main-hd']/a[2]/text()"))
        i['rank']=''.join(response.xpath(".//span[@property='v:rating']/text()"))
        i['content']=''.join(response.xpath(".//div[@property='v:description']/p/text()"))
        i['movie_type']=''.join(response.xpath(".//ul[@class='info-list']/li[3]/span[2]/text()"))
        print(i)
        return i

