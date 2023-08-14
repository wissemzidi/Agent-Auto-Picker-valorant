from pyautogui import screenshot, locateOnScreen, size
from PyQt5.QtWidgets import QApplication, QMessageBox
from pynput.mouse import Controller, Button
from os import startfile, path
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
from threading import Thread
from PyQt5.QtCore import Qt
from time import sleep
from sys import exit
import subprocess
import json


def main(mapName):
    """
    Generate a function comment for the given function body in a markdown code block with the correct language syntax.
    Args:
        mapName (str): The name of the map.
    Returns:
        None
    """
    mouse = Controller()

    newPos = None
    fav_champ = mapsDetails[mapName]["preferredAgent"]

    if fav_champ in agents:
        agentsLineOrder = len(agents) // 2
        newPos = (
            basePos[0] + (agents.index(fav_champ) % agentsLineOrder) * squaresXDiff,
            basePos[1] + (agents.index(fav_champ) // agentsLineOrder) * squaresYDiff,
        )

    if newPos != None:
        sleep(0.1)
        mouse.position = newPos
        mouse.click(Button.left, 2)
        sleep(0.1)
        mouse.position = lockBtnPos
        sleep(0.1)
        mouse.click(Button.left, 1)


def initScreenListenerThread():
    """
    Initializes the screen listener thread.

    This function checks the text of the `initialiseBtn` button and performs the
    following actions based on its value:
        - If the text is "Deactivate", the `executed` flag is set to True, the
        text of the `initialiseBtn` button is changed to "Activate", and the
        text of the `status` label is set to "Not Active ❌".
        - If the text is not "Deactivate", the `executed` flag is set to False,
        the text of the `initialiseBtn` button is changed to "Deactivate", and
        the text of the `status` label is set to "Active ✔".

    After performing the necessary actions based on the `initialiseBtn` button,
    this function creates a new thread named `screenListenerThread` and starts
    it. The thread is created with the following parameters:
        - `target` is set to `initialiseScreenListener`, which is the function
        that will be executed by the thread.
        - `daemon` is set to True, which means that the thread will be a daemon
        thread and will terminate when the main program ends.
        - `name` is set to "screenListener", which is the name of the thread.

    Parameters:
        None

    Returns:
        None
    """
    global screenListenerThread, executed
    if str(fen.initialiseBtn.text()).lower() == "deactivate":
        executed = True
        fen.initialiseBtn.setText("Activate")
        fen.status.setText("Not Active ❌")
    else:
        fen.initialiseBtn.setText("Deactivate")
        fen.status.setText("Active ✔")
        executed = False
        screenListenerThread = Thread(
            target=initialiseScreenListener, daemon=True, name="screenListener"
        )
        screenListenerThread.start()


def initialiseScreenListener():
    """
    Initialises the screen listener.
    This function sets the text of the status label to "Active ✔".
    It calculates the width and height of the screen using the size() function.
    It defines the region of the screen to monitor as the top-left one-fifth of the screen.
    The function enters a while loop until the global variable 'executed' is set to True.
    For each map name in the 'mapsNames' list, it checks if the corresponding image file exists.
    If the image file exists, it uses the locateOnScreen() function to search for the image in the defined region with a confidence of 0.7.
    If the image is found, it calls the main() function with the map name as an argument.
    It prints a message indicating that the map is locked to the specific map name.
    It sets the value of 'executed' to True and updates the text of the initialiseBtn and status labels.
    The function then sleeps for 0.05 seconds before continuing to the next iteration of the while loop.
    """
    global executed
    fen.status.setText("Active ✔")

    width, height = size()
    region = (0, 0, width // 5, height // 5)

    while not executed:
        for mapName in mapsNames:
            if path.exists(f"./assets/maps_pics/{mapName}.png"):
                if (
                    locateOnScreen(
                        f"./assets/maps_pics/{mapName}.png",
                        confidence=0.7,
                        region=region,
                    )
                    != None
                ):
                    main(mapName)
                    print(f"map locked to {mapName}")
                    executed = True
                    fen.initialiseBtn.setText("Activate")
                    fen.status.setText("Not Active ❌")
        sleep(0.05)


def changeAgent():
    """
    Changes the agent for a given map in the config file.

    This function takes no parameters.

    Returns:
        None.
    """
    mapName = str(fen.map.currentText()).lower()
    newAgent = str(fen.agent.currentText()).lower()
    if newAgent == "none":
        newAgent = ""
    if path.exists("./config.json"):
        if newAgent in agents or newAgent == "":
            with open("config.json", "r") as f:
                data = json.loads(f.read())
                data["maps"][mapName]["preferredAgent"] = newAgent
            with open("config.json", "w") as f:
                f.write(json.dumps(data))
            fen.msg.setText("✅ Reload required !")
        else:
            fen.msg.setText("agent not valid ❌")
    else:
        fen.msg.setText("config.json not found ❌")


def initFen(fenTitle):
    """
    Initializes the Fen object with the specified Fen title.

    Parameters:
        fenTitle (str): The title to set for the Fen window.

    Returns:
        None
    """
    fen.setWindowTitle(fenTitle)
    fen.setWindowFlags(Qt.FramelessWindowHint)
    fen.setAttribute(Qt.WA_TranslucentBackground)

    # rendering Images
    fen.exitBtn.setIcon(QIcon("./assets/close.png"))
    fen.exitBtn.setText("")
    fen.minimizeBtn.setIcon(QIcon("./assets/minimize.png"))
    fen.minimizeBtn.setText("")
    fen.appIcon.setPixmap(QPixmap("./assets/icon.ico"))
    fen.appIcon.setScaledContents(True)

    # handling events
    fen.setMouseTracking(True)
    fen.appHeader.mouseReleaseEvent = mouseReleaseEvent
    fen.appHeader.mousePressEvent = mousePressEvent
    fen.appHeader.mouseMoveEvent = mouseMoveEvent


def mousePressEvent(event):
    fen._old_pos = event.pos()


def mouseReleaseEvent(event):
    fen._old_pos = None


def mouseMoveEvent(event):
    if not fen._old_pos:
        return
    delta = event.pos() - fen._old_pos
    fen.move(fen.pos() + delta)


def minimize():
    """
    Minimizes the window by calling the showMinimized() method of the `fen` object.
    """
    fen.showMinimized()


############## Main Program ##############


App = QApplication([])
fen = loadUi("./ui/main.ui")

if not path.exists("./config.json"):
    msg = QMessageBox.critical(
        "Alert !", "config file not found ❌ please execute the config.exe script", "OK"
    )
    subprocess.run(["config.py"])
    exit()

# get config data from "config.json"
with open("config.json", "r") as f:
    data = json.loads(f.read())
    agents = data["agents"]
    basePos = tuple(data["basePos"])
    lockBtnPos = tuple(data["lockBtnPos"])
    mapsNames = list(data["maps"].keys())
    mapsDetails = data["maps"]
    squaresXDiff = data["squaresXDiff"]
    squaresYDiff = data["squaresYDiff"]

initFen("Agent Auto Picker")

fen.initialiseBtn.clicked.connect(initScreenListenerThread)
fen.setAgent.clicked.connect(changeAgent)
fen.exitBtn.clicked.connect(exit)
fen.exitBtn.clicked.connect(lambda: exit(0))
fen.minimizeBtn.clicked.connect(minimize)


fen.show()
App.exec()
