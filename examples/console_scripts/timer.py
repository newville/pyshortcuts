from time import sleep
from datetime import datetime


while True:
    sleep(0.25)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
