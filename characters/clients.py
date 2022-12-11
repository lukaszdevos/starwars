import csv
from tempfile import TemporaryFile

import petl
from dateutil.parser import parse
from django.core.files import File
from requests import Response

from characters.adapters import SwapiAdapter

CHARACTER_HEADER = [
    "name",
    "height",
    "mass",
    "hair_color",
    "skin_color",
    "eye_color",
    "birth_year",
    "gender",
    "homeworld",
    "edited",
]


class SwapiClient:
    def __init__(self, csv_file: File = None):
        self.csv_file = csv_file
        self.adapter = SwapiAdapter()
        self.header = CHARACTER_HEADER

    def create_characters_csv(self) -> File:
        table = self._fetch_all_characters()
        table = self._convert_edited_date(table)
        table = self._convert_homeworld_planets(table)

        temp = TemporaryFile("w+")
        writer = csv.writer(temp)
        writer.writerows(table)

        return temp

    def _fetch_all_characters(self):
        page = 1
        response = self.adapter.get_characters(page=page)
        table = petl.fromdicts(response.get("results"), header=self.header)
        table = self._fetch_from_other_pages(page, response, table)
        return table

    def _fetch_from_other_pages(
        self, page: int, response: Response, table: petl.Table
    ) -> petl.Table:
        while response.get("next"):
            page += 1
            response = self.adapter.get_characters(page=page)
            table_another_page = petl.fromdicts(
                response.get("results"), header=self.header
            )
            table = petl.cat(table, table_another_page, header=self.header)
        return table

    def _convert_edited_date(self, table: petl.Table) -> petl.Table:
        return petl.convert(
            table, "edited", lambda value: parse(value).strftime("%Y-%m-%d")
        )

    def _convert_homeworld_planets(self, table: petl.Table) -> petl.Table:
        planets = self.fetch_all_planets()
        return petl.convert(table, "homeworld", lambda value: planets[value])

    def fetch_all_planets(self) -> dict[str, str]:
        page = 1
        response = self.adapter.get_planets(page=1)
        results = {r.get("url"): r.get("name") for r in response.get("results")}
        while response.get("next"):
            page += 1
            response = self.adapter.get_planets(page=page)
            page_results = {
                r.get("url"): r.get("name") for r in response.get("results")
            }
            results.update(page_results)
        return results
