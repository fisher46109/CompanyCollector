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
MACHINENAME" : "DEV_{username}
```
where username is automatically matched from the environment
5. **Create a configuration file for a specific username named in the format:**
```json
"DEV_{username}
```
where username must be specified for a specific user.

### Input data

### Output data and reports
