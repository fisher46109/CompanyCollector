import os
from app import app
from execution.status_item import StatusItem
from .inp_item import Item
from exceptions.custom_exceptions import SystemException
import sqlite3


def set_output_values_to_database(status_item: StatusItem):
    """ Actualization row in table based on actual item with specify Status and Comment """

    file_path = os.path.join(app.config.input_folder_path, app.config.sql_input_queue_name)
    conn = None
    try:
        conn = sqlite3.connect(file_path)
        c = conn.cursor()
        c.execute("UPDATE queue SET Status = ?, Comment = ? WHERE ID = ?", (status_item.status, status_item.comment, status_item.id))
        conn.commit()
    except Exception as e:
        raise SystemException(e)
    finally:
        if conn:
            conn.close()


def get_item() -> Item | None:
    """ Searching the queue until empty string in Status """

    selected = None
    file_path = os.path.join(app.config.input_folder_path, app.config.sql_input_queue_name)
    conn = None
    try:
        conn = sqlite3.connect(file_path)
        c = conn.cursor()
        try:
            selected = c.execute("SELECT ID FROM queue WHERE Status = '' ").fetchone()
            conn.commit()
        except Exception as e:
            selected = None
    except Exception as e:
        raise Exception(e)
    finally:
        if conn:
            conn.close()

    if not selected:
        return None
    act_item = Item()
    act_item.set_item_values_from_database(selected[0])
    act_item.attempt_number = 1
    return act_item




