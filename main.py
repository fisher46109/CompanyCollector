# Only imports from standard library allowed here!
import os
import traceback
import datetime


def main():
    """ Main function is an interface between AA and the processing script. It is called from the AA and returns
    code response to AA using print method.
    This function must remain independent of other modules as much as possible to make sure it will catch any unhandled
    exception and make sure it will log the fatal log properly even if logger module has not been initialised."""
    # init empty output code
    output = ""
    try:
        # import execution modules
        from execution.execution import execute

        # run execution
        # all exceptions must be handled within execution main loop
        # any unhandled exception will be logged into FatalLog file on the desktop.
        execute()

        # always return "Success" to AA, if execution was successful and all exceptions were handled inside execution.
        output = "Success"
    except Exception as e:
        try:
            output = get_exception_info(e)
        except:
            pass
        try:
            log_fatal(output)
        except:
            """DO NOTHING, If this doesn't work - nothing will save us..."""
    finally:
        try:
            print(str(output))
        except:
            pass


# Functions below must stay in this module close to the main function. They are here to limit dependencies to other
# modules to the minimum.

def get_exception_info(exception: Exception):
    """ Returns string representations of exception message with it's traceback."""
    source = ""
    for tb in reversed(traceback.extract_tb(exception.__traceback__)):
        short_filename = tb.filename.split('\\')[-1]
        source = f"{source} @ {short_filename}/{tb.name}#{tb.lineno}"
    return f"[{type(exception).__name__}] {exception}{source}"


def log_fatal(message):
    """ Appends a line with fatal exception into the fatal log file on the desktop. If the file does not exist, it
    will be created."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    host = os.environ["COMPUTERNAME"]
    username = os.environ["USERNAME"]
    log_line = f"timestamp={timestamp} ; " \
               f"host={host} ; " \
               f"username={username} ; " \
               f"level=FATAL ; " \
               f"source=main ; " \
               f"message={message}"

    if os.path.exists(f"C:\\Users\\{username}\\OneDrive - ING\\Desktop"):
        path_fatal_log_file = f"C:\\Users\\{username}\\OneDrive - ING\\Desktop\\FatalLog.txt"
    else:
        path_fatal_log_file = f"C:\\Users\\{username}\\Desktop\\FatalLog.txt"

    with open(path_fatal_log_file, 'a', encoding='utf-8') as f:
        f.write(log_line + '\n')


if __name__ == '__main__':
    main()
