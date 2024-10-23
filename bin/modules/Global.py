#!/usr/bin/env python3
# -*-coding:UTF-8 -*
"""
The ZMQ_Feed_Q Module
=====================

This module is consuming the Redis-list created by the ZMQ_Feed_Q Module,
And save the item on disk to allow others modules to work on them.

..todo:: Be able to choose to delete or not the saved item after processing.

..note:: Module ZMQ_Something_Q and ZMQ_Something are closely bound, always put
the same Subscriber name in both of them.

Requirements
------------

*Need running Redis instances.
*Need the Mixer or the Importer Module running to be able to work properly.

"""

##################################
# Import External packages
##################################
import base64
import io
import gzip
import os
import sys
import time

from hashlib import md5
from uuid import uuid4

sys.path.append(os.environ['AIL_BIN'])
##################################
# Import Project packages
##################################
from modules.abstract_module import AbstractModule
from lib.ail_core import get_ail_uuid
from lib.ConfigLoader import ConfigLoader
from lib.data_retention_engine import update_obj_date
from lib.objects.Items import Item

# from lib import Statistics

class Global(AbstractModule):
    """
    Global module for AIL framework
    """

    def __init__(self):
        super(Global, self).__init__()

        self.processed_item = 0
        self.time_last_stats = time.time()

        config_loader = ConfigLoader()

        # Get and sanitize ITEM DIRECTORY
        # # TODO: rename PASTE => ITEM
        self.ITEMS_FOLDER = os.path.join(os.environ['AIL_HOME'], config_loader.get_config_str("Directories", "pastes")) + '/'
        self.ITEMS_FOLDER = os.path.join(os.path.realpath(self.ITEMS_FOLDER), '')

        # Waiting time in seconds between to message processed
        self.pending_seconds = 0.5

        # Send module state to logs
        self.logger.info(f"Module {self.module_name} initialized")

    def computeNone(self):
        difftime = time.time() - self.time_last_stats
        if int(difftime) > 30:
            to_print = f'Global; ; ; ;glob Processed {self.processed_item} item(s) in {difftime} s'
            print(to_print)
            self.redis_logger.debug(to_print)

            self.time_last_stats = time.time()
            self.processed_item = 0

    def compute(self, message, r_result=False):
        # Recovering the streamed message informations
        splitted = message.split()

        if len(splitted) == 2:
            item, gzip64encoded = splitted

            # Remove ITEMS_FOLDER from item path (crawled item + submitted)
            if self.ITEMS_FOLDER in item:
                item = item.replace(self.ITEMS_FOLDER, '', 1)

            file_name_item = item.split('/')[-1]
            if len(file_name_item) > 255:
                new_file_name_item = '{}{}.gz'.format(file_name_item[:215], str(uuid4()))
                item = self.rreplace(item, file_name_item, new_file_name_item, 1)

            # Creating the full filepath
            filename = os.path.join(self.ITEMS_FOLDER, item)
            filename = os.path.realpath(filename)

            # Incorrect filename
            if not os.path.commonprefix([filename, self.ITEMS_FOLDER]) == self.ITEMS_FOLDER:
                self.logger.warning(f'Global; Path traversal detected {filename}')
                print(f'Global; Path traversal detected {filename}')

            else:
                # Decode compressed base64
                decoded = base64.standard_b64decode(gzip64encoded)
                new_file_content = self.gunzip_bytes_obj(filename, decoded)

                if new_file_content:
                    filename = self.check_filename(filename, new_file_content)

                    if filename:
                        # create subdir
                        dirname = os.path.dirname(filename)
                        if not os.path.exists(dirname):
                            os.makedirs(dirname)

                        with open(filename, 'wb') as f:
                            f.write(decoded)

                        item_id = filename
                        # remove self.ITEMS_FOLDER from
                        if self.ITEMS_FOLDER in item_id:
                            item_id = item_id.replace(self.ITEMS_FOLDER, '', 1)

                        item = Item(item_id)

                        update_obj_date(item.get_date(), 'item')

                        self.add_message_to_queue(item_id, 'Item')
                        self.processed_item += 1

                        # DIRTY FIX AIL SYNC - SEND TO SYNC MODULE
                        # # FIXME:  DIRTY FIX
                        message = f'{item.get_type()};{item.get_subtype(r_str=True)};{item.get_id()}'
                        print(message)
                        self.add_message_to_queue(message, 'Sync')

                        print(item_id)
                        if r_result:
                            return item_id

        else:
            self.logger.debug(f"Empty Item: {message} not processed")
            print(f"Empty Item: {message} not processed")

    def check_filename(self, filename, new_file_content):
        """
        Check if file is not a duplicated file
        return the filename if new file, else None
        """

        # check if file exist
        if os.path.isfile(filename):
            self.logger.info(f'File already exist {filename}')
            print(f'File already exist {filename}')

            # Check that file already exists but content differs
            curr_file_content = self.gunzip_file(filename)

            if curr_file_content:
                # Compare file content with message content with MD5 checksums
                curr_file_md5 = md5(curr_file_content).hexdigest()
                new_file_md5 = md5(new_file_content).hexdigest()

                if new_file_md5 != curr_file_md5:
                    # MD5 are not equals, verify filename
                    if filename.endswith('.gz'):
                        filename = f'{filename[:-3]}_{new_file_md5}.gz'
                    else:
                        filename = f'{filename}_{new_file_md5}'
                    self.logger.debug(f'new file to check: {filename}')

                    if os.path.isfile(filename):
                        # Ignore duplicate
                        self.logger.debug(f'ignore duplicated file {filename}')
                        print(f'ignore duplicated file {filename}')
                        filename = None

                else:
                    # Ignore duplicate checksum equals
                    self.logger.debug(f'ignore duplicated file {filename}')
                    print(f'ignore duplicated file {filename}')
                    filename = None

            else:
                # File not unzipped
                filename = None

        return filename

    def gunzip_file(self, filename):
        """
        Unzip a file
        publish stats if failure
        """
        curr_file_content = None

        try:
            with gzip.open(filename, 'rb') as f:
                curr_file_content = f.read()
        except EOFError:
            self.logger.warning(f'Global; Incomplete file: {filename}')
            print(f'Global; Incomplete file: {filename}')
            # save daily stats
            # self.r_stats.zincrby('module:Global:incomplete_file', 1, datetime.datetime.now().strftime('%Y%m%d'))
            # Statistics.
        except OSError:
            self.logger.warning(f'Global; Not a gzipped file: {filename}')
            print(f'Global; Not a gzipped file: {filename}')
            # save daily stats
            # self.r_stats.zincrby('module:Global:invalid_file', 1, datetime.datetime.now().strftime('%Y%m%d'))

        return curr_file_content

    # # TODO: add stats incomplete_file/Not a gzipped file
    def gunzip_bytes_obj(self, filename, bytes_obj):
        gunzipped_bytes_obj = None
        try:
            in_ = io.BytesIO()
            in_.write(bytes_obj)
            in_.seek(0)

            with gzip.GzipFile(fileobj=in_, mode='rb') as fo:
                gunzipped_bytes_obj = fo.read()
        except Exception as e:
            self.logger.warning(f'Global; Invalid Gzip file: {filename}, {e}')
            print(f'Global; Invalid Gzip file: {filename}, {e}')

        return gunzipped_bytes_obj

    def rreplace(self, s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)


if __name__ == '__main__':

    module = Global()
    module.run()
