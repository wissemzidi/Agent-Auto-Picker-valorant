from pynput.mouse import Controller, Button
from time import sleep


sleep(2)
mouse = Controller()

mouse.position = (770, 655)
# mouse.position = (435 + 65 + 65, 740 + 65)
# mouse.position = (435 + 65 + 65, 740 + 65)
exit()

i = 1
while True:
    print(f"{i} : ", mouse.position)
    i += 1
    sleep(1)
