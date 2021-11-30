"""Get our settings from os.environ to facilitate running in Docker.
"""
import os
import logging
import json
import functools


def make_meters_map(meters, meter):
    """Add meter to meters by its ID."""
    meters[str(meter["id"])] = meter
    del meter["id"]
    return meters


# Pull in watched meters data
# If not empty, pull out IDs/protocols to watch
# If empty then we're in discovery mode
config_options = open("/data/options.json")
meters_config = json.load(config_options)["meters"]

if meters_config:
    METERS = functools.reduce(make_meters_map, meters_config, {})
    WATCHED_METERS = ",".join(METERS.keys())
    WATCHED_PROTOCOLS = ",".join(set([meter["protocol"] for meter in meters_config]))
else:
    WATCHED_PROTOCOLS = "all"

# Get server, TLS and auth settings
MQTT_HOST = os.environ.get("MQTT_HOST")
MQTT_PORT = int(os.environ.get("MQTT_PORT"))
MQTT_CA_CERT = os.environ.get("MQTT_CA")
MQTT_CERTFILE = os.environ.get("MQTT_CERT")
MQTT_KEYFILE = os.environ.get("MQTT_KEY")
MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_CLIENT_ID = os.environ.get("MQTT_CLIENT_ID")

# Get discovery info
SW_VERSION = os.environ.get("BUILD_VERSION")
HA_DISCOVERY_DISABLED = bool(os.environ.get("HA_DISCOVERY_DISABLED"))
discovery_topic = os.environ.get("HA_DISCOVERY_TOPIC")
HA_DISCOVERY_TOPIC = discovery_topic if bool(discovery_topic) else "homeassistant"

# Set the MQTT base topic
base_topic = os.environ.get("MQTT_BASE_TOPIC")
MQTT_BASE_TOPIC = base_topic if bool(base_topic) else "amr2mqtt"
MQTT_AVAILABILTY_TOPIC = f"{MQTT_BASE_TOPIC}/bridge/state"

# Set up logging
EV_TO_LOG_LEVEL = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
log_level = EV_TO_LOG_LEVEL.get(os.environ.get("LOG_LEVEL"))
logging.basicConfig()
logging.getLogger().setLevel(log_level)

# path to rtlamr
RTLAMR = "/usr/bin/rtlamr"
