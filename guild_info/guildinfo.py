import json
import time
import logging
import requests

# Commented log sections for distribution
#LOGGER_FORMAT = '%(asctime)s %(message)s'
#logging.basicConfig(format=LOGGER_FORMAT, datefmt='[%H:%M:%S]')
log = logging.getLogger()
#log.setLevel(logging.INFO)

start_time = time.time()

def fetch(gid, url, headers, msg):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            if response.status_code == 404:
                msg["body"]["error"] = "Please send a valid endpoint."
            msg["statusCode"] = response.status_code
            log.error("HTTP Status {0}: {1}".format(response.status_code, response.text))
        else:
            msg["body"][gid] = response.json()
    except Exception as e:
        log.error("Error: {0}".format(e))

def run(key_list, ep):
    base_ep = "https://api.guildwars2.com/v2/guild/{0}/{1}"
    tasks = []
    sleep_time = time.time()
    msg = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json' 
        },
        'body': {}
    }

    for index, key in enumerate(key_list):
        # Sleep for the rest of the rate limit at 500
        time_left = time.time() - sleep_time
        if index % 500 == 499 and time_left < 60:
            time.sleep( 60 - time_left )
            sleep_time = time.time()
            log.debug("Slept at index {0}".format( index ))

        # Parse the query params
        key = key.split(":")
        gid = key[0]
        try:
            lid = key[1]
        except IndexError:
            lid = None

        endpoint = base_ep.format( gid, ep )
        auth = {
            'content-type': "application/json",
        }
        if lid:
            auth['authorization'] = 'Bearer {0}'.format( lid )
        
        task = fetch(gid, endpoint, auth, msg)
        tasks.append(task)

    return msg

def handler(event, context):
    """
    Make bulk request to guild/{id} EP. Format of params is:
        {
            "ids" : "gid,gid:lid",
            "ep" : ""
        }
    """
    params = event["queryStringParameters"]
    key_list = params["ids"].split( "," )

    runs = run(key_list, params["ep"])
    log.info( "Time to complete: {0}".format( time.time() - start_time ) )
    final = runs
    final["body"] = json.dumps(final["body"])
    return final