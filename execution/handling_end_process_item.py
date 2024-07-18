from exceptions.custom_exceptions import BusinessException, SystemException
from execution.status_item import StatusItem
from inp_queue.inp_item import Item
from inp_queue.inp_queue import set_output_values_to_database
from logger.files_handling import move_temp_business_logs, move_temp_operational_logs
from main import get_exception_info
from selenium_functions import selenium_function as sf
from app import app
from output_handling.output_handling import move_reports_folder_to_output


def end_process_item(item_exception: None | Exception, act_item: Item) -> None | Item:
    """ Check success or exceptions occurrence,
        Set specified status_item
        Move output files to output
        Set specified values to item in queue
    """

    status_item = None

    if item_exception:  # any exception
        if isinstance(item_exception, BusinessException):                   # if BusinessException (do not retry)
            status_item = handle_business_exception_in_queue(item_exception, act_item)
            act_item = None  # to ensure no retry
        elif isinstance(item_exception, SystemException):                   # if SystemException (retry)
            status_item = handle_system_exception_in_queue(item_exception, act_item)
        else:
            raise item_exception   # other exceptions
    else:   # no exceptions - process success
        status_item = handle_success(act_item)
        act_item = None  # to ensure no retry

    # Move logs and reports to CompanyCollector output folder
    move_temp_business_logs()
    move_temp_operational_logs()
    move_reports_folder_to_output()

    # set values to specified item in database
    set_output_values_to_database(status_item)

    return act_item


def handle_success(act_item: Item) -> None | StatusItem:
    """ Set status item with success (no exceptions occurred) """

    status_item = StatusItem()
    status_item.id = act_item.id

    if act_item.nip_info.number_of_found == 0:
        status_item.status = 'S'
        status_item.comment = ''
        app.logger.log_to_business_and_operational(f'End of processing item with success', app.logger.INFO)
    elif act_item.nip_info.number_of_found == act_item.nip_info.numer_of_displayed:
        status_item.status = 'S'
        status_item.comment = ''
        app.logger.log_to_business_and_operational(f'End of processing item with success', app.logger.INFO)
    elif act_item.nip_info.number_of_found > act_item.nip_info.numer_of_displayed:
        status_item.status = 'P'
        status_item.comment = f'Found {act_item.nip_info.numer_of_displayed} out of {act_item.nip_info.number_of_found}'
        app.logger.log_to_business_and_operational(f'End of processing item with found {act_item.nip_info.numer_of_displayed} out of {act_item.nip_info.number_of_found} ', app.logger.INFO)

    else:
        raise Exception('Unhandled condition in handle_success module')

    return status_item


def handle_business_exception_in_queue(bus_exc: Exception, act_item: Item) -> None | StatusItem:
    """ Handling business exception occurred in loop processing item from queue """

    status_item = StatusItem()
    status_item.id = act_item.id
    status_item.status = 'F'
    status_item.comment = str(bus_exc)
    app.logger.log_to_business_and_operational(f'End of processing item with fail with reason: {status_item.comment}', app.logger.WARN)

    sf.quit_driver_if_opened()

    return status_item


def handle_system_exception_in_queue(sys_exc: Exception, act_item: Item) -> None | StatusItem:
    """ Handling system exception occurred in loop processing item from queue """

    if act_item.attempt_number < app.config.max_tries:
        act_item.attempt_number += 1
        status_item = None
        app.logger.log_to_operational(
            f'Error occurred during processing item. The item will be processed again.'
            f'Reason: {get_exception_info(sys_exc)}')

    else:
        status_item = StatusItem()
        status_item.id = act_item.id
        status_item.status = 'F'
        status_item.comment = f'Too many tries, reason: {sys_exc}'
        app.logger.log_to_business_and_operational(f'End of processing item with fail with: {status_item.comment}', app.logger.WARN)

    sf.quit_driver_if_opened()

    return status_item
