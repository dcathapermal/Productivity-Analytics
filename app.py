from win32gui import GetForegroundWindow
import psutil
import time
import win32process
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QPlainTextEdit
import sys
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
class WorkerThread(QtCore.QObject):
    signalExample = QtCore.pyqtSignal(str, int)

    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            # Long running task ...
            self.signalExample.emit("leet", 1337)
            time.sleep(1)
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        title = "P.A.T.H Finder"
        top = 400
        left = 400
        width = 1100
        height = 500
        #setup the geometry/layout for graph
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.MyUI()
        colors = ['gold','blue']
        explode = (0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, .01)
        labels = ['Productive', 'Unproductive', '2', '3', '4', '5', '6', '7', '8', '9']
        nums = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        fig, ax = plt.subplots()

        def update(num):
            ax.clear()
            str_num = str(num)
            for x in range(2):
                nums[x] += str_num.count(str(x))
            ax.pie(nums, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', startangle=140)
        ani = FuncAnimation(fig, update, frames=range(1000), repeat=False)
        plt.show()

    def MyUI(self):
        textcanvas = TextCanvas(self, width=1.5, height=4)
        canvas1 = Canvas(self, width=5, height=4)
        canvas2 = Canvas2(self, width=4, height=4)
        textcanvas.move(0,0)
        canvas1.move(150,0)
        canvas2.move(650,0)


class Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 4, height = 4, dpi = 100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        #timer worker
        self.worker = WorkerThread()
        self.workerThread = QtCore.QThread()
        self.workerThread.started.connect(self.worker.run)  # Init worker run() at startup (optional)
        self.worker.signalExample.connect(self.signalExample)  # Connect your signals/slots
        self.worker.moveToThread(self.workerThread)  # Move the Worker object to the Thread object
        self.workerThread.start()
        self.process_time={}
        self.timestamp = {}
        self.setParent(parent)

        #code for the signal example was found from https://dev.to/tkkhhaarree/track-windows-app-usage-time-using-python-h9h

    def signalExample(self, text, number):
        current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name().replace(".exe", "")
        self.timestamp[current_app] = int(time.time())
        if current_app not in self.process_time.keys():
            self.process_time[current_app] = 0
        self.process_time[current_app] += 1
        print(self.process_time)
class Canvas2(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.plotBar()

    def plotBar(self):
        data = ((30, 39), (10, 20), (100, 20),
                (500, 300), (50, 1000))

        dim = len(data[0])
        w = 0.6
        dimw = w / dim

        fig, ax = plt.subplots()
        x = np.arange(len(data))
        barlabels = ['Discord', 'Slack', 'Atom', 'Leagueclientux', 'Chrome']
        for i in range(len(data[0])):
            y = [d[i] for d in data]
            b = ax.bar(x + i * dimw, y,
                       dimw,
                       bottom = 0.001)

        ax.set_xticks(x + dimw / 2)
        ax.set_xticklabels(barlabels)

        ax.set_xlabel('Apps')
        ax.set_ylabel('Hours Spent')

        ax.set_title('Graph of Applications and hours spent on them')
class TextCanvas(FigureCanvas):
## Obtain list of applications to track from aal.txt
    def getProductive(self):
        f = open("productive.txt","r")
        text = f.read()
        self.getProductive = text.split("\n")
        f.close()

    ## Obtain list of productive application from prod_app.txt
    def getUnproductive(self):
        f = open("unproductive.txt","r")
        text = f.read()
        self.getUnproductive = text.split("\n")
        f.close()
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        #Text Label
        self.layout = QVBoxLayout()
        # creating label
        self.getProductive()
        self.prodString = "Productive Apps: \n"
        for text in self.getProductive:
            self.prodString += text + "\n"
        self.getUnproductive()
        self.unprodString = "Unproductive Apps: \n"
        for text in self.getUnproductive:
            self.unprodString += text + "\n"

        self.label2 = QLabel(self.prodString, self)
        self.label2.setWordWrap(True)
        self.label3 = QLabel(self.unprodString, self)
        self.label3.setWordWrap(True)

        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.label3)
        self.setLayout(self.layout)
        self.setParent(parent)

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()
