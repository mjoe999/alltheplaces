from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from locations.brands import Brand
from locations.seo import extract_schema


class FatFaceSpider(CrawlSpider):
    name = "fatface"
    brand = Brand.from_wikidata("FATFACE", "Q5437186")
    allowed_domains = ["fatface.com"]
    start_urls = ["https://www.fatface.com/stores"]
    rules = [Rule(LinkExtractor(allow="/store/"), callback="parse_func", follow=False)]

    def parse_func(self, response):
        for item in extract_schema(self.brand, response, False):
            item.set_geo(
                response.xpath("//@data-latitude").get(),
                response.xpath("//@data-longitude").get(),
            )
            if item.has_geo():
                yield item
