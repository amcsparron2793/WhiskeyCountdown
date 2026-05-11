from pathlib import Path

DEFAULT_PROJECT_ROOT = Path(__file__).parent.parent

from WhiskeyCountdown.config import Config
Config.load_data()


from WhiskeyCountdown.custom_errors import InvalidProjectRootError
from WhiskeyCountdown.whiskey_logger import WhiskeyLogger
from WhiskeyCountdown.initializer import _WhiskeyCli, WhiskeyInitializer
from WhiskeyCountdown.time_to_goal import TTCalculations, TTStrings
from WhiskeyCountdown.whiskey_countdown import WhiskeyCountdown, EarlyWhiskeyCountdown
