from app import app
from main_process.find_nips_on_the_website import find_nips_on_the_website
from output_handling.output_handling import create_out_folder, create_empty_report
from inp_queue.inp_item import Item
from main_process.process_single_nip import process_single_nip


def process_item(act_item: Item):
    """ Main processing item taken from the queue """

    # Send log with information about start or retry processing item
    app.logger.log_start_of_processing(act_item)

    # Find on website NIPs info: number of found, number of displayed and list of displayed to process
    act_item.nip_info = find_nips_on_the_website(act_item)

    processed_item_out_folder_path = create_out_folder(act_item)

    if not act_item.nip_info.number_of_found:
        create_empty_report(processed_item_out_folder_path)
    else:
        # Process all NIPs in sequence
        for nip in act_item.nip_info.list_of_nips:
            process_single_nip(nip, processed_item_out_folder_path)
