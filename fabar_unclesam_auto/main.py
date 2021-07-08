import sys
from unclesam_seleniumpart import finish
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication
from PyQt5 import uic
import read_data_and_insert as rdi




class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setToolTip('FBAR을 엉클샘 홈페이지에 자동으로 입력하는 프로그램입니다.')
        self.setWindowTitle('FBAR Automation')
        self.setWindowIcon(QIcon('img/unclesam_icon1.png'))
        self.signal_flag = None
        self.login_id = None
        self.login_pwd = None
        self.file_name = None
        self.show()


    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        login_label_id = QLabel('아이디:')
        login_label_pwd = QLabel('비밀번호:')
        file_label_name = QLabel('파일명:')

        self.login_edit_id = QLineEdit()
        self.login_edit_pwd = QLineEdit()
        self.login_edit_pwd.setEchoMode(QLineEdit.Password)
        self.file_edit_name = QLineEdit()
        self.file_edit_name.setToolTip('확장자 명을 포함한 파일명을 적어주세요')
        self.login_edit_id.editingFinished.connect(self.id_Changed)
        self.login_edit_pwd.editingFinished.connect(self.pwd_Changed)
        self.file_edit_name.editingFinished.connect(self.file_Changed)

        self.rbt1 = QRadioButton('소득신고 대상자(1040) X ')
        self.rbt2 = QRadioButton('소득신고 대상자(1040) O ')
        self.rbt3= QRadioButton('SDOP, SFOP ')
        self.rbt1.pressed.connect(self.rbt1_pressed)
        self.rbt2.pressed.connect(self.rbt2_pressed)
        self.rbt3.pressed.connect(self.rbt3_pressed)

        btn_quit = QPushButton('종료',self)
        btn_quit.clicked.connect(QCoreApplication.instance().quit)
        btn_start = QPushButton('실행',self)
        btn_quit.setToolTip('작업 중이던 모든 것을 종료합니다.')
        btn_start.setToolTip('아이디와 비밀번호, 파일명을 정확하게 입력했으며, 자동화를 실행합니다.')
        btn_start.clicked.connect(self.btn_start_clicked)

        grid.addWidget(login_label_id, 0, 0)
        grid.addWidget(login_label_pwd, 1, 0)
        grid.addWidget(file_label_name, 2, 0)
        grid.addWidget(self.rbt1, 3,0)
        grid.addWidget(self.rbt3, 4,0)
        grid.addWidget(btn_quit, 5, 0)

        grid.addWidget(self.login_edit_id, 0, 1)
        grid.addWidget(self.login_edit_pwd, 1, 1)
        grid.addWidget(self.file_edit_name, 2, 1)
        grid.addWidget(self.rbt2, 3, 1 )
        grid.addWidget(btn_start, 5, 1)
    
    def rbt1_pressed(self):
        self.signal_flag = '996'
    def rbt2_pressed(self):
        self.signal_flag = '997'
    def rbt3_pressed(self):
        self.signal_flag = '998'
    
    def id_Changed(self):
        self.login_id = self.login_edit_id.text()
        print(self.login_id)

    def pwd_Changed(self):
        self.login_pwd = self.login_edit_pwd.text()
        print(self.login_pwd)

    def file_Changed(self):
        self.file_name = self.file_edit_name.text()
        print(self.file_name)


    def btn_start_clicked(self):
        fbr = rdi.data_process(self.login_id, self.login_pwd, self.file_name , self.signal_flag)
        fbr.work()
        QMessageBox.about(self,"message","등록완료")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

    # [210312]엉클샘신고정보워크북_version2021-NEW_SDOP