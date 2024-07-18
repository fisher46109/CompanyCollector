class StatusItem:
    """ Class to store information about status of processing act item """

    def __init__(self):
        self.id: int = 0        # ID of processed item
        self.status: str = ''   # status of processed item
        self.comment: str = ''  # comment of processed item

    def fill_values(self, uid: int, status: str, comment: str):
        """ Fill all attributes inline"""

        self.id = uid
        self.status = status
        self.comment = comment

