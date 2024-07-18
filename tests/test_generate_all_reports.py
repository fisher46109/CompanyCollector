from app import app
from config.config import Config
from logger.logger import Logger
from inp_queue.inp_item import Item
from execution.init_required_applications import init_required_applications
from exceptions.custom_exceptions import BusinessException, SystemException
from inp_queue.inp_queue import Queue
from main_process.company_data import CompanyData
from main import get_exception_info
from output_handling.output_handling import generate_all_reports
import pandas as pd


app.config = Config()               # create instance of class Config with program configurations
cfg = app.config                    # assign to short the name
cfg.load_config_from_jsons()        # read config from file main_config.json

app.logger = Logger(cfg.logs_on)    # create instance of class Logger based on logs_on flag (enable logs)
logger = app.logger                 # assign to short the name

init_required_applications()

app.inp_queue = Queue()
app.inp_queue.act_item = Item()


def test_generate_all_reports():

    company_data = CompanyData()

    company_data.firm_name = '------'
    company_data.first_name = 'Andrzej'
    company_data.last_name = 'Twarów'
    company_data.nip = '6770062655'
    company_data.regon = '350378569'
    company_data.address = 'woj. MAŁOPOLSKIE, pow. krakowski, gm. Czernichów, miejsc. CZERNICHÓW, nr 193, 32-070'
    company_data.status = 'Aktywny'
    company_data.start_date = '1992-01-02'
    company_data.end_date = '-'
    company_data.table_of_entry_history = pd.read_csv('history.csv', sep=';', index_col=False)

    try:
        generate_all_reports('C:\\Users\\fisher46109\\Documents\\TempCompanyCollector\\Output\\MJBAR_20240523_113123', company_data)
    except BusinessException as be:
        print(get_exception_info(be))
    except SystemException as se:
        print(get_exception_info(se))
    except Exception as e:
        print(get_exception_info(e))