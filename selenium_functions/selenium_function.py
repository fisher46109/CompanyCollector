import shutil
from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from exceptions.custom_exceptions import BusinessException, SystemException
from app import app
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep, time
import os


def quit_driver_if_opened():
    """ Quit ceidg driver if it is opened  """

    if app.ceidg:
        app.ceidg.quit()


def open_browser(url: str):
    """ Open browser with specified url address """

    try:
        app.ceidg.get(url)
    except Exception as e:
        raise SystemException(f'The website cannot be opened -> {e}')


def wait_for_element(xpath: str) -> WebElement:
    """ Waiting for the appearance of the element with specified Xpath:
        - wait time from config - waiting_for_elements_in_selenium [s]
        - if time exceeded raise SystemException
        - if appear return this element
    """

    try:
        element = WebDriverWait(app.ceidg, app.config.waiting_for_elements_in_selenium).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except TimeoutException as te:
        raise SystemException(f'Element on the website did not appear -> {te}')


def check_presence_of_the_element(xpath: str, time: int = 1) -> WebElement | None:
    """ Return element from specified path if exist or None if it does not exist """

    try:
        element = WebDriverWait(app.ceidg, time).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except Exception as te:
        return None


def fill_input_element(xpath_str: str, fill_str: str):
    """ Fill input element with specified Xpath (xpath_str) with string value (fill_str) """

    element = wait_for_element(xpath_str)
    element.send_keys(fill_str)


def fill_input_element_with_dropdown_control(xpath_str: str, fill_str: str):
    """ Fill input element with specified Xpath (xpath_str) with string value (fill_str)
        - if dropdown list is not available: raise BusinessException(incorrect city/street)
        - if dropdown list is available: clear input element and fill it with first element from dropdown list
    """

    elements_list = []

    # fill input to get dropdown hints
    clear_and_fill_input_element(xpath_str, fill_str)

    # get hints (as elements) from dropdown
    visible_dropdown_xpath = '//ul[@class="ui-menu ui-widget ui-widget-content ui-autocomplete ui-front" and not(contains(@style, "none"))]'
    elements_in_dropdown_xpath = f'{visible_dropdown_xpath}//div'

    try:
        wait_for_element(visible_dropdown_xpath)
        elements_list = find_list_of_elements(elements_in_dropdown_xpath)
    except Exception as e:
        raise BusinessException('Incorrect data')

    dropdown_list = []
    for item in elements_list:
        dropdown_list.append(item.text)

    if len(dropdown_list) == 1:
        clear_and_fill_input_element(xpath_str, dropdown_list[0])
    elif len(dropdown_list) > 1 and fill_str in dropdown_list:
        clear_and_fill_input_element(xpath_str, fill_str)
    else:
        raise BusinessException('Incorrect data')


def clear_input_element(xpath_str: str, fill_str):
    """ Clear input element with specified Xpath (xpath_str) """

    element = wait_for_element(xpath_str)
    element.clear()


def clear_and_fill_input_element(xpath_str: str, fill_str: str):
    """ Clear input element with specified Xpath (xpath_str) and fill it with string value (fill_str) """

    element = wait_for_element(xpath_str)
    element.clear()
    element.send_keys(fill_str)


def click_element(xpath_str: str):
    """ Click element with specified Xpath (xpath_str) """

    element = wait_for_element(xpath_str)
    element.click()


def find_list_of_elements(xpath_str: str) -> list[WebElement]:
    """ Find elements with specified Xpath (xpath_str) and return as list of elements """

    elements_list: list[WebElement] = []
    elements_list = WebDriverWait(app.ceidg, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, xpath_str))
    )
    return elements_list


def wait_for_all_table_elements(xpath_str: str):
    """ Wait for presence of all table elements - need to reading table correctly"""

    table_elements_xpath = f'{xpath_str}/tbody//tr//td'
    try:
        table_elements = WebDriverWait(app.ceidg, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, table_elements_xpath))
        )
    except TimeoutException as te:
        raise SystemException(f'Table elements on the website did not appear -> {te}')


def get_text_from_element(xpath_str: str) -> str:
    """ Get text from element with specified Xpath (xpath_str) """

    element = wait_for_element(xpath_str)
    if element:
        return element.text
    return ''


def create_table_from_website_data(xpath: str) -> pd.DataFrame:
    """ Create table found in specified xpath and safe it as DataFrame"""

    # Try to find list of headers from table
    headers = []
    headers = find_header_list(xpath)

    # Try to find rows of table data (if next pages available, search them all and append results to list)
    table_data: list[list[str]] = []

    while True:
        table_data = append_data_from_website_to_table(xpath, table_data)
        no_next_button = check_presence_of_the_element('//*[@id="tableHistory_next" and contains(@class, "disabled")]/a')
        if no_next_button:  # if next button inactive break loop
            break
        click_element('//*[@id="tableHistory_next"]/a')  # if next button active go to next page by click next button

    # Creation of df with entry history
    table_from_website = pd.DataFrame(table_data, columns=headers)
    table_from_website.pop(headers[0])  # delete first column

    return table_from_website


def find_header_list(xpath: str) -> list[str]:
    """ Find headers from table and store them as a list """

    head_xpath = f'{xpath}/thead//th'
    header_elements = find_list_of_elements(head_xpath)
    act_row = []
    for element in header_elements:
        act_row.append(element.text.replace('\n', ' '))
    return act_row


def append_data_from_website_to_table(xpath: str, in_table_data: list[list[str]]) -> list[list[str]]:
    """ Find data from table and store them as a list of list """

    wait_for_all_table_elements(xpath)

    body_xpath = f'{xpath}/tbody//tr'
    row_elements = find_list_of_elements(body_xpath)

    temp_table_data: list[list[str]] = []
    for row in row_elements:
        cell_elements = row.find_elements(By.TAG_NAME, 'td')
        act_row: list[str] = []
        for element in cell_elements:
            if '\n' in element.text:
                act_row.append(element.text.replace('\n', ' '))
            else:
                act_row.append(element.text)
        temp_table_data.append(act_row)
    in_table_data += temp_table_data

    return in_table_data


def download_pdf(nip: str, temp_output_folder_path):
    """ Try to download pdf file, rename it to correct name and save in specified output folder """

    download_path = os.path.join(app.config.workspace_path, "selenium_download")

    # Try to create new download folder (if exist delete it first)
    try:
        if os.path.exists(download_path):
            shutil.rmtree(download_path)
        os.makedirs(download_path)
    except Exception as e:
        raise SystemException(e)

    click_element('//*[@id="MainContentForm_btnPrint"]')
    click_element('//*[@id="MainContentForm_linkDownloadG" and @href]')

    pdf_file_name = wait_for_file_in_folder(download_path, app.config.waiting_for_download_file)
    new_file_name = f'PrintedReport_{nip}.pdf'

    old_path = os.path.join(download_path, pdf_file_name)
    if not os.path.exists(temp_output_folder_path):
        try:  # if not, try to create it
            os.mkdir(temp_output_folder_path)
        except Exception as e:
            raise SystemException(e)
    new_path = os.path.join(temp_output_folder_path, new_file_name)
    shutil.move(old_path, new_path)


def wait_for_file_in_folder(download_path: str, time_for_download: int) -> str:
    """ Wait to downloading file is present in download folder """

    start_time = time()
    while time() - start_time < time_for_download:
        files_list = os.listdir(download_path)
        if files_list:
            return files_list[0]    # return path to file
        sleep(1)
    raise SystemException('File download time too long')
