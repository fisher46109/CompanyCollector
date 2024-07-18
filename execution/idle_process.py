from app import app
from time import sleep
from selenium_functions import selenium_function as sf


def idle_process():
    """ Function to wait if queue is empty.
        - close selenium driver if is opened
        - wait time idle_time [s] from config
    """
    sf.quit_driver_if_opened()
    sleep(app.config.idle_time)
    return True
