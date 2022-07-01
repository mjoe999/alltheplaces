# -*- coding: utf-8 -*-
import scrapy
import json
from locations.brands import Brand
from locations.seo import extract_geo, extract_details


class RedLionSpider(scrapy.spiders.SitemapSpider):
    name = "redlion"
    sitemap_urls = ["https://www.redlion.com/sitemap.xml"]
    my_brands = {
        "/americas-best-value-inn/": Brand.from_wikidata("Americas Best Value Inn", "Q4742512"),
        "/canadas-best-value-inn/": Brand.from_wikidata("Canadas Best Value Inn", "Q4742512"),
        "/guesthouse-extended-stay/": Brand.from_wikidata("Guesthouse Extended Stay", "Q4742512"),
        "/knights-inn/": Brand.from_wikidata("Knights Inn", "Q6422409"),
        "/red-lion-hotels/": Brand.from_wikidata("Red Lion Hotels", "Q25047720"),
        "/red-lion-inn-suites/": Brand.from_wikidata("Red Lion Hotels", "Q25047720"),
    }
    download_delay = 1.0

    def sitemap_filter(self, entries):
        for entry in entries:
            for k, v in self.my_brands.items():
                if k in entry["loc"]:
                    yield entry

    def parse(self, response):
        json_link = response.url + "/page-data.json"
        json_link = json_link.replace("redlion.com/", "redlion.com/page-data/")
        yield scrapy.Request(
            json_link,
            callback=self.parse_json_data,
            cb_kwargs=dict(original_response=response),
        )

    def parse_json_data(self, response, original_response):
        hotel = json.loads(response.body)["result"]["data"]["hotel"]
        for k, brand in self.my_brands.items():
            if k in original_response.url:
                item = brand.item(original_response)
                extract_details(item, hotel)
                extract_details(item, hotel["address"])
                item["street_address"] = hotel["address"]["address_line1"]
                item["state"] = hotel["address"].get('administrative_area')
                extract_geo(item, hotel["lat_lon"])
                item["image"] = hotel["banner_images"][0]["url"]
                yield item
                return
