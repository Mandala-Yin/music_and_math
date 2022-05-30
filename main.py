import random
import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLabel, QScrollArea, QFileDialog
from PyQt5.QtWidgets import QTextEdit, QComboBox, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont, QSyntaxHighlighter
from PyQt5.QtCore import QCoreApplication, Qt, QSize, QRegExp
from PyQt5 import QtCore

from process import *
from generator import *


class MyMainWindow(QWidget):

    def __init__(self):

        super().__init__()
        self.Len = 500

        self.input_paths = []
        self.output_txt_path = 'out.txt'
        self.output_mid_path = 'out.mid'
        self.mode = 0

        self.data_pitch = []
        self.data_note = []

        self.initUI()

    def initUI(self):

        self.setGeometry(250, 150, 920, 600)
        self.setWindowTitle('Markov Music Generator')
        self.setObjectName("MyMainWindow")
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("pics/3.jpg")))
        self.setPalette(palette)
        # self.setAutoFillBackground(True)

        self.bottons = []

        self.source_bt = QPushButton("  从源文件选择  ", self)
        self.source_bt.clicked.connect(self.choose_source)

        self.clear_bt = QPushButton("清除", self)
        self.clear_bt.clicked.connect(self.clear_source)

        self.quit_bt = QPushButton("退出", self)
        self.quit_bt.clicked.connect(QCoreApplication.quit)

        self.combobox1 = QComboBox(self)
        self.combobox1.addItem("    半耦合    ")
        self.combobox1.addItem("    全耦合    ")
        self.combobox1.addItem("    解耦合    ")
        self.combobox1.currentIndexChanged[int].connect(self.choose_mode)

        self.gen_bt = QPushButton('生成', self)
        self.gen_bt.clicked.connect(self.generate)

        self.save_bt = QPushButton('保存', self)
        self.save_bt.clicked.connect(self.save)
   
        self.text1 = QTextEdit('', self)
        self.text1.selectAll()
        self.text1.setFocus()
        self.text1.setStyleSheet("background-image:url(./pics/7.jpg)")

        self.text2 = QTextEdit('', self)
        self.text2.selectAll()
        self.text2.setFocus()
        self.text2.setStyleSheet("background-image:url(./pics/7.jpg)")

        self.text3 = QTextEdit('', self)
        self.text3.selectAll()
        self.text3.setFocus()
        self.text3.setStyleSheet("background-image:url(./pics/7.jpg)")

        self.vbox1 = QVBoxLayout()

        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.source_bt)
        self.hbox1.addWidget(self.clear_bt)
        self.hbox1.addStretch(1)  
        self.hbox1.addWidget(self.combobox1)
        self.hbox1.addWidget(self.gen_bt)
        
        self.hbox2 = QHBoxLayout()

        self.vbox_child = QVBoxLayout()
        self.vbox_child.addWidget(self.text1)
        self.vbox_child.addWidget(self.text2)

        self.hbox2.addLayout(self.vbox_child)
        self.hbox2.addWidget(self.text3)

        self.hbox3 = QHBoxLayout()
        self.hbox3.addStretch(1)  
        self.hbox3.addWidget(self.save_bt)
        self.hbox3.addWidget(self.quit_bt)

        self.vbox1.addLayout(self.hbox1)
        self.vbox1.addLayout(self.hbox2)
        self.vbox1.addLayout(self.hbox3)

        self.setLayout(self.vbox1)

        self.show()

    def choose_mode(self, mode):
        self.mode = mode
        print(self.mode)

    def choose_source(self):
        file_name = QFileDialog.getOpenFileName(
            self, "Open File", "./src/", "Txt (*.txt)")

        if file_name[0]:
            self.input_paths.append(file_name[0])
            with open(file_name[0], "r") as rf:
                self.data_pitch += rf.readline().split()
                self.data_note += rf.readline().split()

                self.text1.setText(' '.join(self.data_pitch))
                self.text2.setText(' '.join(self.data_note))

    def clear_source(self):
        self.data_pitch = []
        self.data_note = []
        self.text1.setText("")
        self.text2.setText("")

    def generate(self):
        if self.mode == 0:
            self.new_pitch, self.new_note = mode_half_coupled(self.data_pitch, self.data_note, 500)         
        elif self.mode == 1:
            self.new_pitch, self.new_note = mode_full_coupled(self.data_pitch, self.data_note, 500)
        elif self.mode == 2:
            self.new_pitch, self.new_note = mode_uncoupled(self.data_pitch, self.data_note, 500)

        self.text3.setText(' '.join(self.new_pitch) + '\n' + ' '.join(self.new_note))

    def save(self):
        directory = QFileDialog.getSaveFileName(
            self, "Set Saving Path", "./result")

        with open(directory[0] + ".txt", 'w') as wf:
            wf.write(' '.join(self.new_pitch) + '\n')
            wf.write(' '.join(self.new_note) + '\n')

        array_to_midi(directory[0] + '.txt',
                      directory[0] + '.mid', format='name', bpm=80)
        self.text2.setText("Saved.")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_win = MyMainWindow()
    sys.exit(app.exec_())
