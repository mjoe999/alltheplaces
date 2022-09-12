import random
import logging
from locations.items import GeojsonPointItem
from locations.pipelines import CleanGeoPointPipeline
from scrapy.exceptions import DropItem


class TestSpider:
    ignore_missing_position = False
    logger = logging.getLogger('Testing')


def test_empty_position_rejected():
    try:
        CleanGeoPointPipeline().process_item(GeojsonPointItem(), TestSpider())
        assert False
    except DropItem:
        pass


def test_empty_position_ignore_flag():
    spider = TestSpider()
    spider.ignore_missing_position = True
    CleanGeoPointPipeline().process_item(GeojsonPointItem(), spider)


def test_abort_spurious_positions():
    spurious_position_items = [
        GeojsonPointItem(),
        GeojsonPointItem().set_geo(1.0, 1.0),
        GeojsonPointItem().set_geo(0.0, 1.0),
        GeojsonPointItem().set_geo(1.0, 0.0),
    ]
    good_count = bad_count = 0
    pipeline = CleanGeoPointPipeline()
    spider = TestSpider()
    for i in range(0, 3 * pipeline.VIOLATION_LIMIT):
        try:
            pipeline.process_item(random.choice(spurious_position_items), spider)
            good_count += 1
        except DropItem:
            bad_count += 1
    assert pipeline.VIOLATION_LIMIT == good_count
    assert 2 * pipeline.VIOLATION_LIMIT == bad_count
