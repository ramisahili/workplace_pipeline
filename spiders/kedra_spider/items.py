import scrapy

class WorkplaceItem(scrapy.Item):
    body_id = scrapy.Field()
    body_name = scrapy.Field()
    page = scrapy.Field()
    ref_no = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    partition_date = scrapy.Field()
    file_path = scrapy.Field()
