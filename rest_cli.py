import requests
from requests.exceptions import ConnectionError

import time
import random
import json

if __name__ == '__main__':

	rest_s_url = 'http://10.0.0.1:8000/'
	sensor_name = 'sensor1'

	# get the new data value, actually generating it randomly
	new_s_value = random.randint(1, 1000)
	new_sensor_t = {'value': str(new_s_value)}

	try:
	    resp = requests.put(rest_s_url+'sensors/'+sensor_name,\
	                        data=json.dumps(new_sensor_t),\
	                        headers={'Content-Type':'application/json'})
	except ConnectionError as e:   
	    print e
	    print "Connection problems with PUT"

	if resp.status_code == 200:
	    print new_sensor_t, "PUT correctly"
	else:
	    # This means something went wrong.
	    print "Bad reply from PUT"

