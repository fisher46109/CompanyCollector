from app import app
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from exceptions.custom_exceptions import SystemException


def init_required_applications():
    """ Initialization all applications required to process item """

    try:
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": os.path.join(app.config.workspace_path, "selenium_download"),
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        app.ceidg = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        raise SystemException(f'Functions necessary for processing cannot be initialized -> {e}')
