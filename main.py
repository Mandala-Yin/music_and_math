import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLabel, QScrollArea, QFileDialog
from PyQt5.QtWidgets import QTextEdit, QComboBox, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont, QSyntaxHighlighter
from PyQt5.QtCore import QCoreApplication, Qt, QSize, QRegExp
from PyQt5 import QtCore

from process import *
from markov import Markov

class MyMainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        self.setGeometry(250, 150, 920, 600)
        self.setWindowTitle('Markov Music Generator')
        self.setObjectName("MyMainWindow")
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("1.jpeg")))
        self.setPalette(palette)
        # self.setAutoFillBackground(True)

        self.bottons = []

        self.gen_bt = QPushButton('生成', self)
        self.gen_bt.clicked.connect(QCoreApplication.quit)

        self.save_bt = QPushButton('保存', self)
        self.save_bt.clicked.connect(QCoreApplication.quit)

        self.quit_bt = QPushButton('退出', self)
        self.quit_bt.clicked.connect(QCoreApplication.quit)

        self.source_bt = QPushButton('选取源文件', self)
        self.source_bt.clicked.connect(self.choose)

        self.text1 = QTextEdit('', self)
        self.text1.selectAll()
        self.text1.setFocus()
        self.text1.setGeometry(80, 60, 150, 30)
        # self.text1.setStyleSheet("background-image:url(./gui/3.jpg)")

        self.text2 = QTextEdit('', self)
        self.text2.selectAll()
        self.text2.setFocus()
        self.text2.setGeometry(80, 60, 150, 30)
        # self.text1.setStyleSheet("background-image:url(./gui/3.jpg)")

        self.vbox1 = QVBoxLayout()

        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.source_bt)
        self.hbox1.addWidget(self.gen_bt)
        self.hbox1.addStretch(1)
        self.hbox1.addWidget(self.save_bt)
        self.hbox1.addWidget(self.quit_bt)

        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.text1)
        self.hbox2.addWidget(self.text2)

        self.vbox1.addLayout(self.hbox1)
        self.vbox1.addLayout(self.hbox2)

        self.setLayout(self.vbox1)

        self.show()

    def choose(self):
        m = QFileDialog.getExistingDirectory(None,"选取文件夹","")  # 起始路径
        self.text1.setText(m)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_win = MyMainWindow()
    sys.exit(app.exec_())
