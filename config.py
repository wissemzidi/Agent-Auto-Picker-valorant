from PyQt5.QtWidgets import QApplication, QWidget
from pyautogui import locateOnScreen, size
from PyQt5.uic import loadUi
from threading import Thread
import json


def launchConfigFile():
    """
    Initializes the configuration thread.

    This function creates a global variable `configThread` and assigns it a `Thread` object. The `Thread` object is initialized with the `initConfig` function as the target, the `daemon` flag set to `True`, and the name set to "configThread". The function then starts the thread by calling the `start` method.

    Parameters:
    None

    Returns:
    None
    """
    def initConfigThread():
        """
        Initializes the configuration thread.

        This function creates a global variable `configThread` and assigns it a `Thread` object. The `Thread` object is initialized with the `initConfig` function as the target, the `daemon` flag set to `True`, and the name set to "configThread". The function then starts the thread by calling the `start` method.

        Parameters:
        None

        Returns:
        None
        """
        global configThread
        configThread = Thread(target=initConfig, daemon=True, name="configThread")
        configThread.start()


    def initConfig():
        """
        Initializes the configuration settings.

        This function sets up the initial configuration by performing the following steps:
        1. Sets the text of the instructions widget to "Go to the select agent screen".
        2. Initializes the `stepExecuted` list to an empty list.
        3. Initializes the `confidence` variable to 0.7.
        4. Enters a while loop that continues until the length of `stepExecuted` is less than 4.
        5. Uses the `locateOnScreen` function to find the `lockBtn` image on the screen with a confidence level of 0.7.
            - If `lockBtn` is found and "lockBtn" is not in `stepExecuted` list, it stores the position of the `lockBtn` in the `data` dictionary and appends "lockBtn" to the `stepExecuted` list.
        6. Uses the `locateOnScreen` function to find the `firstAgent` image on the screen with a confidence level of 0.7.
            - If `firstAgent` is found and "firstAgent" is not in `stepExecuted` list, it stores the position of the `firstAgent` in the `data` dictionary and appends "firstAgent" to the `stepExecuted` list.
            - If `secondAgent` is found and "secondAgent" is not in `stepExecuted` list, it calculates the difference between the x-coordinate of `secondAgent` and the x-coordinate of the `basePos` from the `data` dictionary, and stores it in the `squaresXDiff` key of the `data` dictionary. It then appends "secondAgent" to the `stepExecuted` list.
            - If `thirdAgent` is found and "thirdAgent" is not in `stepExecuted` list, it calculates the difference between the y-coordinate of `thirdAgent` and the y-coordinate of the `basePos` from the `data` dictionary, and stores it in the `squaresYDiff` key of the `data` dictionary. It then appends "thirdAgent" to the `stepExecuted` list.
        7. Sets the active window to `fen`.
        8. Sets the active window of the application to `fen`.
        9. Raises the `fen` widget to the top of the window stack.
        10. Checks if the length of `stepExecuted` is equal to 4.
            - If it is, it opens the file "config.json" in write mode and writes the `data` dictionary as a JSON string to the file. It then sets the text of the instructions widget to "Config Saved ✔".
            - If it is not, it sets the text of the instructions widget to "Config error ❌, try again".
        """
        fen.instructions.setText("Go to the select agent screen")

        stepExecuted = []
        confidence = 0.7

        while len(stepExecuted) < 4:
            lockBtn = locateOnScreen(
                "./assets/agents_pics/lockBtn.png", confidence=confidence
            )
            firstAgent = locateOnScreen(
                "./assets/agents_pics/first.png", confidence=confidence
            )
            secondAgent = locateOnScreen(
                "./assets/agents_pics/second.png", confidence=confidence
            )
            thirdAgent = locateOnScreen(
                "./assets/agents_pics/third.png", confidence=confidence
            )

            if lockBtn != None and "lockBtn" not in stepExecuted:
                data["lockBtnPos"] = [
                    int(lockBtn.left + lockBtn.width // 2),
                    int(lockBtn.top + lockBtn.height // 2),
                ]
                stepExecuted.append("lockBtn")

            if firstAgent != None and "firstAgent" not in stepExecuted:
                data["basePos"] = [
                    int(firstAgent.left + (firstAgent.width // 2)),
                    int(firstAgent.top + (firstAgent.height // 2)),
                ]
                stepExecuted.append("firstAgent")
                if secondAgent != None and "secondAgent" not in stepExecuted:
                    data["squaresXDiff"] = int(
                        (secondAgent.left + secondAgent.width // 2) - data["basePos"][0]
                    )
                    stepExecuted.append("secondAgent")
                if thirdAgent != None and "thirdAgent" not in stepExecuted:
                    data["squaresYDiff"] = int(
                        (thirdAgent.top + thirdAgent.height // 2) - data["basePos"][1]
                    )
                    stepExecuted.append("thirdAgent")

        if len(stepExecuted) == 4:
            with open("config.json", "w") as f:
                f.write(json.dumps(data))
            fen.instructions.setText("Config Saved ✔")
        else:
            fen.instructions.setText("Config error ❌, try again")


    ############## Main Program ##############

    fen = loadUi("./ui/config.ui")

    data = {
        "basePos": [540, 925],
        "lockBtnPos": [950, 800],
        "squaresXDiff": 85,
        "squaresYDiff": 65,
        "maps": {
            "ascent": {
                "preferredAgent": "",
            },
            "bind": {"preferredAgent": ""},
            "breeze": {"preferredAgent": ""},
            "fracture": {"preferredAgent": ""},
            "haven": {"preferredAgent": ""},
            "icebox": {"preferredAgent": ""},
            "pearl": {"preferredAgent": ""},
            "split": {"preferredAgent": ""},
        },
        "agents": [
            "astra",
            "breach",
            "brimstone",
            "chamber",
            "cypher",
            "deadlock",
            "fade",
            "gekko",
            "harbor",
            "jett",
            "kay/o",
            "killjoy",
            "neon",
            "omen",
            "phoenix",
            "raze",
            "reyna",
            "sage",
            "skye",
            "sova",
            "viper",
            "yoru",
        ],
    }


    fen.initialiseBtn.clicked.connect(initConfigThread)


    fen.show()

if __name__ == "__main__" :
    App = QApplication([])
    launchConfigFile()
    App.exec()