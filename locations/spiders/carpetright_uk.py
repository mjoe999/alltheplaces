# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from locations.brands import Brand
from locations.seo import extract_schema


class CarpetrightUKSpider(CrawlSpider):
    name = "carpetright_uk"
    brand = Brand.from_wikidata("carpetright", "Q5045782")
    allowed_domains = ["carpetright.co.uk"]
    start_urls = ["https://www.carpetright.co.uk/store/near-me"]
    rules = [Rule(LinkExtractor(allow="/store/"), callback="parse", follow=True)]

    def parse(self, response):
        return extract_schema(self.brand, response)
