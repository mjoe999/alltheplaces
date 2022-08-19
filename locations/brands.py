# -*- coding: utf-8 -*-
from locations.items import GeojsonPointItem


class Brand:

    def __init__(self, brand_name, brand_wikidata):
        self.brand_name = brand_name
        self.brand_wikidata = brand_wikidata

    def __str__(self):
        return self.brand_name

    def name(self):
        return self.brand_name

    def wikidata(self):
        return self.brand_wikidata

    @staticmethod
    def from_wikidata(brand_name, brand_wikidata):
        return Brand(brand_name, brand_wikidata)

    def apply(self, item):
        item['brand'] = self.brand_name
        item['brand_wikidata'] = self.brand_wikidata

    def item(self, response_or_url=None):
        item = GeojsonPointItem()
        self.apply(item)
        if not response_or_url:
            return item
        if isinstance(response_or_url, str):
            url = response_or_url
        else:
            url = response_or_url.url
        item['website'] = url
        # Use the individual POI URL as the ref, can always be re-worked in the spider if not appropriate
        item['ref'] = url
        return item
