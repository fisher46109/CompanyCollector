# CompanyCollector
## The automation solution searches and collects companies data from CEIDG portal using Graphical User Interface of the application. The companies are searched by input values City and Street provided by the Investigators into the Queue. Collected data is stored into Report directories and shared with the Investigators

### To install and run the application, follow these steps: 
1. **Clone the repository**: Download the source code from GitHub and navigate to the project directory.
2. **Create and activate a virtual environment**: Isolates the project's dependencies to avoid conflicts with other projects.
3. **Install the required packages**: Use `pip` to install all dependencies listed in the `requirements.txt` file.
``` sh
pip install -r requirements.txt
```
4. **Add a Machine to the main_config.json file specifying environment data.** Add it to ```host_to_environment``` in format for:
```json
"<MACHINENAME>" : "DEV_{username}"
```
where username is automatically matched from the environment
5. **Create a configuration file for a specific username named in the format:**
```json
"DEV_{username}"
```
where username must be specified for a specific user.

### Input data
The bot uses a remote queue as its input. Each line in the queue contains one item to be processed by the bot. The Queue Item has attributes:
ID - unique number of the item,
Investigator - username of the investigator that assigned the item to the queue,
City - First input value to be used in a search for companies,
Street - Second input value to be used in a search for the companies,
Status - Result of the process filled in by the bot. Three statuses allowed:
“S” - for success
“P” - for partial success
“F” - for fail
In case of Partial Success and Fail, reason should be filled into the Comment column.

The path to the folder where the database should be placed is specified in the configuration file under the name:
```json
"input_folder_path"
```
and its name:
```json
"sql_input_queue_name"
```

### Output data and reports
Result files of the process are stored in a shared directory as a new Report Folder named: <Investigator_username>_<date>_<time>, 
The Report Folder contains:
1.	CompaniesReport.csv - Data for each company. Columns: Firm Name, First Name, Last Name, NIP, REGON, Address, Status, Start Date, End Date
2.	HistoryReport_All.csv - History of all companies in one file. Columns: Date, Operation type, Application number, Application author, Change date
3.	HistoryReport_<Company NIP>.csv - separate file for each company. Columns: Date, Operation type, Application number, Application author, Change date
4.	PrintedReport_<Company NIP>.pdf - separate PDF file for each company

The folder with output files, business logs, and operational logs are specified by the variables:
```json
  "output_folder_path"
  "business_logs_folder_path"
  "operational_logs_folder_path"
```

### Other configurations

The program can run once or repeatedly, with a specified time interval between each run:
```json
  "one_time_program"
  "idle_time"
```

In case of system exceptions, the item is processed a number of times specified in:
```json
  "max_tries" 
```

Due to the possibility of the website blocking file downloads, downloading the report in PDF format can be disabled, and if enabled, the maximum waiting time for file download can be set.
```json
  "pdf_download_flag"
  "waiting_for_download_file"
```
 
Logs can be disabled by:
```json
  "logs_on"
```

### The flowchart of the program is located in the file: [CompanyCollector.drawio](CompanyCollector.drawio)

Which one should be downloaded and opened on the page: [https://app.diagrams.net/](https://app.diagrams.net/)
