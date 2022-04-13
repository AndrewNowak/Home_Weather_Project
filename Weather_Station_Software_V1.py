import RPI.GPIO as GPIO
import board
import adafruit_bme680
import time

#Set up GPIO pins for anemometer sensor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.IN)

#Set up so the sensor can read tp Pi
i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

vane_radius = 5 #cm
vane_circum = 2*3.14159*vane_radius
efficiency = 1 #adjust through testing

try:
    while True:
        #Read values from BME 680
        fahr = sensor.temperature*1.8 + 32 #sensor reads in Celsius, convert to Fahrenheit
        temp = fahr
        voc = sensor.gas
        humid = sensor.humid
        pres = sensor.pressure

        sensor_prev = GPIO.input(12)
        time_delay = 20
        anemom_read_time = time.time() + time_delay # seconds time delay
        cnt = 0 # Number of revolutions over time interval
        while time.time() < anemom_read_time:
            sensor_read = GPIO.input(12)
            if sensor_read == 1 and sensor_prev == 0:
                cnt = cnt + 1
            sensor_prev = sensor_read
            time.sleep(0.001)
        
        rps = cnt/time_delay
        wind_speed =  rps*vane_circum*efficiency*2.23694 #mps -> mph
        

        print('Temperature: {} degrees F'.format(fahr))
        print('Gas: {} ohms'. format(voc))
        print('Humidity: {} %'.format(humid))
        print('Pressure: {} hpa'.format(pres))
        print(' Wind Speed: {} mph'.format(wind_speed))

        time.sleep(580) # wait almost 10 minutes for another reading 
        
    









    
