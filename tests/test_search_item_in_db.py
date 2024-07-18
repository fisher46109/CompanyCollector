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


def test_search_item_in_db():

    print('')
    try:

        while True:
            act_item = app.inp_queue.get_item()
            if not act_item:
                break
            virtual_process(act_item)
        print('ok')

    except BusinessException as be:
        print(str(be))
    except SystemException as se:
        print(str(se))
    except Exception as e:
        print(str(e))


def virtual_process(act_item: Item):

    print(f'{act_item.id} {act_item.investigator} {act_item.city} {act_item.street} {act_item.status} {act_item.comment}')

    if act_item.id == 10001:
        app.inp_queue.update_values('S', '')
    if act_item.id == 10002:
        app.inp_queue.update_values('S', 'COŚ')
    if act_item.id == 10003:
        app.inp_queue.update_values('F', 'FCOŚ')