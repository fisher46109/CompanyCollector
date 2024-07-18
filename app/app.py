# File with declarations global instances
from selenium.webdriver.chrome.webdriver import WebDriver
from config.config import Config
from logger.logger import Logger
from agent_handler.agent_handler import AgentHandler


config: Config | None = None
logger: Logger | None = None
ceidg: WebDriver | None = None
agent: AgentHandler | None = None



