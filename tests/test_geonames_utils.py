from locations.geonames_utils import to_iso_alpha2_country_code


def test_to_iso_alpha2_country_code():
    assert not to_iso_alpha2_country_code(None)
    assert not to_iso_alpha2_country_code("A")
    assert not to_iso_alpha2_country_code("A1")
    assert "GB" == to_iso_alpha2_country_code("GB")
    assert "GB" == to_iso_alpha2_country_code("gb")
    assert "GB" == to_iso_alpha2_country_code("United Kingdom")
    assert "GB" == to_iso_alpha2_country_code("United Kingdom. ")
    assert "GB" == to_iso_alpha2_country_code("GBR")
    assert "GB" == to_iso_alpha2_country_code(" UK ")
