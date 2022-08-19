# -*- coding: utf-8 -*-
import html
import json
import scrapy

from locations.brands import Brand
from locations.dict_parser import DictParser


class BestWesternSpider(scrapy.spiders.SitemapSpider):
    name = "bestwestern"
    brands = [
        Brand.from_wikidata("Best Western Premier", "Q830334"),
        Brand.from_wikidata("Best Western Plus", "Q830334"),
        Brand.from_wikidata("Aiden by Best Western", "Q830334"),
        Brand.from_wikidata("Sure Hotel", "Q830334"),
        Brand.from_wikidata("Surestay Plus", "Q830334"),
        Brand.from_wikidata("Surestay", "Q830334"),
        Brand.from_wikidata("Best Western", "Q830334"),
    ]
    allowed_domains = ["bestwestern.com"]
    sitemap_urls = ["https://www.bestwestern.com/etc/seo/bestwestern/hotels.xml"]
    sitemap_rules = [(r"/en_US/book/hotels-in-.*\.html", "parse_hotel")]
    download_delay = 0.5

    def parse_hotel(self, response):
        hotel_details = response.xpath(
            '//div[@id="hotel-details-info"]/@data-hoteldetails'
        ).get()
        if hotel_details:
            hotel = json.loads(html.unescape(hotel_details))["summary"]
            for brand in self.brands:
                if hotel["name"].lower().startswith(brand.name().lower()):
                    item = DictParser.parse(hotel, brand.item(response))
                    item["street_address"] = hotel["address1"]
                    item["ref"] = hotel["resort"]
                    return item
