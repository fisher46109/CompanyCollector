import shutil
from inp_queue.inp_item import Item
from app import app
import os
from datetime import datetime
from exceptions.custom_exceptions import SystemException
from main_process.company_data import CompanyData


def create_out_folder(act_item: Item) -> str:
    """ Create folder to store reports for all nips in processed item, if created return path to it, else raise SystemException """

    # Check if main workspace folder exists, if not try to create it
    if not os.path.exists(app.config.workspace_path):
        try:  # if not, try to create it
            os.mkdir(app.config.workspace_path)
        except Exception as e:
            raise SystemException(e)

    output_folder_path = os.path.join(app.config.workspace_path, "Output")

    if not os.path.exists(output_folder_path):  # check if business logs folder exists
        try:  # if not, try to create it
            os.mkdir(output_folder_path)
        except Exception as e:
            raise SystemException(e)

    act_time = datetime.now()
    folder_name_time = act_time.strftime('%Y%m%d_%H%M%S')
    folder_name = f'{act_item.investigator}_{folder_name_time}'
    act_item_folder_path = os.path.join(output_folder_path, folder_name)

    if not os.path.exists(act_item_folder_path):  # check if business logs folder exists
        try:  # if not, try to create it
            os.mkdir(act_item_folder_path)
        except Exception as e:
            raise SystemException(e)

    return act_item_folder_path


def create_empty_report(processed_item_out_folder_path: str):
    """ Create empty report if no NIPs found"""

    file_path = os.path.join(processed_item_out_folder_path, 'CompaniesReport.csv')
    # if file does not exist create it an add headers
    if not os.path.exists(file_path):
        with open(file_path, mode='a', encoding='utf-8') as report:
            report.write('Firm Name;First Name;Last Name;NIP;REGON;Address;Status;Start Date;End Date\n')


def generate_all_reports(processed_item_out_folder_path: str, cd: CompanyData):
    """ Generate all reports in output folder based on company data for specified NIP """

    add_company_data_to_companies_report(processed_item_out_folder_path, cd)
    add_company_history_to_companies_history_report(processed_item_out_folder_path, cd)
    create_history_report(processed_item_out_folder_path, cd)


def add_company_data_to_companies_report(processed_item_out_folder_path: str, cd: CompanyData):
    """ Add to (or create if not exist) companies report for all NIPs in one item """

    file_path = os.path.join(processed_item_out_folder_path, 'CompaniesReport.csv')
    # if file does not exist create it an add headers
    if not os.path.exists(file_path):
        with open(file_path, mode='a', encoding='utf-8') as report:
            report.write('Firm Name;First Name;Last Name;NIP;REGON;Address;Status;Start Date;End Date\n')
    # add next row of data
    with open(file_path, mode='a', encoding='utf-8') as report:
        report.write(f'{cd.firm_name};'
                     f'{cd.first_name};'
                     f'{cd.last_name};'
                     f'{cd.nip};'
                     f'{cd.regon};'
                     f'{cd.address};'
                     f'{cd.status};'
                     f'{cd.start_date};'
                     f'{cd.end_date}\n')


def add_company_history_to_companies_history_report(processed_item_out_folder_path: str, cd: CompanyData):
    """ Add to (or create if not exist) companies history report for all NIPs in one item """

    file_path = os.path.join(processed_item_out_folder_path, 'HistoryReport_All.csv')
    # if file does not exist create it an add headers
    if not os.path.exists(file_path):
        with open(file_path, mode='a', encoding='utf-8') as report:
            report.write('Date;Operation type;Application number;Application author;Change date\n')
    # add next rows of data
    cd.table_of_entry_history.to_csv(file_path, sep=';', header=False, index=False, mode='a', encoding='utf-8')


def create_history_report(processed_item_out_folder_path: str, cd: CompanyData):
    """ Create single company report for one NIP """

    file_name = f'HistoryReport_{cd.nip}.csv'
    file_path = os.path.join(processed_item_out_folder_path, file_name)
    # if file does not exist create it an add headers
    if not os.path.exists(file_path):
        with open(file_path, mode='a', encoding='utf-8') as report:
            report.write('Date;Operation type;Application number;Application author;Change date\n')
    # add next rows of data
    cd.table_of_entry_history.to_csv(file_path, sep=';', header=False, index=False, mode='a', encoding='utf-8')


def move_reports_folder_to_output():
    """ Move all reports folders to output folder (if any exists, replace it to new one) """

    source_path = os.path.join(app.config.workspace_path, "Output")
    destination_path = app.config.output_folder_path

    if not os.path.exists(destination_path):  # check if Output folder exists
        try:  # if not, try to create it
            os.mkdir(destination_path)
        except Exception as e:
            raise e

    for folder in os.listdir(source_path):
        source_folder_path = os.path.join(source_path, folder)
        destination_folder_path = os.path.join(destination_path, folder)

        if os.path.exists(destination_folder_path):
            shutil.rmtree(destination_path)
        shutil.move(source_folder_path, destination_folder_path)


