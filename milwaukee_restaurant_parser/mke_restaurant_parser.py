import asyncio
import logging
from dataclasses import dataclass
from datetime import date
from typing import List

from dateutil import parser
import aiohttp
from bs4 import BeautifulSoup


@dataclass
class MilwaukeeFacilityInformation:
    facility_id: str
    name: str
    address: str
    score: int | None
    last_inspection_date: date | None
    status: str

@dataclass
class MilwaukeeFacilitySearch:
    facility_id: str
    name: str
    address: str | None
    sub_type: str | None


BASE_URL = "https://healthinspection.healthspace.com/clients/wi/Milwaukee/Web.nsf/"
TIMEOUT = aiohttp.ClientTimeout(total=30)


async def get_facility(facility_id: str) -> MilwaukeeFacilityInformation:
    async with aiohttp.ClientSession(base_url=BASE_URL, timeout=TIMEOUT, connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(
                f"formFacility.xsp?id={facility_id}&module=Food") as response:
            response.raise_for_status()
            html = await response.text()

    parsed = BeautifulSoup(html, features="html.parser")

    name_element = parsed.find("span", id="view:_id1:_id200:nameCF1")
    address_element = parsed.find("span", id="view:_id1:_id200:facilityAddressCF1")
    score_element = parsed.find("span", id="view:_id1:_id200:ScoreCF1")
    last_inspection_date_element = parsed.find("span", id="view:_id1:_id200:lastInspectionCF1")
    status_element = parsed.find("span", id="view:_id1:_id200:statusCF1")

    return MilwaukeeFacilityInformation(
        facility_id=facility_id,
        name=name_element.text,
        address=address_element.text,
        score=try_parse_int(score_element.text),
        last_inspection_date=try_parse_date(last_inspection_date_element.text),
        status=status_element.text,
    )

async def search_facilities(search: str) -> List[MilwaukeeFacilitySearch]:
    async with aiohttp.ClientSession(base_url=BASE_URL, timeout=TIMEOUT, connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(
                f"restQuery.xsp/searchFacilities?query={search}&maxcount=50&module=Food&viewname=XPagesFacilitiesByType&source=util_searchEstablishments.cc") as response:
            response.raise_for_status()
            search_results = await response.json()

    return [MilwaukeeFacilitySearch(facility_id=result['unid'], name=result['name'], address=result.get('Address'), sub_type=result.get('SubType')) for result in search_results]


def try_parse_date(value, default=None) -> date | None:
    try:
        return parser.parse(value).date()
    except (ValueError, TypeError):
        return default


def try_parse_int(value, default=None) -> int | None:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


async def main():
    search_results = await search_facilities("wy'east")
    print(search_results)
    facility = await get_facility(search_results[0].facility_id)
    print(facility)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
