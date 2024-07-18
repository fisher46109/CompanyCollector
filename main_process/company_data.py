import pandas as pd


class CompanyData:
    """ Class for store information about company for single nip processing"""

    def __init__(self):
        self.firm_name: str = ''
        self.first_name: str = ''
        self.last_name: str = ''
        self.nip: str = ''
        self.regon: str = ''
        self.address: str = ''
        self.status: str = ''
        self.start_date: str = ''
        self.end_date: str = ''
        self.table_of_entry_history = pd.DataFrame()
