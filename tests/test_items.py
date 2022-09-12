from locations.items import GeojsonPointItem


def test_geo_methods():
    item = GeojsonPointItem()

    assert not item.has_geo()
    assert not item.set_geo(0, 0).has_geo()
    assert not item.set_geo(91.0, 1.0).has_geo()
    assert not item.set_geo(-91.0, 1.0).has_geo()
    assert not item.set_geo(1.0, -181.0).has_geo()
    assert not item.set_geo(1.0, 181.0).has_geo()

    assert item.set_geo(1.0, 0).has_geo()

    assert item.set_geo(1.0, 2.0).has_geo()
    assert item.set_geo("-90.0", "-180.0").has_geo()
    assert item.set_geo("90.0", "180.0").has_geo()

    item["lat"] = "1.0"
    item["lon"] = 2.0
    assert item.has_geo()
    assert isinstance(item["lat"], float)

    item["lat"] = "1.0"
    item["lon"] = "2.0"
    assert item.has_geo()
    assert item["lat"] == 1.0
    assert item["lon"] == 2.0
