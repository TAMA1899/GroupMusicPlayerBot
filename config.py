from os import getenv

from dotenv import load_dotenv

load_dotenv()
que = {}
admins = {}

SESSION_NAME = getenv("SESSION_NAME", "AQCKsKNW6LY70PSUjtYgWS-z0luPGL2TRkv0s3XYSOeIqVWKLOlM5FzCfqch1GfVORIlH-nyFlJ61suiWvNT6GaUdbJ3a95auZv5jomPUj3g0_lJZPk6dRGiBvngRvIB0IyPIJNj2dTlf2g3q2AIMGALQH-no2LqMKxVlGjeIRb-jtXPl7PFpWobcr7-HVbzKvgpfcohUHbQDb1O9-BetvBT_KCYMMGZn43Y-0Mk-pavEMSk7VsdHYCVU0uRc4mjMSQ3TL0wjO7oymiUudW0jr1ERO7QtnLaH8MTzY0gHOatBNUk72ASl7QmclKnFgBxndyLXwborswjCavAIXUoRs9bSW3WRQA")
BOT_TOKEN = getenv("BOT_TOKEN", "1858649461:AAEJu3U-Vnc_vvogVaAiskcN1PUGKQROTDg")

API_ID = int(getenv("API_ID", "3371945"))
API_HASH = getenv("API_HASH", "880695522786b34a4e943902db6e4f64")

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "10"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS", "1652454077").split()))
