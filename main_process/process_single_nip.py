from app import app
from selenium_functions import selenium_function as sf
from exceptions.custom_exceptions import SystemException
from main_process.company_data import CompanyData
from output_handling.output_handling import generate_all_reports


def process_single_nip(nip: str, processed_item_out_folder_path: str):
    """ Process single NIP from all found NIP list """

    sf.open_browser(app.config.main_url)

    sf.clear_and_fill_input_element('//*[@id="MainContentForm_txtNip"]', nip)
    # Try to click search button
    sf.click_element('//*[@id="MainContentForm_btnInputSearch"]')

    found_results_label = sf.check_presence_of_the_element('//*[@id="MainContentForm_lblCount"]', app.config.waiting_for_elements_in_selenium)
    if not found_results_label:  # no result found for nip from list
        raise SystemException('Incompatibility: NIP from NIP list cannot be found in system')

    # Try to click details button
    sf.click_element('//*[@id="MainContentForm_DataListEntities_hrefDetails_0"]')

    company_data = CompanyData()

    company_data.firm_name = sf.get_text_from_element('//*[@id="MainContentForm_lblName"]')
    company_data.first_name = sf.get_text_from_element('//*[@id="MainContentForm_lblFirstName"]')
    company_data.last_name = sf.get_text_from_element('//*[@id="MainContentForm_lblLastName"]')
    company_data.nip = sf.get_text_from_element('//*[@id="MainContentForm_lblNip"]')
    company_data.regon = sf.get_text_from_element('//*[@id="MainContentForm_lblRegon"]')
    company_data.address = sf.get_text_from_element('//*[@id="MainContentForm_lblPlaceOfBusinessAddress"]')
    company_data.status = sf.get_text_from_element('//*[@id="MainContentForm_lblStatus"]')
    company_data.start_date = sf.get_text_from_element('//*[@id="MainContentForm_lblDateOfCommencementOfBusiness"]')
    company_data.end_date = sf.get_text_from_element('//*[@id="MainContentForm_lblDateOfCessationOfBusinessActivity"]')

    # Try to click entry history
    sf.click_element('//*[@id="MainContentForm_btnShowHistory"]')

    # Try to find table with entry history data
    company_data.table_of_entry_history = sf.create_table_from_website_data('//*[@id="tableHistory"]')

    # Try to click back button
    sf.click_element('//*[@id="MainContentForm_backButton_bottomButtonYellowArrow"]')

    # Try to download PDF if pdf_download_flag is set
    if app.config.pdf_download_flag:
        sf.download_pdf(company_data.nip, processed_item_out_folder_path)

    generate_all_reports(processed_item_out_folder_path, company_data)






