# -*- coding: utf-8 -*-
import json

import requests


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CityViewPipeline(object):
    def process_item(self, item, spider):
        if item['num_beds'] == 2 and item['date'].month > 7:
            requests.post("https://api.flock.com/hooks/sendMessage/4eeac7dd-5819-4c8d-896c-9ab7b9da0d7a",
                          data=json.dumps(
                              {
                                  "text": "Apartment available at city view",
                                  "flockml": "Apartment available at City view from <strong>{}</strong>, costing ${}, floor {}, sq ft {}".format(
                                      item['date'].isoformat(), item['price'], item['floor'], item['sqft'])
                              }))
            return item
