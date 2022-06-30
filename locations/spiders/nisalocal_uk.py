# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from locations.brands import Brand
from locations.seo import extract_schema


class NisaLocalUKSpider(CrawlSpider):
    name = "nisalocal_uk"
    brand = Brand.from_wikidata("Nisa Local", "Q16999069")
    allowed_domains = ["nisalocally.co.uk"]
    start_urls = ["https://www.nisalocally.co.uk/stores/index.html"]
    rules = [Rule(LinkExtractor(allow=".*/stores/.*"), callback="parse", follow=True)]

    def parse(self, response):
        return extract_schema(self.brand, response)
