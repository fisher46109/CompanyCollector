from main_process.process_item import process_item
from app import app
from config.config import Config
from logger.logger import Logger
from inp_queue.inp_item import Item
from execution.init_required_applications import init_required_applications
from exceptions.custom_exceptions import BusinessException,SystemException
from inp_queue.inp_queue import Queue


app.config = Config()               # create instance of class Config with program configurations
cfg = app.config                    # assign to short the name
cfg.load_config_from_jsons()        # read config from file main_config.json

app.logger = Logger(cfg.logs_on)    # create instance of class Logger based on logs_on flag (enable logs)
logger = app.logger                 # assign to short the name

init_required_applications()

app.inp_queue = Queue()
app.inp_queue.act_item = Item()


def test_process_item():
    item1 = Item()              # few results

    item1.id = 10001
    item1.investigator = 'MB'
    item1.city = 'Kraków'
    item1.street = 'krótka'
    item1.status = ''
    item1.comment = ''
    item1.attempt_number = 1

    item2 = Item()

    item2.id = 10002            # more results than displayed
    item2.investigator = 'MB'
    item2.city = 'Kraków'
    item2.street = 'Banacha'
    item2.status = ''
    item2.comment = ''
    item2.attempt_number = 1

    item3 = Item()

    item3.id = 10003            # no results
    item3.investigator = 'MB'
    item3.city = 'Warszawa'
    item3.street = 'polityczny'
    item3.status = ''
    item3.comment = ''
    item3.attempt_number = 1

    item4 = Item()

    item4.id = 10004  # one result
    item4.investigator = 'MB'
    item4.city = 'Kazimierza Wielka'
    item4.street = 'Łabądź'
    item4.status = ''
    item4.comment = ''
    item4.attempt_number = 1

    print('')
    try:
        process_item(item1)
    except BusinessException as be:
        print(str(be))
    except SystemException as se:
        print(str(se))
    except Exception as e:
        print(str(e))
