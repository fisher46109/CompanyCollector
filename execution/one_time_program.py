from app import app
from selenium_functions import selenium_function as sf


def one_time_program():
    """ Check if the program is executed once or in a loop - based on one_time_program from config """

    if app.config.one_time_program:
        sf.quit_driver_if_opened()
        return True
