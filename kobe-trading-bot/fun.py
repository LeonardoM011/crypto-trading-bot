import os
import sys
sys.path.insert(1, "../deps/binance")
from binance.client import Client

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
    print('[' + bcolors.FAIL + 'FAILED' + bcolors.ENDC + '] ' + message)

def print_info(message):
    print('[' + bcolors.WARNING + ' INFO ' + bcolors.ENDC + '] ' + message)

def print_ok(message):
    print('[' + bcolors.OKGREEN + '  OK  ' + bcolors.ENDC + '] ' + message)

def print_insert(message):
    return print('[' + bcolors.OKCYAN + 'INSERT' + bcolors.ENDC + '] ' + message)

# Print error if var is False and return False
def error(var, msg):
    if var:
        return True
    print("Error:", msg)
    return False

# Try except function for binance
def try_except(success, failure, *exceptions):
    try:
        return success()
    except exceptions or Exception:
        return failure() if callable(failure) else failure    

# Finds index of key that equals value inside of list
def find_index_of(key, value, list):
    return next((i for i, item in enumerate(list) if item[key] == value), None)

# Returns True if successful and False if not
def check_connectivity(client):
    return client.get_system_status()['status'] == 0 and client.get_system_status()['msg'] == 'normal'

# Returns api_key and api_secret key through input or environment variable if available
def get_api_keys():
    api_key = print_insert("Enter BINANCE API KEY (press enter to fetch from env var): ")
    if not api_key:
        print_info("Trying to fetch from env variable ($BINANCE_API_KEY)...")
        api_key = os.environ.get("BINANCE_API_KEY")
        # TODO: Change this
        assert error(api_key, "Unable to fetch API KEY!")
        print_ok("API KEY successfully fetched.")
    
    api_secret = print_insert("Enter BINANCE API SECRET KEY (press enter to fetch from env var): ")
    if not api_secret:
        print_info("Trying to fetch from env variable ($BINANCE_API_SECRET_KEY)...")
        api_secret = os.environ.get("BINANCE_API_SECRET_KEY")
        # TODO: Change this
        if not api_secret:
            print_failed("Unable to fetch API SECRET KEY!")
            return -1
        print_ok("API SECRET KEY successfully fetched.")
    return api_key, api_secret