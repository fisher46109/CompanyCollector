from main import get_exception_info
from app import app
from config.config import Config
from logger.logger import Logger
from inp_queue.inp_item import Item
from execution.init_required_applications import init_required_applications
from exceptions.custom_exceptions import BusinessException, SystemException
from selenium_functions import selenium_function as sf
from time import sleep
import pandas as pd


app.config = Config()               # create instance of class Config with program configurations
cfg = app.config                    # assign to short the name
cfg.load_config_from_jsons()        # read config from file main_config.json

app.logger = Logger(cfg.logs_on)    # create instance of class Logger based on logs_on flag (enable logs)
logger = app.logger                 # assign to short the name

init_required_applications()

process_result = ''
item_exception: None | Exception = None
act_item: None | Item = None


def test_create_table_from_website_data():

    # url from PDD example
    url1 = 'https://aplikacja.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/EntryChangeHistory.aspx?Id=11e96944-5915-4228-aaf7-639accc4d969&archival=False'

    # url for NIP: 7010936126 - two pages of entry history (after long, long search...)
    url2 = 'https://aplikacja.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/EntryChangeHistory.aspx?Id=5b1c3425-7863-4c80-a19e-d8d7bf65c971&archival=False'

    # url for NIP 6772402279 - four pages of entry history in the FUCKING Banacha street xD
    url3 = 'https://aplikacja.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/EntryChangeHistory.aspx?Id=51cdfd8e-c929-4394-b23a-a19ab0b4ed5e&archival=False'

    try:
        sf.open_browser(url3)
        df = sf.create_table_from_website_data('//*[@id="tableHistory"]')
        print(df)

    except BusinessException as be:
        print(get_exception_info(be))
    except SystemException as se:
        print(get_exception_info(se))
    except Exception as e:
        print(get_exception_info(e))

    sleep(5)