import requests
import time

def check_ping(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True, response.elapsed.total_seconds() * 1000  
        else:
            return False, None
    except requests.ConnectionError:
        return False, None

def revive():
    url_to_check = "https://23104118-8fef-4cd3-a95f-1101d1160f5c-00-1xyslrhl57wa8.janeway.replit.dev/" 
    interval_seconds = 30

    while True:
        success, response_time = check_ping(url_to_check)

        if success:
            print(f"Ping successful! Response time: {response_time:.2f} ms")
        else:
            print("Ping failed!")

        time.sleep(interval_seconds)


revive()
