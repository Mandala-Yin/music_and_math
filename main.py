import sys
import os
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from PyQt5.QtWidgets import QTextEdit, QComboBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5 import QtCore

from process import *
from generator import *

class Child_Widget(QWidget):
    _signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.file = None
        self.maxlen = 0
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 220, 600, 400)
        self.setWindowTitle('fragment')
        self.setObjectName("MyWidget")
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("pics/7.jpg")))

        self.setPalette(palette)
        self.setAutoFillBackground(False)

        self.text = QLabel()
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        self.try_bt = QPushButton('试听', self)
        self.try_bt.clicked.connect(self.play_midi)

        self.save_bt = QPushButton('保存', self)
        self.save_bt.clicked.connect(self.save)

        self.yes_bt = QPushButton('拼接', self)
        self.yes_bt.clicked.connect(self.choose)

        self.quit_bt = QPushButton('放弃', self)
        self.quit_bt.clicked.connect(self.quit_)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.text)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.try_bt)
        hbox1.addWidget(self.save_bt)
        hbox1.addStretch(1)
        hbox1.addWidget(self.yes_bt)
        hbox1.addWidget(self.quit_bt)

        vbox1.addLayout(hbox1)
        self.setLayout(vbox1)

    def save(self):
        directory = QFileDialog.getSaveFileName(
            self, "Set Saving Path", "./result")

        if directory[0] != "":
            with open(directory[0] + "_fragment.txt", 'w') as wf:
                wf.write(' '.join(self.pitch) + '\n')
                wf.write(' '.join(self.note) + '\n')

            array_to_midi(directory[0] + '_fragment.txt',
                          directory[0] + '_fragment.mid', format='name', bpm=80)

    def choose(self):
        self._signal.emit(1)
        self.close()

    def quit_(self):
        self._signal.emit(0)
        self.close()

    def play_midi(self):
        freq = 44100
        bitsize = -16
        channels = 2
        buffer = 1024
        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.set_volume(1)
        clock = pygame.time.Clock()
        try:
            pygame.mixer.music.load(self.file)
        except:
            import traceback
            print(traceback.format_exc())
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(30)


class MyMainWindow(QWidget):

    def __init__(self):

        super().__init__()
        self.child = Child_Widget()

        self.len = 16
        self.rank = None

        self.input_paths = []
        self.mode = 0

        self.data_pitch = []
        self.data_note = []

        self.pitch = []
        self.note = []

        self.length_list = []

        for i in range(3, 8):
            self.length_list.append(str(2**i) + "   ")

        self.rank_list = ['mixed rank', '1', '2', '3', '4', '5']

        self.initUI()

    def initUI(self):

        self.setGeometry(250, 150, 920, 600)
        self.setWindowTitle('Markov Music Generator')
        self.setObjectName("MyMainWindow")
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("pics/3.jpg")))
        self.setPalette(palette)

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

        self.combobox2 = QComboBox(self)
        self.combobox2.addItems(self.length_list)
        self.combobox2.currentIndexChanged[int].connect(self.choose_len)

        self.combobox3 = QComboBox(self)
        self.combobox3.addItems(self.rank_list)
        self.combobox3.currentIndexChanged[int].connect(self.choose_rank)

        self.gen_bt = QPushButton('生成片段', self)
        self.gen_bt.clicked.connect(self.generate)

        self.restart_bt = QPushButton("重新开始", self)
        self.restart_bt.clicked.connect(self.restart)

        self.save_bt = QPushButton('保存', self)
        self.save_bt.clicked.connect(self.save)

        self.title1 = QLabel()
        self.title1.setAlignment(Qt.AlignCenter)
        self.title1.setText("音高")

        self.text1 = QTextEdit('', self)
        self.text1.selectAll()
        self.text1.setFocus()
        self.text1.setStyleSheet("background-image:url(./pics/7.jpg)")

        self.title2 = QLabel()
        self.title2.setAlignment(Qt.AlignCenter)
        self.title2.setText("时值")

        self.text2 = QTextEdit('', self)
        self.text2.selectAll()
        self.text2.setFocus()
        self.text2.setStyleSheet("background-image:url(./pics/7.jpg)")


        self.vbox1 = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.source_bt)
        self.hbox1.addWidget(self.clear_bt)
        self.hbox1.addStretch(1)
        self.hbox1.addWidget(self.combobox1)
        self.hbox1.addWidget(self.combobox2)
        self.hbox1.addWidget(self.combobox3)
        self.hbox1.addWidget(self.gen_bt)

        self.hbox2 = QHBoxLayout()

        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.title1)
        self.vbox2.addWidget(self.text1)

        self.vbox3 = QVBoxLayout()
        self.vbox3.addWidget(self.title2)
        self.vbox3.addWidget(self.text2)

        self.hbox2.addLayout(self.vbox2)
        self.hbox2.addLayout(self.vbox3)

        self.hbox3 = QHBoxLayout()
        self.hbox3.addStretch(1)
        self.hbox3.addWidget(self.restart_bt)
        self.hbox3.addWidget(self.save_bt)
        self.hbox3.addWidget(self.quit_bt)

        self.vbox1.addLayout(self.hbox1)
        self.vbox1.addLayout(self.hbox2)
        self.vbox1.addLayout(self.hbox3)

        self.setLayout(self.vbox1)
        self.child._signal.connect(self.update)

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

    def choose_len(self, i):
        self.len = int(self.length_list[i].rstrip())

    def choose_rank(self, i):
        if i == 0:
            self.rank = None
        else:
            self.rank = int(self.rank_list[i])

    def clear_source(self):
        self.data_pitch = []
        self.data_note = []
        self.text1.setText("")
        self.text2.setText("")

    def generate(self):
        if self.mode == 0:
            self.new_pitch, self.new_note = mode_half_coupled(
                self.data_pitch, self.data_note, self.len, self.rank)
        elif self.mode == 1:
            self.new_pitch, self.new_note = mode_full_coupled(
                self.data_pitch, self.data_note, self.len, self.rank)
        elif self.mode == 2:
            self.new_pitch, self.new_note = mode_uncoupled(
                self.data_pitch, self.data_note, self.len, self.rank)

        self.child.text.setText(
            ' '.join(self.new_pitch) + '\n\n\n' + ' '.join(self.new_note))

        with open("out.txt", 'w') as wf:
            wf.write(' '.join(self.new_pitch) + '\n')
            wf.write(' '.join(self.new_note) + '\n')

        array_to_midi('out.txt', 'out.mid', format='name', bpm=80)
        self.child.file = "out.mid"
        self.child.show()
    
    def restart(self):
        self.pitch = []
        self.note = []

    def update(self, save_it):
        if save_it != 0:
            self.pitch += self.new_pitch
            self.note += self.new_note
        os.remove('out.txt')
        os.remove('out.mid')

    def save(self):
        directory = QFileDialog.getSaveFileName(
            self, "Set Saving Path", "./result")

        if directory[0] != "":
            with open(directory[0] + ".txt", 'w') as wf:
                wf.write(' '.join(self.pitch) + '\n')
                wf.write(' '.join(self.note) + '\n')

            array_to_midi(directory[0] + '.txt',
                          directory[0] + '.mid', format='name', bpm=80)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_win = MyMainWindow()
    sys.exit(app.exec_())
