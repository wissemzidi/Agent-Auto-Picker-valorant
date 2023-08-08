from pynput.keyboard import Listener as keyboardListener
from pynput.mouse import Controller, Button
from PyQt5.QtWidgets import QApplication
from pyautogui import screenshot
from os import startfile, path
from PyQt5.uic import loadUi
from threading import Thread
from time import sleep
from sys import exit
import json


def keyPress(key):
    if str(key) == "<67>":
        main()
        listener.stop()


def main():
    mouse = Controller()
    if not path.exists("./champ.txt"):
        open("./champ.txt", "w").write("champNameHere")
        startfile("champ.txt")
        exit()

    with open("./champ.txt", "r") as f:
        fav_champ = str(f.readline().strip()).lower()

    lockBtnPos = (950, 800)  # old (770, 655)
    newPos = (0, 0)
    basePos = (540, 925)
    squareXDiff = 85
    squareYDiff = 65

    if fav_champ in allAgents:
        agentsLineOrder = len(allAgents) // 2
        newPos = (
            540 + (allAgents.index(fav_champ) % agentsLineOrder) * squareXDiff,
            925 + (allAgents.index(fav_champ) // agentsLineOrder) * squareYDiff,
        )

    if newPos != (0, 0):
        sleep(0.1)
        mouse.position = newPos
        mouse.click(Button.left, 2)
        sleep(0.1)
        mouse.position = lockBtnPos
        sleep(0.1)
        mouse.click(Button.left, 1)
    else:
        startfile("champ.txt")
    exit()


def initScreenListenerThread():
    global screenListenerThread
    screenListenerThread = Thread(target=initialiseScreenListener, daemon=True).start()


def initialiseScreenListener():
    while True:
        im = screenshot()
        validPixels = 1
        for i in range(pixelsPositions.__len__()):
            pixelColor = im.getpixel(pixelsPositions[i])
            if pixelsColors[i] == pixelColor:
                validPixels += 1
            else:
                break
        if validPixels == 4:
            listener.stop()
            main()
            break
            exit()
        sleep(0.05)


def changeAgent():
    newAgent = fen.agentName.text()
    if newAgent in allAgents and path.exists("./champ.txt"):
        with open("./champ.txt", "w") as f:
            f.write(fen.agentName.text())
    else:
        fen.agentName.setText("agent not valid !")


############## Main Program ##############


App = QApplication([])
fen = loadUi("userInterface.ui")

global allAgents
# get config data from "config.json"
with open("config.json", "r") as f:
    data = json.loads(f.read())
    allAgents = data["agents"]
    agentsPreferredMap = data["preferredAgentMap"]
    mapsPixelsColors = data["mapsPixelsColors"]
    pixelsPositions = list(tuple(pointPos) for pointPos in data["pointsPos"])
    maps = list(agentsPreferredMap.keys())
    print(pixelsPositions)

exit()

if path.exists("./champ.txt"):
    with open("./champ.txt", "r") as f:
        fav_champ = str(f.readline().strip()).lower()
        if len(fav_champ) > 0:
            fen.agentName.setText(fav_champ)

fen.initialiseBtn.clicked.connect(initScreenListenerThread)
fen.selectBtn.clicked.connect(changeAgent)
fen.exitBtn.clicked.connect(exit)


pixelsPositions = [(0, 100), (0, 200), (0, 300), (0, 400)]
pixelsColors = [(55, 168, 227), (68, 174, 226), (89, 178, 227), (106, 177, 222)]

global listener
listener = keyboardListener(on_press=keyPress)
listener.start()


fen.show()
App.exec()
