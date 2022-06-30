# -*- coding: utf-8 -*-
import scrapy
from locations.brands import Brand
from locations.seo import extract_schema


class SuperdrySpider(scrapy.spiders.SitemapSpider):
    name = "superdry"
    brand = Brand.from_wikidata("Superdry", "Q1684445")
    sitemap_urls = ["https://stores.superdry.com/sitemap.xml"]

    def parse(self, response):
        return extract_schema(self.brand, response)
