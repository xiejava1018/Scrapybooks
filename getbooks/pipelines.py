# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from os.path import join, basename, dirname
from urllib.parse import urlparse

import requests
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import item, Request
from scrapy.pipelines.files import FilesPipeline


class GetbooksPipeline:
    def process_item(self, item, spider):
        return item



class KgBookFilePipeline(FilesPipeline):

    def get_media_requests(self,item,info):
        yield Request(item['book_url'],meta={'book_file':item['book_file']})

    def file_path(self, request, response=None, info=None):
        file_name=request.meta.get('book_file')
        return file_name


