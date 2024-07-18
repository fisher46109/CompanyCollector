from app import app
from inp_queue.inp_item import Item
from exceptions.custom_exceptions import BusinessException, SystemException
from selenium_functions import selenium_function as sf
from main_process.nip_info import NipInfo


def find_nips_on_the_website(act_item: Item) -> NipInfo:
    """ Find NIPs on the website from main_url config address
        - Fill and check in dropdown list if city and street values are correct (if not raise BusinessException)
        - If input values are correct search results
        - Read all NIPs and number of found and displayed on the page - store it in nip_info instance and return it.
    """

    # Try to open browser - if cannot, raise SystemException (repeat processing)
    sf.open_browser(app.config.main_url)

    # Try to find element City from act_item in dropdown list - if not present raise BusinessException (do not repeat processing)
    try:
        sf.fill_input_element_with_dropdown_control('//*[@id="MainContentForm_txtCity"]', act_item.city)
    except BusinessException as e:
        raise BusinessException(f'{e} of City ')

    # Try to find element Street from act_item in dropdown list - if not present raise BusinessException (do not repeat processing)
    try:
        sf.fill_input_element_with_dropdown_control('//*[@id="MainContentForm_txtStreet"]', act_item.street)
    except BusinessException as e:
        raise BusinessException(f'{e} of Street ')

    # Try to click search button
    sf.click_element('//*[@id="MainContentForm_btnInputSearch"]')

    nip_info = NipInfo()  # store information of found NIPs

    # check presence of NIP numbers and read it if present
    element_present = sf.check_presence_of_the_element('//dd[contains(@id, "Nip")]')
    if element_present:
        elements_list = sf.find_list_of_elements('//dd[contains(@id, "Nip")]')
        for item in elements_list:
            nip_info.list_of_nips.append(item.text)

    all_found_results_label = sf.check_presence_of_the_element('//*[@id="MainContentForm_lblCount"]',5)
    if all_found_results_label:  # any result found
        nip_info.number_of_found = get_number_of_found(all_found_results_label.text)

    too_many_results_label = sf.check_presence_of_the_element('//*[@id="MainContentForm_lblToManyResults"]', 1)
    if too_many_results_label:  # found more results than displayed
        nip_info.numer_of_displayed = get_number_of_displayed(too_many_results_label.text)
    else:
        nip_info.numer_of_displayed = nip_info.number_of_found

    return nip_info


def get_number_of_found(text: str) -> int:
    """ Try to read and convert label with found to int number """

    try:
        if not text:
            return 0
        number = int(text.split(': ')[1])  # number is after ': '
    except Exception as e:
        raise SystemException(e)
    return number


def get_number_of_displayed(text: str) -> int:
    """ Try to read and convert label with displayed to int number """

    try:
        if not text:
            return 0
        number = int(text.split(' ')[2])  # number is in third word
    except Exception as e:
        raise SystemException(e)
    return number
