import scrapy
from ..items import WorkplaceItem
from urllib.parse import urlencode


class WorkplaceSpider(scrapy.Spider):
    name = "workplace"
    allowed_domains = ["workplacerelations.ie"]

    def __init__(self, start_date="1/1/2025", end_date="1/8/2025", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_date = start_date
        self.end_date = end_date

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.workplacerelations.ie/en/search/?advance=true",
            callback=self.parse_bodies
        )

    def parse_bodies(self, response):
        checkboxes = response.css('input[type="checkbox"][id^="CB2_"]')

        for checkbox in checkboxes:
            value = checkbox.attrib.get("value")
            input_id = checkbox.attrib.get("id")
            label_text = response.css(f'label[for="{input_id}"]::text').get()

            if value and label_text:
                body_id = value.strip()
                body_name = label_text.strip()
                yield self.request_search_page(body_id, body_name, page=1)

    def request_search_page(self, body_id, body_name, page):
        query = {
            "decisions": 1,
            "from": self.start_date,
            "to": self.end_date,
            "body": body_id,
            "pageNumber": page
        }
        ## log start date and end date
        self.logger.info(f"[{body_name}] Scraping page {page} from {self.start_date} to {self.end_date}")

        url = "https://www.workplacerelations.ie/en/search/?" + urlencode(query)
        return scrapy.Request(
            url=url,
            callback=self.parse_search_results,
            cb_kwargs={"body_id": body_id, "body_name": body_name, "page": page}
        )

    def parse_search_results(self, response, body_id, body_name, page):
        items = response.css("li.each-item.clearfix")

        if not items:
            self.logger.info(f"[{body_name}] No more items on page {page}")
            return

        for item in items:
            title = item.css("h2.title::text").get(default="").strip()
            link = item.css("h2.title a::attr(href)").get()
            if link:
                link = response.urljoin(link)

            date = item.css("span.date::text").get(default="").strip()
            description = (
                item.css("div.description::text").get()
                or item.css("p::text").get()
            )
            if description:
                description = description.strip()

            ref_no = (
                item.css("div.refno::text").get()
                or item.css("div.col-sm-9.ref span + span::text").get(default="").strip()
            )

            yield WorkplaceItem(
                body_id=body_id,
                body_name=body_name,
                page=page,
                ref_no=ref_no,
                title=title,
                date=date,
                description=description,
                link=link
            )

        yield self.request_search_page(body_id, body_name, page + 1)
