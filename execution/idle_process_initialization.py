from app import app
from time import sleep
from selenium_functions import selenium_function as sf
from main import get_exception_info
from exceptions.custom_exceptions import SystemException
from inp_queue.inp_item import Item


def idle_process_initialization(sys_exc: SystemException, act_item: Item ):
    """ Try to kill all processes disturbing initialization and wait time idle_time_for_initialization [s] to next try """

    # Try to kill all processes disturbing initialization
    sf.quit_driver_if_opened()

    # Send operational log with detail
    app.logger.log_to_operational(f'Error occurred during processing Item {act_item.id} initialization. The initialization will start again.'
                                  f'Reason: {get_exception_info(sys_exc)}')
    if act_item.attempt_number < app.config.max_tries:
        app.logger.log_to_operational(f'Start {act_item.attempt_number + 1}. attempt...')
    else:
        app.logger.log_to_operational(f'Max try number exceeded, item will be skipped')

    # Wait time idle_time_for_initialization for next try of initialization
    sleep(app.config.idle_time_for_initialization)

