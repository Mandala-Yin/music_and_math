import sys
import math
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QMessageBox,QLabel,QScrollArea
from PyQt5.QtWidgets import QTextEdit,QComboBox,QLineEdit,QMainWindow,QHBoxLayout,QVBoxLayout
from PyQt5.QtGui import QPalette,QBrush,QPixmap,QFont,QSyntaxHighlighter
from PyQt5.QtCore import QCoreApplication, Qt, QSize, QRegExp 
from PyQt5 import QtCore
from publish_subscribe import Publisher,Reader

class Add_Widget(QWidget):

    _signal = QtCore.pyqtSignal(list, list)

    def __init__(self, reader):

        super().__init__()
        self.reader = reader
        self.poets = list(self.reader.publisher.poets)
        self.initUI()

    def initUI(self):

        self.setGeometry(570,320,300,200)
        self.setWindowTitle('新增订阅')
        self.setObjectName("MyWidget")
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("2.jpeg")))

        self.setPalette(palette)
        self.setAutoFillBackground(False)

        self.text1 = QTextEdit('请在这里输入作者名字',self)
        self.text1.selectAll()
        self.text1.setFocus()
        self.text1.setGeometry(80,60,150,30)
        self.text1.setStyleSheet("background-image:url(1.jpeg)")


        self.combobox1 = QComboBox(self)
        self.combobox1.addItem("不限")
        self.combobox1.addItems(sorted(list(self.reader.publisher.poets)))
        self.combobox1.currentIndexChanged[str].connect(self.getPoet)

        self.text2 = QTextEdit('请在这里输入用空格隔开的关键词（至多三个）',self)
        self.text2.selectAll()
        self.text2.setFocus()
        self.text2.setGeometry(220,60,150,30)
        self.text2.setStyleSheet("background-image:url(1.jpeg)")

        self.bt1 = QPushButton('确认',self)
        self.bt1.setStyleSheet("QPushButton{background-image: url(1.jpeg)}")
        self.bt1.clicked.connect(self.getInfo)

        self.bt2 = QPushButton('取消',self)
        self.bt2.setStyleSheet("QPushButton{background-image: url(1.jpeg)}")
        self.bt2.clicked.connect(self.close)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.combobox1)
        vbox1.addWidget(self.text2)
        hbox1 = QHBoxLayout()
        hbox1.addStretch(5)
        hbox1.addWidget(self.bt1)
        hbox1.addStretch(10)
        hbox1.addWidget(self.bt2)
        hbox1.addStretch(5)
        vbox1.addLayout(hbox1)

        self.setLayout(vbox1)

    def getPoet(self, poet):
        if poet == "不限":
            self.poets = list(self.reader.publisher.poets)
        else:
            self.poets = [poet]

    def getInfo(self):
        words = self.text2.toPlainText().split()
        self._signal.emit(self.poets, words)

        self.text2.setText("请在这里输入用空格隔开的关键词（至多三个）")
        self.close()



class Error_Widget(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.setGeometry(570,320,300,200)
        self.setWindowTitle('错误')
        self.setObjectName("MyWidget")
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("2.jpeg")))

        self.setPalette(palette)
        self.setAutoFillBackground(False)

        self.error_title = QLabel()
        self.error_title.setAlignment(Qt.AlignCenter)
        self.error_title.setText("Error: 订阅无效")

        self.error_text = QLabel()
        self.error_text.setWordWrap(True)
        self.error_text.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        self.exit_bt = QPushButton('知道了',self)
        self.exit_bt.setStyleSheet("QPushButton{background-image: url(2.jpeg)}")
        self.exit_bt.clicked.connect(self.close)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.error_title)
        vbox1.addWidget(self.error_text)
        hbox1 = QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self.exit_bt)
        hbox1.addStretch(10)
        vbox1.addLayout(hbox1)
        self.setLayout(vbox1)


    def PrintErrorInfo(self, error_case):
        if error_case == 1:
            self.error_text.setText("最多只能输入三个关键词")
        if error_case == 2:
            self.error_text.setText("没有有效结果")
        self.show()



class Show_Widget(QWidget):
    def __init__(self, reader):

        super().__init__()

        self.reader = reader
        self.content_fuzzy = []
        self.content_accu = []
        self.keywords = []
        self.new_keywords = []
        self.state = ""
        self.initUI()

    def initUI(self):

        self.setGeometry(540,220,360,480)
        self.setWindowTitle('订阅内容')
        self.setObjectName("MyWidget")
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("2.jpeg")))

        self.setPalette(palette)
        self.setAutoFillBackground(False)

        self.show_title = QLabel()
        self.show_title.setAlignment(Qt.AlignCenter)
        self.show_title.setText("全部订阅结果")
    
        self.show_text = QTextEdit()
        self.show_text.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.show_text.setStyleSheet("background-image:url(2.jpeg)")

        self.combobox1 = QComboBox(self)
        self.combobox1.addItem("1")
        self.combobox1.currentIndexChanged[str].connect(self.showContent)

        self.accu_bt = QPushButton('精确匹配',self)
        self.accu_bt.setStyleSheet("QPushButton{background-image: url(2.jpeg)}")
        self.accu_bt.clicked.connect(self.change_to_accu)

        self.fuzzy_bt = QPushButton('模糊匹配',self)
        self.fuzzy_bt.setStyleSheet("QPushButton{background-image: url(2.jpeg)}")
        self.fuzzy_bt.clicked.connect(self.change_to_fuzzy)

        self.exit_bt = QPushButton('关闭',self)
        self.exit_bt.setStyleSheet("QPushButton{background-image: url(2.jpeg)}")
        self.exit_bt.clicked.connect(self.close)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.show_title)
        vbox1.addWidget(self.show_text)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.exit_bt)
        hbox1.addStretch(10)
        hbox1.addWidget(self.accu_bt)
        hbox1.addStretch(2)
        hbox1.addWidget(self.fuzzy_bt)
        vbox1.addLayout(hbox1)
        self.setLayout(vbox1)

    def getContent(self, content_fuzzy, content_accu, keywords, new_keywords):
        
        self.content_fuzzy = content_fuzzy
        self.content_accu = content_accu
        self.keywords = keywords                                            # 精确匹配的词语
        self.new_keywords = [w for w in new_keywords if w not in keywords]  # 模糊匹配的词语

        self.state = "accurate"                                             # 最初是精确匹配状态
        self.clear_content()

    def clear_content(self):
        
        content = ""
        if self.state == "accurate":
            self.nPages = math.ceil(len(self.content_accu) / 3)
            for idx in self.content_accu[0:3]:
                poem = self.reader.publisher.poems[idx]
                content += "<p>"
                for line in poem[1:]:
                    content += (line + "<br>")
                content += "</p>"
        else:
            self.nPages = math.ceil(len(self.content_fuzzy) / 3)
            for idx in self.content_fuzzy[0:3]:
                poem = self.reader.publisher.poems[idx]
                content += "<p>"
                for line in poem[1:]:
                    content += (line + "<br>")
                content += "</p>"
            for word in self.new_keywords:
                content = content.replace(word, "<font color = 'yellow'>" + word + "</font>")
        
        pagelist = [str(i) for i in list(range(1, self.nPages + 1))]

        self.combobox1.clear()
        self.combobox1.addItems(pagelist)

        for word in self.keywords:
            content = content.replace(word, "<font color = 'red'>" + word + "</font>")
        self.show_text.setHtml("<center>" + content + "</center>")


    def showContent(self, start_pos):

        if self.state == "accurate":
            content_list = self.content_accu
        else:
            content_list = self.content_fuzzy

        try:
            content = ""
            start_pos = int(start_pos)
            for idx in content_list[3 * (start_pos - 1) : 3 * start_pos]:
                poem = self.reader.publisher.poems[idx]
                content += "<p>"
                for line in poem[1:]:
                    content += (line + "<br>")
                content += "</p>"
            for word in self.keywords:
                content = content.replace(word, "<font color = 'red'>" + word + "</font>")
            if self.state == "fuzzy":
                for word in self.new_keywords:
                    content = content.replace(word, "<font color = 'yellow'>" + word + "</font>")
            self.show_text.setHtml("<center>" + content + "</center>")
        except ValueError:
            pass

    def change_to_accu(self):
        self.state = "accurate"
        self.clear_content()

    def change_to_fuzzy(self):
        self.state = "fuzzy"
        self.clear_content()

class MyMainWindow(QWidget):

    def __init__(self, reader, child1, child2, child3):

        super().__init__()
        self.reader = reader
        self.add_child = child1
        self.error_child = child2
        self.show_child = child3
        self.nSubscribes = 0            # 现在的订阅数
        self.content_fuzzy_list = []    # 每次订阅内容的模糊匹配
        self.content_accu_list = []     # 每次订阅内容的精确匹配
        self.keywords_list = []         # 每次选取的关键词
        self.new_keywords_list = []     # 每次模糊匹配选取的近义词

        self.initUI()
    
    def initUI(self):

        self.setGeometry(540,220,360,480)
        self.setWindowTitle('诗歌订阅')
        self.setObjectName("MyMainWindow")
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("1.jpeg")))
        self.setPalette(palette)
        self.setAutoFillBackground(False)

        self.bottons = []
        
        self.exit_bt = QPushButton('退出',self)
        self.exit_bt.setStyleSheet("QPushButton{background-image: url(2.jpeg)}")
        self.exit_bt.clicked.connect(QCoreApplication.quit)

        self.add_bt = QPushButton('新增订阅',self)
        self.add_bt.setStyleSheet("QPushButton{background-image: url(2.jpeg)}")
        self.add_bt.clicked.connect(self.add_subscribe)

        self.vbox1 = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.exit_bt)
        self.hbox1.addStretch(1)
        self.hbox1.addWidget(self.add_bt)
        self.hbox1.addStretch(10)

        self.hbox2 = QHBoxLayout()
        self.hbox2.addStretch(3)
        self.vbox2 = QVBoxLayout()
        self.hbox2.addLayout(self.vbox2)
        self.hbox2.addStretch(3)

        self.vbox1.addLayout(self.hbox1)
        self.vbox1.addLayout(self.hbox2)
        self.vbox1.addStretch(1)
        self.setLayout(self.vbox1)

        self.add_child._signal.connect(self.get_addInfo)

        self.show()

    def add_subscribe(self):
        self.add_child.show()
    
    # 获得 add_child 传回来的信息，两个参数都是 list 形式
    def get_addInfo(self, poets, keywords):

        if len(keywords) > 3:
            self.error_child.PrintErrorInfo(1)
            return
        else:
            self.keywords_list.append(keywords)
            return_lst = self.reader.getContent(poets, keywords, 3)
            if len(return_lst) == 2:
                new_keywords = return_lst[0][1]
                content_fuzzy = return_lst[0][0]
                content_accu = return_lst[1]
            else: 
                new_keywords = []
                content_fuzzy = return_lst[0]
                content_accu = return_lst[0]
            if len(content_fuzzy) == 0:
                self.error_child.PrintErrorInfo(2)
            else:
                self.content_fuzzy_list.append(content_fuzzy)
                self.content_accu_list.append(content_accu)
                self.new_keywords_list.append(new_keywords)
                info = " "
                if len(poets) == 1:
                    info = info + poets[0] + " | "
                for w in keywords:
                    info = info + w + " "
                info = info + " "
                new_bt = QPushButton(info, self)
                new_bt.setStyleSheet("QPushButton{background-image: url(2.jpeg)}")
                tmp = self.nSubscribes
                new_bt.clicked.connect(lambda: self.show_subscribe(tmp))
                self.bottons.append(new_bt)
                self.nSubscribes += 1
                self.vbox2.addWidget(new_bt)
                self.vbox2.addStretch(1)
                QApplication.processEvents()
                
    def show_subscribe(self, idx):
        self.show_child.getContent(self.content_fuzzy_list[idx], self.content_accu_list[idx],
                                self.keywords_list[idx], self.new_keywords_list[idx])
        self.show_child.show()

if __name__=='__main__':
    app = QApplication(sys.argv)

    publisher = Publisher("publisher")
    reader = Reader("reader")
    reader.connectPublisher(publisher)

    child1 = Add_Widget(reader)
    child2 = Error_Widget()
    child3 = Show_Widget(reader)
    main_win = MyMainWindow(reader, child1, child2, child3)
    sys.exit(app.exec_())