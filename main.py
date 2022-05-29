import random
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
        self.Len = 500

        self.pitch_markov = Markov(3)  # 这里传矩阵阶数
        self.note_markov = Markov(3)
        self.input_path = ""
        self.output_txt_path = 'out.txt'
        self.output_mid_path = 'out.mid'

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
        self.gen_bt.clicked.connect(self.generate)

        self.save_bt = QPushButton('保存', self)
        self.save_bt.clicked.connect(self.save)

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
        file_name = QFileDialog.getOpenFileName(
            self, "Open File", "./src/", "Txt (*.txt)")
        self.input_path = file_name[0]
        if file_name[0]:
            with open(file_name[0], "r") as rf:
                data = rf.read()
                self.text1.setText(data)

    def generate(self):
        random.seed(520)

        with open(self.input_path, "r") as f:
            data_pitch = f.readline().split()
            self.pitch_markov.pushback(data_pitch)  # 用 pushback 方法喂数据
            data_note = f.readline().split()
            self.note_markov.pushback(data_note)

            self.pitch_markov.getTransferMatrix()  # 喂完数据后用这个方法初始化转移矩阵
            self.note_markov.getTransferMatrix()
            # pitch_markov.showMatrix() # 支持展示转移矩阵

            self.text2.setText("Success!")

            new_pitch = []
            new_note = []

            while(len(new_pitch) < self.Len):  # 暴力拼接，不太妙
                new_pitch += self.pitch_markov.getSequense()
            while(len(new_note) < self.Len):
                new_note += self.note_markov.getSequense()
            self.new_pitch = new_pitch[:self.Len]
            self.new_note = new_note[:self.Len]

    def save(self):
        directory = QFileDialog.getSaveFileName(
            self, "Set Saving Path", "./result")

        with open(directory[0] + ".txt", 'w') as wf:
            wf.write(' '.join(self.new_pitch) + '\n')
            wf.write(' '.join(self.new_note) + '\n')

        array_to_midi(directory[0] + '.txt', directory[0] + '.mid', format='name', bpm=80)
        self.text2.setText("Saved.")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_win = MyMainWindow()
    sys.exit(app.exec_())
