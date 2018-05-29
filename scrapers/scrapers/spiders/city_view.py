import datetime
from locale import *

import scrapy
from scrapers.items import Apartment

setlocale(LC_NUMERIC, '')


class CityViewSpider(scrapy.Spider):
    name = "city_view"
    start_urls = ['http://www.equityapartments.com/boston/longwood/cityview-at-longwood-apartments']

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapers.pipelines.CityViewPipeline': 100,
        }
    }

    def parse(self, response):
        for row in response.css('.data-view .unit-expanded-card'):
            try:
                specs = row.css('.specs')
                p = specs.css('p')
                price = p[0].css('.pricing::text').extract_first()[1:]
                bed_string = p[1].css('p').extract_first()
                if bed_string.find("Bed") != -1:
                    num_beds = int(bed_string[bed_string.find("Bed") - 2])
                else:
                    num_beds = None

                area_and_floor = p[2].css('span').extract()
                sqft_string = area_and_floor[0]
                if sqft_string.find(">") is not None and sqft_string.find("sq") is not None:
                    sqft = sqft_string[sqft_string.find(">") + 1: sqft_string.find("sq") - 1]
                else:
                    sqft = None

                floor_string = area_and_floor[1]
                if floor_string.find("</") is not None:
                    index = floor_string.find("</") - 2
                    floor = floor_string[index:index + 2]
                else:
                    floor = None

                date_string = p[3].css('p').extract_first()
                date = date_string[date_string.find('<p>') + 3: date_string.find('</p>') - 1].strip()

                date = date[date.find('ble') + 4:]

                date = datetime.datetime.strptime(date, "%m/%d/%Y").date()

                description = [amenity.css('::text').extract_first().strip() for amenity in row.css('.amenity')]

                yield Apartment(
                    price=price,
                    date=date,
                    sqft=sqft,
                    floor=floor,
                    num_beds=num_beds,
                    description=description
                )
            except Exception as e:
                import logging
                logging.error("Exception in parsing apartment", e)
