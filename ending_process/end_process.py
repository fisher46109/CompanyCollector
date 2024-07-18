from app import app
from logger.files_handling import move_temp_business_logs, move_temp_operational_logs
from output_handling.output_handling import move_reports_folder_to_output
from selenium_functions import selenium_function as sf


def end_process(process_status: str):
    """ Functions ending process """

    output_str = ''
    if process_status == 'Success':
        output_str = 'Process ended with Success'
    else:
        output_str = f'Process ended with ERROR: {process_status}'

    # Send ending logs
    app.logger.log_to_business_and_operational(output_str, app.logger.INFO)

    # Move all created files
    move_temp_business_logs()
    move_temp_operational_logs()
    move_reports_folder_to_output()

    # Close Selenium driver if oppened
    sf.quit_driver_if_opened()

    app.agent.send_result(process_status)

