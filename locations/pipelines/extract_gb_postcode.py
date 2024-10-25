import re

import scrapy

from locations.items import Feature, set_located_in
from locations.spiders.aldi_sud_gb import AldiSudGBSpider
from locations.spiders.asda_gb import AsdaGBSpider
from locations.spiders.chevron_us import ChevronUSSpider
from locations.spiders.coop_food_gb import CoopFoodGBSpider
from locations.spiders.costcutter_gb import CostcutterGBSpider
from locations.spiders.exxon_mobil import ExxonMobilSpider
from locations.spiders.homebase_gb_ie import HomebaseGBIESpider
from locations.spiders.lidl_gb import LidlGBSpider
from locations.spiders.londis_gb import LondisGBSpider
from locations.spiders.morrisons_gb import MorrisonsGBSpider
from locations.spiders.nisalocal_gb import NisalocalGBSpider
from locations.spiders.one_stop_gb import OneStopGBSpider
from locations.spiders.premier_gb import PremierGBSpider
from locations.spiders.sainsburys import SainsburysSpider
from locations.spiders.scotmid_gb import ScotmidGBSpider
from locations.spiders.shell import ShellSpider
from locations.spiders.spar_gb import SparGBSpider
from locations.spiders.superdrug import SuperdrugSpider
from locations.spiders.tesco_gb import TescoGBSpider
from locations.spiders.waitrose import WaitroseSpider
from locations.spiders.whsmith import WhsmithSpider


class ExtractGBPostcodePipeline:
    def process_item(self, item, spider):
        if item.get("country") == "GB":
            if item.get("addr_full") and not item.get("postcode"):
                item["postcode"] = extract_gb_postcode(item["addr_full"])
        elif item.get("country") == "IE":
            if item.get("addr_full") and not item.get("postcode"):
                if postcode := re.search(
                    r"([AC-FHKNPRTV-Y][0-9]{2}|D6W)[ -]?([0-9AC-FHKNPRTV-Y]{4})", item["addr_full"].upper()
                ):
                    item["postcode"] = "{} {}".format(postcode.group(1), postcode.group(2))
        return item


def extract_gb_postcode(s: str):
    """
    Look for first occurrence, if any, of a GB format postcode in a string.
    :param s: the string to search for a GB postcode
    :return: the first candidate postcode instance, None if not present
    """
    s = s.upper()
    if postcode := re.search(r"(\w{1,2}\d{1,2}\w? \d\w{2})", s):
        return postcode.group(1)
    if postcode := re.search(r"(\w{1,2}\d{1,2}\w?) O(\w{2})", s):
        return postcode.group(1) + " 0" + postcode.group(2)
    return None


def simplify_name(name: str):
    if name:
        return re.sub(r"[^A-Za-z ]+", "", name)
    return ""


# A list of brands in the UK which are well known to "host" other well known brands.
UK_MOTHER_BRANDS = {
    "sainsburys": SainsburysSpider,
    "tesco": TescoGBSpider,
    "whsmith": WhsmithSpider,
    "morrisons": MorrisonsGBSpider.MORRISONS,
    "waitrose": WaitroseSpider,
    "scotmid": ScotmidGBSpider,
    "superdrug": SuperdrugSpider,
    "homebase": HomebaseGBIESpider,
    "londis": LondisGBSpider,
    "costcutter": CostcutterGBSpider,
    "lidl": LidlGBSpider,
    "aldi": AldiSudGBSpider,
    "coop": CoopFoodGBSpider,
    "co op": CoopFoodGBSpider,
    "asda": AsdaGBSpider,
    "nisa": NisalocalGBSpider,
    "onestop": OneStopGBSpider,
    "one stop": OneStopGBSpider,
    "premier": PremierGBSpider,
    "shell": ShellSpider,
    "esso": ExxonMobilSpider.ESSO,
    "spar": SparGBSpider,
    "texaco": ChevronUSSpider.TEXACO,
}


def located_in_gb_retail(item: Feature, test_str: str = None, spider: scrapy.Spider = None) -> bool:
    """
    Many branded POIs are in fact located within or about a larger branded instance. The relationship
    is in many cases detectable from the name / attributes of the "enclosed" feature.
    :param item: the feature that may be associated in/with a retail brand
    :param test_str: a string to test for retail brand name, if not the feature will be introspected
    :param spider: update statistics counters if supplied
    :return:
    """
    if not item.get("country") == "GB":
        return False

    if test_str:
        test_str = simplify_name(test_str)
    else:
        test_str = " ".join([simplify_name(item.get("name")), simplify_name(item.get("branch"))])
    test_str = test_str.lower()

    for k, v in UK_MOTHER_BRANDS.items():
        if k in test_str:
            set_located_in(v, item, spider)
            return True

    return False
