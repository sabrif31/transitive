""" Take a screenshot and copy its text content to the clipboard. """

import argparse
import sys
import cv2
import json
import os
import pyautogui

import pyperclip
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer

from termcolor import colored

import pytesseract
from deep_translator import (GoogleTranslator, DeeplTranslator)

from rich.tree import Tree
from rich import print

# from .logger import log_copied, log_ocr_failure
# from .notifications import notify_copied, notify_ocr_failure
from lib.ocr import ensure_tesseract_installed, get_ocr_result

class Transitive(QtWidgets.QWidget):
    def __init__(self, parent, langs=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self.setWindowTitle("TextShot")
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog
        )
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        self._screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos())

        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(self.getWindow()))
        self.setPalette(palette)

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.start, self.end = QtCore.QPoint(), QtCore.QPoint()
        self.langs = langs

    def setup(self, x, y, width, height):
        path = "lib/config"
        if not os.path.exists(path):
            os.makedirs(path)

        position_settings = {"x": x, "y": y, "width": width, "height": height}

        with open('lib/config/config.json', 'w') as outfile:
            json.dump(position_settings, outfile)

        print(colored('''[SAVED] Coordinate is saved''', "green"))
        os.system('python translator-command.py')

    def getWindow(self):
        return self._screen.grabWindow(0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QtWidgets.QApplication.quit()

        return super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 100))
        painter.drawRect(0, 0, self.width(), self.height())

        if self.start == self.end:
            return super().paintEvent(event)

        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 3))
        painter.setBrush(painter.background())
        painter.drawRect(QtCore.QRect(self.start, self.end))
        return super().paintEvent(event)

    def mousePressEvent(self, event):
        self.start = self.end = event.pos()
        self.update()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        return super().mousePressEvent(event)

    def snipOcr(self):
        self.hide()

        ocr_result = self.ocrOfDrawnRectangle()
        if ocr_result:
            return ocr_result

    def hide(self):
        super().hide()
        QtWidgets.QApplication.processEvents()

    def ocrOfDrawnRectangle(self):
        pos1 = [self.start.x(), self.start.y()]
        pos2 = [self.end.x(), self.end.y()]
        width = pos2[0] - pos1[0]
        height = pos2[1] - pos1[1]

        """
        if width < 0:
            width = pos1[0] - pos2[0]
            height = pos1[1] - pos2[1]


        print(width)
        """

        self.setup(self.start.x(), self.start.y(), width, height)
        
        """
        return get_ocr_result(
            self.getWindow().copy(
                min(self.start.x(), self.end.x()),
                min(self.start.y(), self.end.y()),
                abs(self.start.x() - self.end.x()),
                abs(self.start.y() - self.end.y()),
            ),
            self.langs,
        )
        """

class OneTimeTransitive(Transitive):
    """Take an OCR screenshot once then end execution."""

    def mouseReleaseEvent(self, event):
        if self.start == self.end:
            return super().mouseReleaseEvent(event)

        ocr_result = self.snipOcr()
        if ocr_result:
            pyperclip.copy(ocr_result)
            # log_copied(ocr_result)
            # notify_copied(ocr_result)

        QtWidgets.QApplication.quit()


class IntervalTransitive(Transitive):
    """
    Draw the screenshot rectangle once, then perform OCR there every `interval` ms.
    """

    prevOcrResult = None

    def __init__(self, parent, interval, langs=None, flags=Qt.WindowFlags()):
        super().__init__(parent, langs, flags)
        self.interval = interval

    def mouseReleaseEvent(self, event):
        if self.start == self.end:
            return super().mouseReleaseEvent(event)

        # Take a shot as soon as the rectangle has been drawn
        self.onShotOcrInterval()
        # And then every `self.interval`ms
        self.startShotOcrInterval()

    def startShotOcrInterval(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.onShotOcrInterval)
        self.timer.start(self.interval)

    def onShotOcrInterval(self):
        prev_ocr_result = self.prevOcrResult
        ocr_result = self.snipOcr()

        if not ocr_result:
            print('fail')
            # log_ocr_failure()
            return

        self.prevOcrResult = ocr_result
        if prev_ocr_result == ocr_result:
            return
        else:
            pyperclip.copy(ocr_result)
            # log_copied(ocr_result)

arg_parser = argparse.ArgumentParser(description=__doc__)
arg_parser.add_argument(
    "langs",
    nargs="?",
    default="eng",
    help='languages passed to tesseract, eg. "eng+fra" (default: %(default)s)',
)
arg_parser.add_argument(
    "-i",
    "--interval",
    type=int,
    default=None,
    help="select a screen region then take textshots every INTERVAL milliseconds",
)
arg_parser.add_argument(
    "-fs",
    "--forcesetup",
    type=bool,
    default=False,
    help="Re-coordinate the postion of chat",
)


def take_textshot(langs, interval, force=False):
    ensure_tesseract_installed()
    path_exists = os.path.exists("lib/config/config.json")
    if path_exists: #  and force == False
        os.system('python translator-command.py')
    else:
        QtCore.QCoreApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
        app = QtWidgets.QApplication(sys.argv)

        window = QtWidgets.QMainWindow()
        if interval != None:
            transitive = IntervalTransitive(window, interval, langs)
            transitive.show()
        else:
            transitive = OneTimeTransitive(window, langs)
            transitive.show()

        sys.exit(app.exec_())


def main():
    args = arg_parser.parse_args()
    take_textshot(args.langs, args.interval, args.forcesetup)


if __name__ == "__main__":
    main()