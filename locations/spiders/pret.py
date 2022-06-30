# -*- coding: utf-8 -*-
import scrapy
from locations.brands import Brand
from locations.seo import extract_schema


class PretSpider(scrapy.spiders.SitemapSpider):
    name = "pret"
    brand = Brand.from_wikidata("PRET", "Q2109109")
    sitemap_urls = [
        "https://locations.pret.co.uk/sitemap.xml",
        "https://locations.pret.com/sitemap.xml",
        "https://locations.pretamanger.fr/sitemap.xml",
    ]

    def parse(self, response):
        if "order-online" not in response.url:
            return extract_schema(self.brand, response)
