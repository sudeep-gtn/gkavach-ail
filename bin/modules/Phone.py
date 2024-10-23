#!/usr/bin/env python3
# -*-coding:UTF-8 -*

"""
The Phone Module
================

This module is consuming the Redis-list created by the Categ module.

It apply phone number regexes on item content and warn if above a threshold.

"""

##################################
# Import External packages
##################################
import os
import re
import sys
import phonenumbers

sys.path.append(os.environ['AIL_BIN'])
##################################
# Import Project packages
##################################
from modules.abstract_module import AbstractModule
from lib.objects.Items import Item

# # TODO: # FIXME:  improve regex / filter false positives
class Phone(AbstractModule):
    """
    Phone module for AIL framework
    """

    # regex to find phone numbers, may raise many false positives (shalt thou seek optimization, upgrading is required)
    # reg_phone = re.compile(r'(\+\d{1,4}(\(\d\))?\d?|0\d?)(\d{6,8}|([-/\. ]{1}\d{2,3}){3,4})')
    REG_PHONE = re.compile(r'(\+\d{1,4}(\(\d\))?\d?|0\d?)(\d{6,8}|([-/\. ]{1}\(?\d{2,4}\)?){3,4})')

    def __init__(self):
        super(Phone, self).__init__()

        # Waiting time in seconds between to message processed
        self.pending_seconds = 1

    def compute(self, message):
        item = Item(message)
        content = item.get_content()
        # List of the regex results in the Item, may be null
        results = self.REG_PHONE.findall(content)

        # If the list is greater than 4, we consider the Item may contain a list of phone numbers
        if len(results) > 4:
            self.logger.debug(results)
            self.redis_logger.warning(f'{item.get_id()} contains PID (phone numbers)')

            msg = f'infoleak:automatic-detection="phone-number";{item.get_id()}'
            self.add_message_to_queue(msg, 'Tags')

            stats = {}
            for phone_number in results:
                try:
                    x = phonenumbers.parse(phone_number, None)
                    country_code = x.country_code
                    if stats.get(country_code) is None:
                        stats[country_code] = 1
                    else:
                        stats[country_code] = stats[country_code] + 1
                except:
                    pass
            for country_code in stats:
                if stats[country_code] > 4:
                    self.redis_logger.warning(f'{item.get_id()} contains Phone numbers with country code {country_code}')


if __name__ == '__main__':
    module = Phone()
    module.run()
