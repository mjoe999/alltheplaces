import base64
import hashlib
from scrapy.exporters import JsonLinesItemExporter, JsonItemExporter
from scrapy.utils.python import to_bytes


mapping = (
    ("addr_full", "addr:full"),
    ("housenumber", "addr:housenumber"),
    ("street", "addr:street"),
    ("street_address", "addr:street_address"),
    ("city", "addr:city"),
    ("state", "addr:state"),
    ("postcode", "addr:postcode"),
    ("country", "addr:country"),
    ("name", "name"),
    ("phone", "phone"),
    ("website", "website"),
    ("twitter", "contact:twitter"),
    ("facebook", "contact:facebook"),
    ("opening_hours", "opening_hours"),
    ("image", "image"),
    ("brand", "brand"),
    ("brand_wikidata", "brand:wikidata"),
    ("located_in", "located_in"),
    ("located_in_wikidata", "located_in:wikidata"),
)


def item_to_properties(item):
    props = {"ref": str(item["ref"])}

    if extras := item.get("extras"):
        props.update(extras)

    # Bring in the optional stuff
    for map_from, map_to in mapping:
        if item_value := item.get(map_from):
            props[map_to] = item_value

    return props


def compute_hash(item):
    ref = str(item.get("ref") or "").encode("utf8")
    sha1 = hashlib.sha1(ref)

    if spider_name := item.get("extras", {}).get("@spider"):
        sha1.update(spider_name.encode("utf8"))

    return base64.urlsafe_b64encode(sha1.digest()).decode("utf8")


def build_feature(item):
    feature = [
        ("type", "Feature"),
        ("id", compute_hash(item)),
        ("properties", item_to_properties(item)),
    ]
    if item.has_geo():
        feature.append(
            (
                "geometry",
                {
                    "type": "Point",
                    "coordinates": [item["lon"], item["lat"]],
                },
            )
        )
    return feature


class LineDelimitedGeoJsonExporter(JsonLinesItemExporter):
    def _get_serialized_fields(self, item, default_value=None, include_empty=None):
        return build_feature(item)


class GeoJsonExporter(JsonItemExporter):
    def _get_serialized_fields(self, item, default_value=None, include_empty=None):
        return build_feature(item)

    def start_exporting(self):
        self.file.write(
            to_bytes('{"type":"FeatureCollection","features":[', self.encoding)
        )

    def finish_exporting(self):
        self.file.write(to_bytes("]}", self.encoding))
