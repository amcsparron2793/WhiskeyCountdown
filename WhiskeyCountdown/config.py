import yaml
from pathlib import Path
from WhiskeyCountdown import DEFAULT_PROJECT_ROOT


class ConfigLoader:
    """
    Utility class for loading and writing configuration files.

    This class provides methods to load configuration data from YAML files
    and write configuration data to YAML files. It facilitates managing
    application configurations by simplifying file operations and handling
    default paths for configurations.

    :cvar DEFAULT_CONFIG_PATH: The default path to the configuration file, provided
        as a fallback for loading configurations.
    :type DEFAULT_CONFIG_PATH: Path
    """
    DEFAULT_CONFIG_PATH = DEFAULT_PROJECT_ROOT / 'cfg' / "default_config.yaml"

    @classmethod
    def load_config(cls, config_path: Path = None) -> dict:
        with open(config_path or cls.DEFAULT_CONFIG_PATH, "r") as file:
            return yaml.safe_load(file)

    @classmethod
    def write_config(cls, config_path: Path, data: dict):
        with open(config_path, "w") as file:
            yaml.dump(data, file)


class Config:
    """
    Handles configuration data and provides class-level constants for various
    configuration aspects.

    This class is responsible for loading configuration data from a specified
    file path and initializing various constants that can be used throughout
    the application. It consolidates and organizes configuration values such
    as target dates, string constants, and labels.

    :ivar END_YEAR: Year component of the target date configuration.
    :type END_YEAR: int
    :ivar END_MONTH: Month component of the target date configuration.
    :type END_MONTH: int
    :ivar END_DAY: Day component of the target date configuration.
    :type END_DAY: int
    :ivar END_HOUR: Hour component of the target date configuration.
    :type END_HOUR: int
    :ivar EARLY_END_DAY: Days for early arrival configuration.
    :type EARLY_END_DAY: int
    :ivar LEAVE_HOUR: Hour for leave configuration.
    :type LEAVE_HOUR: int
    :ivar TIME_TO_STRING: String constant representing normal arrival.
    :type TIME_TO_STRING: str
    :ivar EARLY_TIME_TO_STRING: String constant representing early arrival.
    :type EARLY_TIME_TO_STRING: str
    :ivar LEAVE_TIME_TO_STRING: String constant representing leave time.
    :type LEAVE_TIME_TO_STRING: str
    :ivar EARLY_LEAVE_TIME_TO_STRING: String constant representing early leave
                                      time.
    :type EARLY_LEAVE_TIME_TO_STRING: str
    :ivar DAYS_LABEL: Label for days used in string formatting.
    :type DAYS_LABEL: str
    :ivar HOURS_LABEL: Label for hours used in string formatting.
    :type HOURS_LABEL: str
    :ivar MINUTES_LABEL: Label for minutes used in string formatting.
    :type MINUTES_LABEL: str
    :ivar SECONDS_LABEL: Label for seconds used in string formatting.
    :type SECONDS_LABEL: str
    """
    @classmethod
    def load_data(cls, config_path: Path = None):
        cls._data = ConfigLoader.load_config(config_path)
        # Target date configuration
        cls.END_YEAR = cls._data["target_date"]["year"]
        cls.END_MONTH = cls._data["target_date"]["month"]
        cls.END_DAY = cls._data["target_date"]["day"]
        cls.END_HOUR = cls._data["target_date"]["hour"]

        # Early arrival configuration
        cls.EARLY_END_DAY = cls._data["early_arrival"]["day"]

        # Leave configuration
        cls.LEAVE_HOUR = cls._data["leave"]["hour"]

        # String constants
        cls.TIME_TO_STRING = cls._data["strings"]["arrival"]
        cls.EARLY_TIME_TO_STRING = cls._data["strings"]["early_arrival"]
        cls.LEAVE_TIME_TO_STRING = cls._data["strings"]["leave"]
        cls.EARLY_LEAVE_TIME_TO_STRING = cls._data["strings"]["early_leave"]

        cls.DAYS_LABEL = cls._data["strings"]["labels"]["days"]
        cls.HOURS_LABEL = cls._data["strings"]["labels"]["hours"]
        cls.MINUTES_LABEL = cls._data["strings"]["labels"]["minutes"]
        cls.SECONDS_LABEL = cls._data["strings"]["labels"]["seconds"]
