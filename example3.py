import random
import time
import os

import requests
from prometheus_client import start_http_server, Gauge, Info

# weatherlink_url = os.getenv("WEATHERLINK_URL")
weatherlink_url = "http://weatherlink.ksquared.net/v1/current_conditions"

# poll_interval = os.getenv("WEATHERLINK_POLL_INTERVAL")
poll_interval = 3

# Create a Prometheus metrics

did = Info('weatherlink_did', "the Device ID of this sensor")
ts = Gauge('weatherlink_ts', 'Timestamp of last measurement')

# derived from my Davis Vantage Vue
iss_keys = [
    'lsid', 'data_structure_type', 'txid', 'temp', 'hum', 'dew_point', 'wet_bulb',
    'heat_index', 'wind_chill', 'thw_index', 'thsw_index',
    'wind_speed_last', 'wind_dir_last', 'wind_speed_avg_last_1_min', 'wind_dir_scalar_avg_last_1_min',
    'wind_speed_avg_last_2_min', 'wind_dir_scalar_avg_last_2_min', 'wind_speed_hi_last_2_min',
    'wind_dir_at_hi_speed_last_2_min', 'wind_speed_avg_last_10_min', 'wind_dir_scalar_avg_last_10_min',
    'wind_speed_hi_last_10_min', 'wind_dir_at_hi_speed_last_10_min',
    'rain_size', 'rain_rate_last', 'rain_rate_hi', 'rainfall_last_15_min', 'rain_rate_hi_last_15_min',
    'rainfall_last_60_min', 'rainfall_last_24_hr', 'rain_storm', 'rain_storm_start_at', 'solar_rad',
    'uv_index', 'rx_state', 'trans_battery_flag', 'rainfall_daily', 'rainfall_monthly', 'rainfall_year',
    'rain_storm_last', 'rain_storm_last_start_at', 'rain_storm_last_end_at'
]
iss_vars = {}
for k in iss_keys:
    iss_vars[k] = Gauge(f'weatherlink_iss_{k}', f'The value for ISS {k}')

# derived from my Davis WeatherLink 6100
bar_keys = ['lsid', 'data_structure_type', 'bar_sea_level', 'bar_trend', 'bar_absolute']
bar_vars = {}
for k in bar_keys:
    bar_vars[k] = Gauge(f'weatherlink_bar_{k}', f'The value for Barometric Sensor {k}')

# derived from my Davis WeatherLink 6100
inside_keys = ['lsid', 'data_structure_type', 'temp_in', 'hum_in', 'dew_point_in', 'heat_index_in']
inside_vars = {}
for k in inside_keys:
    inside_vars[k] = Gauge(f'weatherlink_inside_{k}', f'The value for Inside Temp/Humidity Sensor {k}')

sensors = {
    '1' : iss_vars,
    '3': bar_vars,
    '4': inside_vars
}

if __name__ == '__main__':
    # Start the Prometheus HTTP server on port 8000
    start_http_server(8000)

    while True:
        r = requests.get(weatherlink_url)
        j = r.json()
        data = j['data']

        did.info({'device': data['did']})
        ts.set(data['ts'])

        for conds in data['conditions']:
            t = conds['data_structure_type']
            try:
                vars = sensors.get(f'{t}')
                for k in vars.keys():
                    if conds[k] is not None:
                        vars[k].set(conds[k])
            except:
                print('Unknown data_structure_type: ', conds['data_structure_type'])

        # Generate a random number
        random_number = generate_random_number()
        print('Random number is: ', random_number)
        # Set the value of the Prometheus metric
        random_number_metric.set(random_number)

        # Sleep for 30 sec
        time.sleep(5)
