import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication
from PyQt5 import uic
import stock_data
from stock_practice import *



class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setToolTip('주식 데이터 정리 프로그램입니다.')
        self.setWindowTitle('주식 선입 선출법')
        self.setWindowIcon(QIcon('img/unclesam.jpg'))
        self.file_name = None
        self.show()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)


        file_label_name = QLabel('파일명:')

        self.file_edit_name = QLineEdit()
        self.file_edit_name.setToolTip('파일명과 확장자를 같이 적어주세요')
        self.file_edit_name.editingFinished.connect(self.file_Changed)


        btn_quit = QPushButton('종료',self)
        btn_quit.clicked.connect(QCoreApplication.instance().quit)
        btn_start = QPushButton('실행',self)
        btn_quit.setToolTip('작업 중이던 모든 것을 종료합니다.')
        # btn_start.setToolTip('아이디와 비밀번호, 파일명을 정확하게 입력했으며, 자동화를 실행합니다.')
        btn_start.clicked.connect(self.btn_start_clicked)


        grid.addWidget(file_label_name, 2, 0)
        grid.addWidget(btn_quit, 5, 0)


        grid.addWidget(self.file_edit_name, 2, 1)
        grid.addWidget(btn_start, 5, 1)
    

    

    def file_Changed(self):
        self.file_name = self.file_edit_name.text()

    def btn_start_clicked(self):
        work(self.file_name)
        QMessageBox.about(self,"message","변환완료")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
