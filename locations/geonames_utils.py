import geonamescache

gc = geonamescache.GeonamesCache()

# All keys in this dict should be lower case.
UNHANDLED_COUNTRY_MAPPINGS = {
    "uk": "GB",
}


def to_iso_alpha2_country_code(country_str):
    if not country_str:
        return None
    # Clean up some common appendages we see on country strings.
    country_str = country_str.strip().replace(".", "")
    if len(country_str) < 2:
        return None
    if len(country_str) == 2:
        # Check for the clean/fast path, spider has given us a 2-alpha iso country code.
        if gc.get_countries().get(country_str.upper()):
            return country_str.upper()
    if len(country_str) == 3:
        # Check for a 3-alpha code, this is done by iteration.
        country_str = country_str.upper()
        for country in gc.get_countries().values():
            if country["iso3"] == country_str:
                return country["iso"]
    # Failed so far, now let's try a match by name.
    country_name = country_str.lower()
    for country in gc.get_countries().values():
        if country["name"].lower() == country_name:
            return country["iso"]
    # Finally let's go digging in the random country string collection!
    return UNHANDLED_COUNTRY_MAPPINGS.get(country_name)
