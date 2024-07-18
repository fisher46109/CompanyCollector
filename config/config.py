import json
import os


class Config:
    """ Class containing process configurations based on system variables and configuration JSON files """

    def __init__(self):
        """ Initialization process variables with empty or default values """

        # init configuration variables # # # # # # # # # # # # # # # # # # # # # # # # # #
        self.process_name: str = ''                     # proces name
        self.user_name: str = ''                        # user name
        self.machine_name: str = ''                     # name of machine from which the bot is launched
        self.environment: str = ''                      # name of environment
        # variables read from specific configuration # # # # # # # # # # # # # # # # # # #
        self.bot_name: str = ''                         # bot name
        self.workspace_path: str = ''                   # path of program workspace
        self.input_folder_path: str = ''                # path of input data folder
        self.output_folder_path: str = ''               # path of output data folder
        self.business_logs_folder_path: str = ''        # path of business logs folder
        self.operational_logs_folder_path: str = ''     # path of operational logs folder
        self.input_queue_name: str = ''                 # name of input file
        self.sql_input_queue_name: str = ''             # name of input database file
        self.one_time_program: bool = False             # flag of single proces or working in loop (T/F)
        self.idle_time: int = 0                         # time [s] between checking queue
        self.idle_time_for_initialization: int = 0      # time [s] to next try of initialisation process functions
        self.max_tries: int = 0                         # max number of repeat item tries
        self.logs_on: bool = False                      # flag for enable or disable logs (T/F)
        self.mail_address: str = ''                     # e-mail address to send process information
        self.main_url: str = ''                         # main website url address
        self.waiting_for_elements_in_selenium: int = 0  # max waiting time to presence of element in selenium
        self.waiting_for_download_file: int = 0         # max waiting time to download file
        self.pdf_download_flag: bool = False            # flag for enable or disable download pdf files (T/F)

    @staticmethod
    def replace_keywords(processed_dict: dict, old_string: str, new_string: str):
        """ Static method to convert keywords contained in configuration files """

        for key, value in processed_dict.items():
            if isinstance(value, str):   # check if value is string
                if old_string in value:  # check if string to replace is in the whole sentence
                    processed_dict[key] = value.replace(old_string, new_string)

    def set_attributes_from_dict(self, conf_dict: dict):
        """ Assignment keys from JSON to class attributes (if present in attributes list) """

        for key, value in conf_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def load_config_from_jsons(self):
        """ Read from main config JSON
            Read machine and specific username variables
            Assignment variables from main and specific config files to class attributes
        """

        # Main_config.json is in the same folder as this module file
        main_config_path: str = f"{os.path.dirname(__file__)}\\main_config.json"
        self.user_name = os.environ.get('USERNAME')
        self.machine_name = os.environ.get('COMPUTERNAME')

        # Reading of main configuration file to specify user config file
        with open(main_config_path, 'r', encoding='utf-8') as json_file:
            json_main_dict = json.load(json_file)

        self.process_name = json_main_dict["process_name"]
        raw_environment: str = json_main_dict["host_to_environment"][self.machine_name]  # read raw environment name
        self.environment = raw_environment.replace('{username}', self.user_name)  # match environment name to actual username

        # Specifies json files are in the same folder as this module file
        chosen_json_path = f'{os.path.dirname(__file__)}\\{self.environment}.json'   # set path to specified JSON config

        # Reading of chosen configuration files based on machinename and username
        with open(chosen_json_path, 'r', encoding='utf-8') as json_file:
            json_dict = json.load(json_file)

        self.replace_keywords(json_dict, '{username}', self.user_name)  # replace all {username} occurrence to username read from system

        self.set_attributes_from_dict(json_dict)    # setting instance attributes values from configuration dictionary
