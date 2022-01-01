import yaml
import pathlib
from jsonschema import validate, ValidationError

CONFIG_SCHEMA = """
  type: object
  properties:
    base_topic: 
      type: string
    broker_host: 
      type: string
    broker_port: 
      type: number
  required:
    - base_topic
    - broker_host
    - broker_port
"""

CONFIG_FILENAME="config.yaml"
APPNAME = "z2mcli"

def _default_config():
    config = {}
    config["base_topic"] = "zigbee2mqtt"
    config["broker_host"] = "localhost"
    config["broker_port"] = 1883
    return config

def _get_config_filepath():
    config_path = [
        pathlib.Path.home().joinpath(".config", APPNAME, CONFIG_FILENAME),
        pathlib.Path("/etc").joinpath(APPNAME, CONFIG_FILENAME)
    ]

    for p in config_path:
        if p.exists() and p.is_file():
            return p

    return None

def _read_and_validate_yaml(file_path):
    f = open(file_path, "r")
    config_yaml = yaml.safe_load(f)
    validate(instance=config_yaml, schema=yaml.load(CONFIG_SCHEMA, Loader=yaml.Loader))
    return config_yaml
            
def read_config():
    file_path = _get_config_filepath()
    if file_path is not None:
        try:
            return _read_and_validate_yaml(file_path)
        except yaml.scanner.ScannerError as e:
            raise yaml.scanner.ScannerError("Config doesn't appear to be valid YAML: " + str(file_path)) from e
        except ValidationError as e:
            raise ValidationError("Config file has errors: " + str(file_path)) from e
    else:
        return _default_config()
