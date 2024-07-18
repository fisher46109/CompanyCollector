from app import app
from inp_queue.inp_queue import get_item
from inp_queue.inp_item import Item
from config.config import Config
from logger.logger import Logger
from agent_handler.agent_handler import AgentHandler
from main_process.process_item import process_item
from execution.init_required_applications import init_required_applications
from exceptions.custom_exceptions import BusinessException, SystemException
from main import get_exception_info
from ending_process.end_process import end_process
from execution.one_time_program import one_time_program
from execution.idle_process import idle_process
from execution.idle_process_initialization import idle_process_initialization
from execution.handling_end_process_item import end_process_item


def execute():
    """ Main process logic """

    app.config = Config()  # create instance of class Config with program configurations
    cfg = app.config  # assign to short the name
    cfg.load_config_from_jsons()  # read config from file main_config.json

    app.logger = Logger(cfg.logs_on)  # create instance of class Logger based on logs_on flag (enable logs)
    logger = app.logger  # assign to short the name

    app.agent = AgentHandler()

    process_result = ''
    item_exception: None | Exception = None
    act_item: None | Item = None

    try:
        while True:
            if app.agent.stop_bot_flag():
                break
            if not act_item:    # if no act_item from last loop course
                act_item = get_item()
            if not act_item:    # if no act_item from queue
                if one_time_program():
                    break
                idle_process()
                continue
            try:
                init_required_applications()  # init applications required to process item
            except SystemException as se:  # system exceptions cause a retry of operation without processing act item
                idle_process_initialization(se, act_item)
                continue
            try:
                process_item(act_item)
            except Exception as e:
                item_exception = e
            act_item = end_process_item(item_exception, act_item)
            item_exception = None
        process_result = 'Success'
    except (BusinessException, SystemException) as e:
        logger.log_to_business_and_operational(str(e), logger.ERROR)
        process_result = e
    except Exception as e:
        logger.log_to_operational(str(e), logger.ERROR)
        process_result = get_exception_info(e)
    finally:
        end_process(process_result)



