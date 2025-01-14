from scrapy.spiders import SitemapSpider

from locations.items import Feature
from locations.pipelines.address_clean_up import clean_address
from locations.user_agents import BROWSER_DEFAULT


class DominosPizzaFRSpider(SitemapSpider):
    name = "dominos_pizza_fr"
    item_attributes = {"brand": "Domino's", "brand_wikidata": "Q839466"}
    allowed_domains = ["dominos.fr"]
    user_agent = BROWSER_DEFAULT
    sitemap_urls = ["https://www.dominos.fr/sitemap.aspx"]
    sitemap_rules = [
        (
            r"https:\/\/www\.dominos\.fr\/magasin\/([-\w.]+)_(unknown|[\d]+)$",
            "parse_store",
        )
    ]

    def parse_store(self, response):
        properties = {
            "ref": response.url,
            "name": response.xpath('//h2[@class="storetitle"]/text()').extract_first(),
            "addr_full": clean_address(response.xpath('//a[@id="open-map-address"]/text()').extract()),
            "lat": response.xpath('//input[@id="store-lat"]/@value').get().replace(",", "."),
            "lon": response.xpath('//input[@id="store-lon"]/@value').get().replace(",", "."),
            "phone": response.xpath('//div[@class="store-phone"]/a/text()').get(),
            "website": response.url,
        }
        yield Feature(**properties)
