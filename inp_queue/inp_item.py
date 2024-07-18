import sqlite3
import os
from app import app
from exceptions.custom_exceptions import SystemException
from main_process.nip_info import NipInfo


class Item:
    """ Class containing actual item data with number of processing attempt  """

    def __init__(self):
        """ Initialization of item with empty values and attempt number = 1 (first attempt) """

        self.id: int = 0
        self.investigator: str = ''
        self.city: str = ''
        self.street: str = ''
        self.status: str = ''
        self.comment: str = ''
        self.attempt_number: int = 1            # number of processing attempt
        self.nip_info: None | NipInfo = None    # info about found and displayed Nips

    def set_item_values_from_database(self, uid: int):
        """ Assignment all values based on Item and actual attempt number  """

        file_path = os.path.join(app.config.input_folder_path, app.config.sql_input_queue_name)
        conn = None
        try:
            conn = sqlite3.connect(file_path)
            c = conn.cursor()
            self.id = uid
            self.investigator = c.execute("SELECT Investigator FROM queue WHERE ID = ? ", (uid,)).fetchone()[0]
            self.city = c.execute("SELECT City FROM queue WHERE ID = ? ", (uid,)).fetchone()[0]
            self.street = c.execute("SELECT Street FROM queue WHERE ID = ? ", (uid,)).fetchone()[0]
            self.status = c.execute("SELECT Status FROM queue WHERE ID = ? ", (uid,)).fetchone()[0]
            self.comment = c.execute("SELECT Comment FROM queue WHERE ID = ? ", (uid,)).fetchone()[0]
            conn.commit()
        except Exception as e:
            raise SystemException(e)
        finally:
            if conn:
                conn.close()
