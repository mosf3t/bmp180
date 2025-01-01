# ---
# Adapted from: https://github.com/octaprog7/BMP180
# 
# Sensor: BMP180 (GY-68) Air Pressure and Temperature Sensor
# Datasheet: https://cdn.shopify.com/s/files/1/1509/1638/files/GY-68_BMP180_Barometrischer_Sensor_Luftdruck_Modul_fur_Arduino_und_Raspberry_Pi_Datenblatt.pdf?15836792964504220844
# Tested with: Raspberry Pi Pico (H) 2021
# ---

# WARNING: do not connect "+" to 5V or the sensor will be damaged!
from machine import I2C, Pin
import bmp180.sensor_base as sensor_base
import time
from sensor_base.bus_service import I2cAdapter

def pa_mmhg(value: float) -> float:
    """Convert air pressure from Pa to mm Hg"""
    return value*7.50062E-3

if __name__ == '__main__':
    # Set scl and sda pins for your board, otherwise nothing will work!
    # https://docs.micropython.org/en/latest/library/machine.I2C.html#machine-i2c    # bus =  I2C(scl=Pin(4), sda=Pin(5), freq=100000)   # на esp8266    !
    # Warning!!!
    # Replace id=1 with id=0 if you are using the first I2C port !!!
    bus = I2C(1, scl=Pin(3, Pin.IN, Pin.PULL_UP), sda=Pin(2, Pin.IN, Pin.PULL_UP), freq=400000)  # for Raspberry Pi Pico (H)
    adaptor = I2cAdapter(bus)
    
    # ps - pressure sensor
    ps = sensor_base.Bmp180(adaptor)

    # if you have EIO exceptions, then check all connections.
    res = ps.get_id()
    print(f"chip_id: {hex(res)}")

    print("Calibration data from registers:")
    print([ps.get_calibration_data(i) for i in range(11)])

    print(20 * "*_")
    print("Reading temperature in a cycle.")
    for i in range(333):
        ps.start_measurement(temperature_or_pressure=True)  # switch to temperature
        delay = sensor_base.get_conversion_cycle_time(ps.temp_or_press, ps.oversample)
        time.sleep_ms(delay)    # delay for temperature measurement
        print(f"Temperature from BMP180: {ps.get_temperature()} \xB0 С\tDelay: {delay} [ms]")

    ps.start_measurement(temperature_or_pressure=False)     # switch to pressure
    delay = sensor_base.get_conversion_cycle_time(ps.temp_or_press, ps.oversample)
    time.sleep_ms(delay)  # delay for pressure measurement

    print(20 * "*_")
    print("Reading pressure using an iterator!")
    for index, press in enumerate(ps):
        time.sleep_ms(delay)  # delay for pressure measurement
        ps.start_measurement(temperature_or_pressure=False)
        print(f"Pressure from BMP180: {press} Pa\t{pa_mmhg(press)} mm Hg\tDelay: {delay} [ms]")
