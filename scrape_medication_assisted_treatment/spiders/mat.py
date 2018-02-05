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
            "table": response.css("table.tablesaw").extract_first(),
            "rows": response.css("table.tablesaw tr").extract(),
            "fields": [x.strip() for x in response.css("table.tablesaw tr td::text").extract()],
        }
