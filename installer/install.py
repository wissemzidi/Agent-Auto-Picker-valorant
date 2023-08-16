from PyQt5.QtWidgets import QApplication, QFileDialog
from pyuac import runAsAdmin, isUserAdmin
import win32com.shell.shell as shell
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from threading import Thread
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import win32com.client
from sys import exit
import shutil
import sys
import os


def createShortcut(sourcePath, toPath, icon):
    """
    Creates a shortcut from a source file to a specified path with an icon.

    Parameters:
        source (str): The path to the source file.
        toPath (str): The path where the shortcut will be created.
        icon (str): The path to the icon file.

    Returns:
        None
    """
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(toPath)
    shortcut.Targetpath = sourcePath
    shortcut.IconLocation = icon
    shortcut.save()


def copyFolderToPrograms(installDir):
    # try:
    installDir = os.path.join(installDir, "Agent Auto Picker")
    src = os.path.join(os.getcwd(), "Agent Auto Picker")
    # shutil.copytree(src, installDir)

    def copy2_verbose(src, dst):
        fen.files.setText(str(src))
        shutil.copy2(src, dst)

    shutil.copytree(src, installDir, copy_function=copy2_verbose)
    fen.files.setText("")
    return True


# except:
#     return False


def createDesktopShortcut():
    # try:
    username = os.getlogin()
    shortcutPath = f"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Agent Auto Picker test.lnk"
    shutil.copy2(shortcutPath, f"C:\\Users\\{username}\\Desktop")
    return True


# except:
#     return False


def createAppShortcut(installDir):
    try:
        programsShortcutsPath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
        mainExecutablePath = os.path.join(
            installDir, "Agent Auto Picker\Agent Auto Picker.exe"
        )
        curdir = os.getcwd()

        # creating the shortcut and saving it
        path = os.path.join(curdir, "Agent Auto Picker test.lnk")

        createShortcut(
            os.path.join(mainExecutablePath),
            os.path.join(programsShortcutsPath, "Agent Auto Picker test.lnk"),
            os.path.join(curdir, "icon.ico"),
        )
        return True
    except:
        return False


def install(installDir):
    global fen
    if not installDir:
        installDir = os.environ["ProgramFiles"]
    fen.close()
    fen = loadUi("./progress.ui")
    initFen("Installing Agent Auto Picker")

    fen.cancelBtn.clicked.connect(cancel)

    fen.exitBtn.clicked.connect(lambda: exit(0))
    fen.minimizeBtn.clicked.connect(minimize)

    fen.show()
    fen.message.setText("Copying Agent Auto Picker Files")
    if not copyFolderToPrograms(installDir):
        fen.error.setText("Error: Failed to copy Agent Auto Picker")
        return
    fen.progress.setValue(60)

    fen.message.setText("Creating Agent Auto Picker shortcut")
    if not createAppShortcut(installDir):
        fen.error.setText("Error: Failed to create Agent Auto Picker shortcut")
        return

    if not createDesktopShortcut():
        fen.error.setText("Error: Failed to create the desktop shortcut")

    fen.message.setText("Agent Auto Picker installed successfully ✅")
    fen.progress.setValue(100)


def initFen(fenTitle):
    fen.setWindowTitle(fenTitle)
    fen.setWindowFlags(Qt.FramelessWindowHint)
    fen.setAttribute(Qt.WA_TranslucentBackground)

    # rendering Images
    fen.exitBtn.setIcon(QIcon("close.png"))
    fen.exitBtn.setText("")
    fen.minimizeBtn.setIcon(QIcon("minimize.png"))
    fen.minimizeBtn.setText("")
    fen.appIcon.setPixmap(QtGui.QPixmap("icon.ico"))
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


def selectDir():
    directory = QFileDialog.getExistingDirectory(None, "Select Directory")
    if directory:
        fen.dir.setText(str(directory))


def cancel():
    exit(0)


def reset():
    fen.dir.setText(str(os.environ["ProgramFiles"]))
    fen.createShortcut.setChecked(False)
    fen.runConfig.setChecked(False)


def minimize():
    fen.showMinimized()


if __name__ == "__main__":
    # requesting admin privileges
    if not isUserAdmin():
        print("Requires Admin")
        runAsAdmin()
    else:
        App = QApplication(sys.argv)
        App.setWindowIcon(QIcon("icon.ico"))
        fen = loadUi("./installConfig.ui")
        initFen("Install Agent Auto Picker")

        fen.selectDirBtn.clicked.connect(selectDir)
        fen.installBtn.clicked.connect(lambda: install(fen.dir.text()))
        fen.cancelBtn.clicked.connect(cancel)
        fen.resetBtn.clicked.connect(reset)

        fen.exitBtn.clicked.connect(lambda: exit(0))
        fen.minimizeBtn.clicked.connect(minimize)

        # set dynamic text
        fen.dir.setText(str(os.environ["ProgramFiles"]))

        fen.show()
        App.exec()
