import os
from app import app


def create_business_logs_folder():
    """ Creation of business logs folder """

    if not os.path.exists(app.config.workspace_path):   # check if main workspace folder exists
        try:                                            # if not, try to create it
            os.mkdir(app.config.workspace_path)
        except Exception as e:
            raise e

    business_folder_path = os.path.join(app.config.workspace_path, "Business_Logs")

    if not os.path.exists(business_folder_path):   # check if business logs folder exists
        try:                                       # if not, try to create it
            os.mkdir(business_folder_path)
        except Exception as e:
            raise e

    return business_folder_path


def create_operational_logs_folder():
    """ Creation of operational logs folder """

    if not os.path.exists(app.config.workspace_path):   # check if main workspace folder exists
        try:                                            # if not, try to create it
            os.mkdir(app.config.workspace_path)
        except Exception as e:
            raise e

    operational_folder_path = os.path.join(app.config.workspace_path, "Operational_Logs")

    if not os.path.exists(operational_folder_path):   # check if operational logs folder exists
        try:                                          # if not, try to create it
            os.mkdir(operational_folder_path)
        except Exception as e:
            raise e

    return operational_folder_path


def move_temp_business_logs():
    """ Move business logs to destination path """

    source_path = os.path.join(app.config.workspace_path, "Business_Logs")
    destination_path = app.config.business_logs_folder_path

    if not os.path.exists(destination_path):  # check if Business_Logs folder exists
        try:  # if not, try to create it
            os.mkdir(destination_path)
        except Exception as e:
            raise e

    for filename in os.listdir(source_path):
        if filename.endswith(".txt"):
            source_file = os.path.join(source_path, filename)
            destination_file = os.path.join(destination_path, filename)
            with open(source_file, 'r', encoding='utf-8') as src, open(destination_file, 'a', encoding='utf-8') as dst:
                for line in src:
                    dst.write(line)
            os.remove(source_file)


def move_temp_operational_logs():
    """ Move operational logs to destination path """

    source_path = os.path.join(app.config.workspace_path, "Operational_Logs")
    destination_path = app.config.operational_logs_folder_path

    if not os.path.exists(destination_path):  # check if Operational_Logs folder exists
        try:  # if not, try to create it
            os.mkdir(destination_path)
        except Exception as e:
            raise e

    for filename in os.listdir(source_path):
        if filename.endswith(".txt"):
            source_file = os.path.join(source_path, filename)
            destination_file = os.path.join(destination_path, filename)
            with open(source_file, 'r', encoding='utf-8') as src, open(destination_file, 'a', encoding='utf-8') as dst:
                for line in src:
                    dst.write(line)
            os.remove(source_file)
