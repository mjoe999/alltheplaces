# -*- coding: utf-8 -*-
import scrapy
from locations.brands import Brand
from locations.seo import extract_schema


class JewsonUKSpider(scrapy.spiders.SitemapSpider):
    name = "jewson_uk"
    brand = Brand.from_wikidata("Jewson", "Q6190226")
    sitemap_urls = ["https://www.jewson.co.uk/sitemap/sitemap_branches_jewson.xml"]

    def parse(self, response):
        for item in extract_schema(self.brand, response, False):
            item.set_geo(
                response.xpath("//@data-latitude").get(),
                response.xpath("//@data-longitude").get(),
            )
            yield item
