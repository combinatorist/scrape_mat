import scrapy


class MatSpider(scrapy.Spider):
    name = "mat"

    start_urls=[
        "https://www.samhsa.gov/medication-assisted-treatment/physician-program-data/treatment-physician-locator?field_bup_physician_us_state_value=TN"
    ]

    def parse(self, response):
        def parse_fields(row):
            return [
                {
                    "raw": field.extract(),
                    "text": field.css("::text").extract(),
                    "clean": field.css("::text").extract_first().strip(),
                }
                for field in row.css("td")
            ]

        def parse_rows(table):
            return [
                {
                    "raw": row.extract(),
                    "fields": parse_fields(row),
                }
                for row in table.css("tr")
            ]

        def parse_tables(response):
            return [
                {
                    "raw": table.extract(),
                    "rows": parse_rows(table),
                }
                for table in response.css("table.tablesaw")
            ]

        yield {
            "url": response.url,
            "body": response.body.decode(),
            "tables": parse_tables(response)
        }
