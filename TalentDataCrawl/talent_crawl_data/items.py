import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity


def strip_space(value):
    return value.strip();


class NewspaperItem(scrapy.Item):
    url = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    summary = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    title = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    content = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    source = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    published_date = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Join(),
    )
    images = scrapy.Field(
        input_processor=MapCompose(strip_space),
        output_processor=Identity(),
    )
    indexed_date = scrapy.Field()
