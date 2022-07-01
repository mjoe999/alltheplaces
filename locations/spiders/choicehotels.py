# -*- coding: utf-8 -*-
import scrapy
import json
import re
from locations.seo import extract_details, get_first_key
from locations.brands import Brand


# The implementation ignores "collection" hotels. This may want to be re-visited but they
# should not be branded Choice Hotels in common with other branded hotel collections
class ChoiceHotelsSpider(scrapy.spiders.SitemapSpider):
    name = "choicehotels"
    allowed_domains = ["choicehotels.com"]
    sitemap_urls = ["https://www.choicehotels.com/propertysitemap.xml"]
    my_brands = {
        "Ascend Hotel Collection": None,
        "Cambria Hotel": Brand.from_wikidata("Cambria Hotel", "Q1075788"),
        "Clarion Hotel": Brand.from_wikidata("Clarion Hotel", "Q78165540"),
        "Clarion Hotel & Suites": Brand.from_wikidata(
            "Clarion Hotel & Suites", "Q78165540"
        ),
        "Clarion Inn": Brand.from_wikidata("Clarion Inn", "Q78165540"),
        "Clarion Inn & Suites": Brand.from_wikidata(
            "Clarion Inn & Suites", "Q78165540"
        ),
        "Clarion Pointe": Brand.from_wikidata("Clarion Pointe", "Q78165540"),
        "Clarion Suites": Brand.from_wikidata("Clarion Suites", "Q78165540"),
        "Comfort Hotel": Brand.from_wikidata("Comfort Hotel", "Q1075788"),
        "Comfort Inn": Brand.from_wikidata("Comfort Inn", "Q1075788"),
        "Comfort Inn & Suites": Brand.from_wikidata("Comfort Inn & Suites", "Q1075788"),
        "Comfort Suites": Brand.from_wikidata("Comfort Suites", "Q1075788"),
        "Econo Lodge": Brand.from_wikidata("Econo Lodge", "Q5333330"),
        "MainStay Suites": Brand.from_wikidata("MainStay Suites", "Q1075788"),
        "Quality Hotel": Brand.from_wikidata("Quality Hotel", "Q1075788"),
        "Quality Hotel & Suites": Brand.from_wikidata(
            "Quality Hotel & Suites", "Q1075788"
        ),
        "Quality Inn": Brand.from_wikidata("Quality Inn", "Q1075788"),
        "Quality Suites": Brand.from_wikidata("Quality Suites", "Q1075788"),
        "Quality Inn & Suites": Brand.from_wikidata("Quality Inn & Suites", "Q1075788"),
        "Rodeway Inn": Brand.from_wikidata("Rodeway Inn", "Q7356709"),
        "Rodeway Inn & Suites": Brand.from_wikidata("Rodeway Inn & Suites", "Q7356709"),
        "Sleep Inn": Brand.from_wikidata("Sleep Inn", "Q1075788"),
        "Sleep Inn & Suites": Brand.from_wikidata("Sleep Inn & Suites", "Q1075788"),
        "Suburban Extended Stay Hotel": Brand.from_wikidata(
            "Suburban Extended Stay Hotel", "Q1075788"
        ),
        "WoodSpring Suites": Brand.from_wikidata("WoodSpring Suites", "Q30672853"),
    }
    brand_name_override = {
        "Cambria Hotel & Suites": "Cambria Hotel",
        "Comfort Resort": "Comfort Hotel",
        "Comfort Suites Suites": "Comfort Suites",
        "Econo Lodge Lodge": "Econo Lodge",
        "Econo Lodge Inn & Suites": "Econo Lodge",
        "Quality Resort": "Quality Hotel",
    }
    download_delay = 1.0

    def parse(self, response):
        if (
            "/test-hotels" in response.url
            or "/notavail/" in response.url
            or "/ascend-hotels/" in response.url
        ):
            return
        script = "".join(response.xpath("//script/text()").extract())
        matched = re.search(r"window.PRELOADED_STATE = (.*)?;", script)
        data = json.loads(matched.group(1))
        property_entry = get_first_key(data, "property")
        if not property_entry or property_entry["status"] != "ACTIVE":
            return
        brand_name = "{} {}".format(
            property_entry["brandName"].strip(), property_entry["productName"].strip()
        )
        brand_name = self.brand_name_override.get(brand_name, brand_name)
        brand = self.my_brands.get(brand_name)
        if not brand:
            self.logger.error(">>>>>> no brand for %s %s", brand_name, response.url)
            return
        item = brand.item(response)
        extract_details(item, property_entry)
        address = property_entry["address"]
        extract_details(item, address)
        item["street_address"] = address["line1"]
        item["state"] = address.get("subdivision")
        # Add a nice exterior image link if possible
        for entry in get_first_key(property_entry, "images"):
            if "Exterior" == entry.get("categoryCode"):
                item["image"] = "https://www.choicehotels.com" + entry["backupUrl"]
                break
        yield item
