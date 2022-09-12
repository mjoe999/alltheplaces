# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GeojsonPointItem(scrapy.Item):
    lat = scrapy.Field()
    lon = scrapy.Field()
    name = scrapy.Field()
    addr_full = scrapy.Field()
    housenumber = scrapy.Field()
    street = scrapy.Field()
    street_address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    postcode = scrapy.Field()
    country = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    twitter = scrapy.Field()
    facebook = scrapy.Field()
    opening_hours = scrapy.Field()
    image = scrapy.Field()
    ref = scrapy.Field()
    brand = scrapy.Field()
    brand_wikidata = scrapy.Field()
    located_in = scrapy.Field()
    located_in_wikidata = scrapy.Field()
    extras = scrapy.Field()

    def has_geo(self) -> bool:
        """
        Is the POI considered to have a valid position set, "null island" is considered invalid.
        As a side affect will convert any non-float coordinates as best effort to be float values.
        :return: true iff both latitude and longitude have non-zero float values within world bounds
        """
        if lat_val := self.get("lat"):
            lat_val = self["lat"] = float(lat_val)
        elif lat_val is None:
            return False
        if lon_val := self.get("lon"):
            lon_val = self["lon"] = float(lon_val)
        elif lon_val is None:
            return False
        if lat_val == 0 and lon_val == 0:
            return False
        return -90.0 <= lat_val <= 90.0 and -180.0 <= lon_val <= 180.0

    def set_geo(self, lat, lon) -> "GeojsonPointItem":
        """
        Set the position of the POI.
        :param lat: item latitude
        :param lon: item longitude
        :return: this instance
        """
        self["lat"] = float(lat)
        self["lon"] = float(lon)
        return self
