import bottle
from bottle import request, response, route
from bottle import post, get, put, delete
import json
import time

_names = set()              # the set of sensors names
host_ip_addr = '10.0.0.1'   # to be used with Mininet
sensor_name = 'sensor1'


@post('/sensors')
def creation_handler():
    try:
        # parse input data
        try:
            data = json.loads(request.body.read())
        except:
            raise ValueError

        # extract the sensor name
        try:
            sensor_name = data['name']
        except (TypeError, KeyError):
            raise ValueError

        # check for the existence of the sensor name
        if len( _names ) > 0:
            if [ x for x in _names if x[0] == sensor_name]:
                raise KeyError        

    except ValueError:
        response.status = 400
        return "Bad Request - input data with errors in POST"
    
    except KeyError:
        response.status = 409
        return "Bad Request - sensor name already exist in POST"

    # add element with default value set to 0 and current time    
    new_sensor_t = (sensor_name, 0, time.ctime())
    _names.add( new_sensor_t )

    # return 200 Success
    response.status = 200
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(new_sensor_t)

@get('/sensors')
def listing_handler():
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(list(_names))

@get('/sensors/<sensor_name>')
def listing_with_name_handler(sensor_name):
    response.headers['Content-Type'] = 'application/json'

    try:
        # check for the existence of sensor with name "sensor_name"
        the_sensor = [ x for x in _names if x[0] == sensor_name]
        if the_sensor:
            return json.dumps(the_sensor)
        else:
            raise KeyError

    except KeyError:
        response.status = 409
        return "Bad Request - sensor name does not exist in GET"

@put('/sensors/<sensor_name>')
def update_handler(sensor_name):
    try:
        # parse input data
        try:
            data = json.loads(request.body.read())
            print data
        except:
            raise ValueError

        # extract and validate new value
        try:
            if not data["value"].isdigit():
                raise ValueError
            newdata = int(data["value"])
            print newdata

        except (TypeError, KeyError):
            raise ValueError

        # check for the existence of sensor with name "sensor_name"
        the_sensor = [ x for x in _names if x[0] == sensor_name]
        if not the_sensor:
            raise KeyError        

    except ValueError:
        response.status = 400
        return
    except KeyError:
        response.status = 409
        return "Bad Request - sensor name does not exist in GET"

    # add new name and remove old name    
    _names.remove(the_sensor[0])
    newdata_t = (sensor_name, newdata, time.ctime()) 
    _names.add(newdata_t)

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(newdata_t)

@delete('/sensors/<sensor_name>')
def delete_handler(sensor_name):
    try:
        # check for the existence of sensor with name "sensor_name"
        the_sensor = [ x for x in _names if x[0] == sensor_name]
        if not the_sensor:
            raise KeyError        

    except KeyError:
        response.status = 409
        return "Bad Request - sensor name does not exist in DELETE"

    # Remove name
    _names.remove(the_sensor[0])
    return

if __name__ == '__main__':
# setting up the testing sensor
    newdata_t = (sensor_name, 0, time.ctime()) 
    _names.add(newdata_t)
    
    bottle.run(host = host_ip_addr, port = 8000)
