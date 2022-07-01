# -*- coding: utf-8 -*-
import scrapy
import json
import re
from locations.brands import Brand
from locations.seo import parse_ldjson


class RedRoofSpider(scrapy.spiders.SitemapSpider):
    name = "redroof"
    RED_ROOF_INN = Brand.from_wikidata("Red Roof Inn", "Q7304949")
    HOME_TOWNE_STUDIOS = Brand.from_wikidata("HomeTowne Studios", "Q109868848")
    sitemap_urls = ["https://www.redroof.com/sitemap.xml"]
    sitemap_rules = [
        ("/hometownestudios/property/", "parse_hometowne_studios"),
        ("/property/", "parse_redroof"),
    ]
    download_delay = 1.0

    def parse_hometowne_studios(self, response):
        # TODO: parse the embedded JSON variable, too few POIs for today!
        self.logger.info("HomeTowne Studios: %s", response.url)

    def parse_redroof(self, response):
        hotel_code = response.url.split("/")[-1]
        json_url = "https://storage.googleapis.com/redroof/properties/{}.js".format(
            hotel_code
        )
        yield scrapy.Request(
            json_url,
            callback=self.parse_red_roof_json,
            cb_kwargs=dict(original_response=response),
        )

    def parse_red_roof_json(self, response, original_response):
        pattern = re.compile("({.*})")
        matches = pattern.search(response.text)
        json_data = json.loads(matches.group(1))
        return parse_ldjson(self.RED_ROOF_INN, json_data, "Hotel", original_response)
