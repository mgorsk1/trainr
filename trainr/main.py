import time

from trainr.fan import HBFan
import os

if __name__ == '__main__':
    fan_device_id = os.getenv('FAN_DEVICE_ID')
    fan_ip = os.getenv('FAN_IP')
    fan_local_key = os.getenv('FAN_LOCAL_KEY')

    fan = HBFan(fan_device_id, fan_ip, fan_local_key)

    fan.turn_on()

    time.sleep(3)
    fan.set_speed(1)

    time.sleep(3)
    fan.set_speed(3)

    time.sleep(5)
    fan.set_speed(2)

    time.sleep(10)

    fan.turn_off()