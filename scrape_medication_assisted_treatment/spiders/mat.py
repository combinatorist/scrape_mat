import scrapy


class MatSpider(scrapy.Spider):
    name = "mat"

    start_urls=[
        "https://www.samhsa.gov/medication-assisted-treatment/physician-program-data/treatment-physician-locator?field_bup_physician_us_state_value=TN"
    ]

    def parse(self, response):
        yield {
            "type": "page",
            "url": response.url,
            "body": response.body.decode(),
            "tables": self.parse_tables(response)
        }

        for a in response.css('li.pager__item--next a'):
            yield response.follow(a, callback=self.parse)

    def parse_tables(self, response):
        return [
            {
                "type": "table",
                "raw": table.extract(),
                "rows": self.parse_rows(table),
            }
            for table in response.css("table.tablesaw")
        ]

    def parse_rows(self, table):
        return [
            {
                "type": "row",
                "raw": row.extract(),
                "is_header": row.css("th").extract_first() is not None,
                "fields": self.parse_fields(row),
            }
            for row in table.css("tr")
        ]

    def parse_fields(self, row):
        return [
            {
                "type": "field",
                "raw": field.extract(),
                "text": field.css("::text").extract(),
                "clean": field.css("::text").extract_first().strip(),
            }
            for field in row.css("td")
        ] + [
            {
                "type": "field",
                "raw": field.extract(),
                "text": field.css("::text").extract(),
                "clean": field.css("::text").extract_first().strip(),
            }
            for field in row.css("th")
        ]
