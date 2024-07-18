import sys
import threading


class AgentHandler:
    """ Class to handle communication between agent ad bot.
        To correct use:
            - Create instance of AgentHandler in main program of bot
            - Check logic value of method "stop_bot_flag" or attribute "stop_flag" in place where you want
              stop process safely (for example in main loop condition)
            - Use method "send_result" to return process result to agent
    """

    def __init__(self):
        """ Initialization class to communication with agent:
            - stop_flag to ensure safe process close
            - background thread to receive information from agent
            - send info about start bot work
        """
        self.stop_flag: bool = False
        input_thread = threading.Thread(target=self.read_from_agent, daemon=True)
        input_thread.start()
        self.send_start_info()

    def read_from_agent(self):
        """ Background thread to read information from agent:
            - waiting for "STOP" to set stop_flag (to safe close process in correct place)
        """
        while True:
            input_data = sys.stdin.readline().strip()
            if input_data == "STOP":
                self.stop_flag = True

    def stop_bot_flag(self) -> bool:
        """ Method to check stop bot condition """
        return self.stop_flag

    @staticmethod
    def send_result(result: str = ""):
        """ Method to send result of process to agent """
        print(f"RESULT:{result}")

    @staticmethod
    def send_start_info():
        """ Method to send info about start of process to agent"""
        print("BOT STARTED")

