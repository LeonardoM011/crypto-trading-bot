import os
import sys
import getpass
sys.path.insert(1, "../deps/binance")
from binance.client import Client
from binance.exceptions import BinanceRequestException
from binance.exceptions import BinanceAPIException
from binance.exceptions import BinanceWithdrawException

class output:
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    def print_failed(message):
        print('[' + output.bcolors.FAIL + 'FAILED' + output.bcolors.ENDC + '] ' + message)

    def print_info(message):
        print('[' + output.bcolors.WARNING + ' INFO ' + output.bcolors.ENDC + '] ' + message)

    def print_ok(message):
        print('[' + output.bcolors.OKGREEN + '  OK  ' + output.bcolors.ENDC + '] ' + message)

    def print_insert(message):
        return input('[' + output.bcolors.OKCYAN + 'INSERT' + output.bcolors.ENDC + '] ' + message)
    
    def print_insertpass(message):
        return getpass.getpass('[' + output.bcolors.OKCYAN + 'INSERT' + output.bcolors.ENDC + '] ' + message)

# Try except function for binance
def try_except(fn):
    try:
        return fn()
    except BinanceRequestException as e:
        output.print_failed(e.message)
    except BinanceAPIException as e:
        output.print_failed(e.message)
        output.print_failed("Code " + e.status_code)
    except BinanceWithdrawException as e:
        output.print_failed(e.message)
    return None

# Finds index of key that equals value inside of list
def find_index_of(key, value, list):
    return next((i for i, item in enumerate(list) if item[key] == value), None)

# Returns True if successful and False if not
def check_connectivity(client):
    status = try_except(client.get_system_status)
    if not status:
        return None
    return status['status'] == 0

# Returns if api keys are valid
def check_account_status(client):
    status = try_except(client.get_account_api_trading_status)
    if not status:
        return None
    return status['success'] == True and status['status']['isLocked'] == False

# Get key through input (used in get_api_keys())
def _get_key_input(key_name):
    return output.print_insertpass("Enter " + key_name + " (press enter to fetch from env var): ")

# Get key through environment variable (used in get_api_keys())
def _get_key_env(key_name):
    output.print_info("Trying to fetch from env variable ($" + key_name + ")...")
    key = os.environ.get(key_name)
    if not key:
        output.print_failed("Unable to fetch " + key_name + " from environmental variable.")
        return
    output.print_ok(key_name + " successfully fetched from environmental variable.")
    return key

# Returns api_key and api_secret key through input or environment variable if available
def get_api_key(key_name):
    api_key = _get_key_input(key_name)
    if not api_key:
        api_key = _get_key_env(key_name)
        while not api_key:
            api_key = _get_key_input(key_name)
    return api_key
