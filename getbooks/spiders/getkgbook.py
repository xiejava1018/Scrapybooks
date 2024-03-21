import os
import re
import scrapy
from getbooks.items import KgbookItem


class GetkgbookSpider(scrapy.Spider):
    name = "getkgbook"  #爬虫的名称
    allowed_domains = ["kgbook.com"]   #爬取的网站
    start_urls = ["https://kgbook.com"]  #爬取的首页

    def parse(self, response):
        categorys = response.xpath('//div[@id="category"]/div/ul/li/a')
        for category in categorys[0:1]:
            category_url = category.xpath('./@href').extract_first()
            url=response.urljoin(category_url)
            #爬取进入到目录页
            yield response.follow(url, self.parse_booklist)

    #解析目录页
    def parse_booklist(self,response):
        book_list_select=response.css('.channel-item h3.list-title a')
        #获取书籍列表
        for book_info_select in book_list_select[0:1]:
            book_name=book_info_select.css('::text').extract_first()
            book_detail_url=book_info_select.css('::attr(href)').extract_first()
            book_detail_url=response.urljoin(book_detail_url)
            print(book_name,book_detail_url)
            yield scrapy.Request(url=book_detail_url, callback=self.pase_bookdetail)
        #翻页
        nextpage_url = response.xpath('//div[@class="pagenavi"]/a[contains(text(), "下一页")]/@href').extract_first()
        if nextpage_url:
            yield response.follow(nextpage_url, self.parse_booklist)

    #解析详情页
    def pase_bookdetail(self,response):
        navegate=response.xpath('//nav[@id="location"]/a')
        if len(navegate)>1:
            book_category=navegate[1].xpath('./text()').extract_first()
        book_name=response.css('.news_title::text').extract_first()
        book_author=response.xpath('//div[@id="news_details"]/ul/li[contains(text(),"作者")]/text()').extract_first()
        pattern=re.compile('mobi|epub|azw3|pdf',re.I) #解析书籍的类型
        book_download_urls=response.xpath('//div[@id="introduction"]/a[@class="button"]')
        for book_download_urlinfo in book_download_urls:
            book_type=book_download_urlinfo.re(pattern)
            if book_type:
                book_download_url=book_download_urlinfo.xpath('./@href').extract_first()
                #获取要下载的书籍的名称、作者、要保存的路径、下载地址
                item=KgbookItem()
                item['book_name']=book_name
                item['book_author']=book_author
                item['book_file']=os.path.join(book_category,book_name+"."+str(book_type[0]).lower())
                item['book_url']=book_download_url
                print(book_name,book_author,book_download_url,item['book_file'])
                return item

