from datetime import datetime
import os
from app import app
from .files_handling import create_business_logs_folder, create_operational_logs_folder
from inp_queue.inp_item import Item


class Logger:
    """ Class of handling logs """

    def __init__(self, logs_on_flag: bool = True):
        """ Creation of business and operational logs folders, and sending information about start of process """

        # flag of enabling logs
        self.logs_on_flag = logs_on_flag

        # constant strings for levels of logs
        self.INFO = 'INFO'
        self.WARN = 'WARN'
        self.ERROR = 'ERROR'

        # path for logs folders
        self.business_logs_folder_path = ''
        self.operational_logs_folder_path = ''

        # initalize if logs_on_flag enabled
        if self.logs_on_flag:
            self.business_logs_folder_path = create_business_logs_folder()
            self.operational_logs_folder_path = create_operational_logs_folder()
            self.log_to_business_and_operational('Start of work', self.INFO)

    def log_to_business(self, message: str, log_level: str = ''):
        """ Formatting business log and safe it to specify file """

        if not self.logs_on_flag:   # leave function iflogs_on_flag is disabled
            return
        act_time = datetime.now()
        log_time = act_time.strftime('%Y-%m-%d %H:%M:%S')
        log_time_to_name = act_time.strftime('%Y-%m')
        bot_name = app.config.bot_name
        if log_level == '':
            log_level = self.INFO   # for unidentified log level set INFO level
        file_name = f"BusinessLogs_{log_time_to_name}.txt"
        file_path = os.path.join(self.business_logs_folder_path, file_name)

        with open(file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f'{log_time};{bot_name};{log_level};{message}\n')

    def log_to_operational(self, message: str, log_level: str = ''):
        """ Formatting operational log and safe it to specify file """

        if not self.logs_on_flag:  # leave function iflogs_on_flag is disabled
            return
        act_time = datetime.now()
        log_time = act_time.strftime('%Y-%m-%d %H:%M:%S')
        log_time_to_name = act_time.strftime('%Y-%m-%d')
        bot_name = app.config.bot_name
        if log_level == '':
            log_level = self.INFO  # for unidentified log level set INFO level
        file_name = f"OperationalLogs_{log_time_to_name}.txt"
        file_path = os.path.join(self.operational_logs_folder_path, file_name)

        with open(file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f'{log_time};{bot_name};{log_level};{message}\n')

    def log_to_business_and_operational(self, message: str, log_level: str = ''):
        """ Sending business and operational logs together """

        self.log_to_business(message, log_level)
        self.log_to_operational(message, log_level)

    @staticmethod
    def log_start_of_processing(act_item: Item):
        """ Log start of processing specified item or next attempt"""

        if act_item.attempt_number == 1:
            app.logger.log_to_business_and_operational(f'Start of processing item from queue: ID: {act_item.id}', app.logger.INFO)
        else:
            app.logger.log_to_business_and_operational(f'Start {act_item.attempt_number}. attempt...', app.logger.INFO)
