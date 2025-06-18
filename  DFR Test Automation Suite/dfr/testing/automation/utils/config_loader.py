```python
import configparser
import os
from pathlib import Path
# Assuming global_config.py will define BASE_DIR as the repository root.
# If global_config.py is at dfr/testing/automation/config/global_config.py,
# then BASE_DIR = Path(__file__).resolve().parents[4] would be the repo root.
from dfr.testing.automation.config import global_config
from dfr.testing.automation.utils.logger_setup import setup_logger

logger = setup_logger(__name__)

class ConfigLoader:
    """
    Utility class for loading configurations from INI files.
    It supports environment-specific configurations and caches loaded files.
    """
    _config_cache = {}

    @staticmethod
    def load_env_config(env_name: str) -> configparser.ConfigParser:
        """
        Loads configuration from an environment-specific INI file.
        INI files are expected to be in the 'config/' directory at the repository root.
        Caches the loaded config to avoid redundant file reads.

        Args:
            env_name (str): The name of the environment (e.g., 'dev', 'staging').

        Returns:
            configparser.ConfigParser: The loaded configuration object.

        Raises:
            FileNotFoundError: If the configuration file for the environment is not found.
            configparser.Error: If there is an error parsing the configuration file.
        """
        if env_name in ConfigLoader._config_cache:
            logger.debug(f"Using cached config for environment: {env_name}")
            return ConfigLoader._config_cache[env_name]

        config = configparser.ConfigParser()
        # Assumes global_config.BASE_DIR is the repository root
        config_file_path = global_config.BASE_DIR / "config" / f"{env_name}_env_config.ini"

        if not config_file_path.exists():
            logger.error(f"Environment config file not found: {config_file_path}")
            raise FileNotFoundError(f"Environment config file not found: {config_file_path}")

        try:
            config.read(config_file_path)
            logger.info(f"Loaded environment config from: {config_file_path}")
            ConfigLoader._config_cache[env_name] = config
            return config
        except configparser.Error as e:
            logger.error(f"Error loading config file {config_file_path}: {e}")
            raise

    @staticmethod
    def get_env_credential(config: configparser.ConfigParser, section: str, key_ref: str) -> str | None:
        """
        Retrieves a sensitive credential value referenced by a key from environment variables.
        The value in the INI file for `key_ref` is expected to be the name of an environment variable.

        Args:
            config (configparser.ConfigParser): The loaded configuration object.
            section (str): The section in the INI file.
            key_ref (str): The key in the section whose value is the environment variable name.

        Returns:
            str | None: The credential value from the environment variable, or None if not found/set.
        """
        try:
            env_var_name = config.get(section, key_ref)
            credential = os.getenv(env_var_name)
            if not credential:
                logger.warning(f"Credential environment variable '{env_var_name}' for [{section}] '{key_ref}' is not set.")
            return credential
        except (configparser.NoSectionError, configparser.NoOptionError):
            logger.warning(f"Config key reference '{key_ref}' not found in section [{section}].")
            return None
        except Exception as e:
            logger.error(f"Error getting environment credential for [{section}] '{key_ref}': {e}")
            return None

    @staticmethod
    def get_option(config: configparser.ConfigParser, section: str, key: str, fallback=None) -> str | None:
        """
        Helper to get a config option with an optional fallback value.

        Args:
            config (configparser.ConfigParser): The loaded configuration object.
            section (str): The section in the INI file.
            key (str): The key whose value to retrieve.
            fallback (any, optional): The value to return if the key is not found. Defaults to None.

        Returns:
            str | None: The configuration value, or the fallback if not found.

        Raises:
            KeyError: If the key is not found and no fallback is provided.
        """
        try:
            return config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                logger.debug(f"Config key '{key}' not found in section [{section}], using fallback.")
                return fallback
            logger.error(f"Config key '{key}' not found in section [{section}] and no fallback provided.")
            raise KeyError(f"Config key '{key}' not found in section [{section}] and no fallback provided.")

    @staticmethod
    def get_section(config: configparser.ConfigParser, section: str) -> dict:
        """
        Helper to get an entire config section as a dictionary.

        Args:
            config (configparser.ConfigParser): The loaded configuration object.
            section (str): The section in the INI file to retrieve.

        Returns:
            dict: A dictionary representing the section.

        Raises:
            KeyError: If the section is not found.
        """
        if config.has_section(section):
            return dict(config.items(section))
        else:
            logger.error(f"Config section '{section}' not found.")
            raise KeyError(f"Config section '{section}' not found.")

```