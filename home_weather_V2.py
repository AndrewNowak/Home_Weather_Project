import RPi.GPIO as GPIO
import board
import adafruit_bme680
import time
import requests

#set up GPIO pins for anemometer sensor
GPIO.setmode(GPIO.BCM) # Do not use board, this will not work with I2C (???)
GPIO.setup(12,GPIO.IN) # Becuase BCM, this is pin 32 (GPIO 12), not pin 12

#set up so sensor can read 
i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

vane_radius = 0.127 #m
vane_circum = 2*3.14159*vane_radius
efficiency = 1 #adjust through testing

try:
    while True:
        fahr = sensor.temperature*1.8 +32 #C to F
        temp=fahr
        voc = sensor.gas
        humid = sensor.humidity
        pres = sensor.pressure*0.02953 #Convert from hPa to inches
        
        sensor_prev = GPIO.input(12)
        #print('sensor_prev'.format(sensor_prev))
        time_delay = 20
        anemom_read_time = time.time() + time_delay
        cnt= 0
        while time.time() < anemom_read_time:
            sensor_read = GPIO.input(12)
            #print(sensor_read)
            if sensor_read == 1 and sensor_prev == 0:
                cnt = cnt+1
            sensor_prev = sensor_read
            time.sleep(0.001)
        rps = cnt/time_delay
        wind_speed = rps*vane_circum*efficiency*2.23694
        
        #print('Temperature: {} degrees F'.format(fahr))
        #print('Gas: {} ohms'.format(voc))
        #print('Humidity: {} %'.format(humid))
        #print('Pressure: {} in'.format(pres))
        #print('Wind Speed: {} mph'.format(wind_speed))
        
        WUurl = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?"
        WU_station_id = "" #insert station ID
        WU_station_pwd = "" #insert station password
        WU_creds = "ID=" + WU_station_id + "&PASSWORD"+ WU_station_pwd
        date_str = "&dateutc=now"
        action_str = "&action=updateraw"
        
        r = requests.get(
            WUurl +
            WUcreds +
            date_str +
            "&humidity=" + humid +
            "&baromin=" + pres +
            "&windspeedmph=" + wind_speed +
            "&tempf=" + fahr +
            action_str)
        
        time.sleep(580)
finally:
    print('error')
    GPIO.cleanup() 
