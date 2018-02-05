import scrapy


class MatSpider(scrapy.Spider):
    name = "mat"

    start_urls=[
        "https://www.samhsa.gov/medication-assisted-treatment/physician-program-data/treatment-physician-locator?field_bup_physician_us_state_value=TN"
    ]

    def parse(self, response):
        yield {
            "url": response.url,
            "body": response.body.decode(),
            "tables": self.parse_tables(response)
        }

    def parse_tables(self, response):
        return [
            {
                "raw": table.extract(),
                "rows": self.parse_rows(table),
            }
            for table in response.css("table.tablesaw")
        ]

    def parse_rows(self, table):
        return [
            {
                "raw": row.extract(),
                "fields": self.parse_fields(row),
            }
            for row in table.css("tr")
        ]

    def parse_fields(self, row):
        return [
            {
                "raw": field.extract(),
                "text": field.css("::text").extract(),
                "clean": field.css("::text").extract_first().strip(),
            }
            for field in row.css("td")
        ]
