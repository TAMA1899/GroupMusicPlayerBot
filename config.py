from os import getenv

from dotenv import load_dotenv

load_dotenv()
que = {}
admins = {}

SESSION_NAME = getenv("SESSION_NAME", "BQCn7FaEWbrboGeMRVV3UnvCG33Qcxrg-XZmow18K1uWw3RM9579y86bM7ynwAGw8eRE5Ae5W78E-ZmH1sUG2U_unacfNzmoNg9-_pvalKylGwVjmonvuI70sjipS4NyqKZT03T3wVttROBn4vF_WYYw8Pr1Dzke_N8XA65aNqikxCaddSYfOkytOZhp-J3aZWcT02iAZnJeuHAOKYlnTv8FeOmH6jLKkr_TkLrNs3Kal-6neCNgfZa8-MzwcW8R_vVAZ2P8KC0Ed48jKBJUP_oScxBDxTTA3Q6_RAHTuWxENMDPP6E5AkQPO8d8kOFVXvr4964d5LBfd10aCJw57GIYO0OarQA")
BOT_TOKEN = getenv("BOT_TOKEN", "1864672623:AAE6cXQhtiWwu6OW2Cls3pffiNTZcCwIIls")

API_ID = int(getenv("API_ID", "3448718"))
API_HASH = getenv("API_HASH", "5e6d19055850eb5b35720a87e798d0b0")

BOT_NAME = getenv("BOT_NAME", "𝐑𝐨𝐛𝐨𝐭𝐌𝐮𝐬𝐢𝐜")

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "15"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS", "994286253").split()))
