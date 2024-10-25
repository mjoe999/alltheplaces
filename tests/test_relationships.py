import pytest
import scrapy

from locations.items import Feature, set_located_in
from locations.pipelines.extract_gb_postcode import UK_MOTHER_BRANDS, located_in_gb_retail
from locations.spiders.sainsburys import SainsburysSpider


def test_missing_item_attributes():
    with pytest.raises(AttributeError):
        set_located_in(scrapy.Spider, Feature())


def test_empty_dict():
    with pytest.raises(AttributeError):
        set_located_in({}, Feature())


def test_relationship_via_dict():
    item = Feature()
    set_located_in({"brand": "sample", "brand_wikidata": "Q1"}, item)
    assert item.get("located_in") == "sample"
    assert item.get("located_in_wikidata") == "Q1"


def test_relationship_via_spider():
    item = Feature()
    set_located_in(SainsburysSpider, item)
    assert item.get("located_in") == "Sainsbury's"
    assert item.get("located_in_wikidata") == "Q152096"


def test_gb_success_lookup():
    item = Feature()
    item["name"] = "fjfjf in Sainsbury's central"
    item["country"] = "GB"
    assert located_in_gb_retail(item)


def test_gb_failed_lookup():
    item = Feature()
    item["country"] = "GB"
    assert not located_in_gb_retail(item, test_str="no brands here!")


def test_gb_retail_map():
    item = Feature()
    item["country"] = "GB"
    for k, v in UK_MOTHER_BRANDS.items():
        assert located_in_gb_retail(item, test_str=k)
