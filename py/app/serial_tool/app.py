from PySide2 import QtGui, QtWidgets, QtCore
import sys


class SerialWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.layout = QtWidgets.QGridLayout(self)
        self.text_edit = QtWidgets.QPlainTextEdit(self)
        self.layout.addWidget(self.text_edit)


class NewConnectWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

# public slots:
#     void login();//点击登录按钮是执行的槽函数
# private:
#     QLabel *userNameLbl;         //"用户名"标签
#     QLabel *pwdLbl;              //"密码"标签
#     QLineEdit *userNameLEd;      //用户名编辑行
#     QLineEdit *pwdLEd;           //密码编辑行
#     QPushButton *loginBtn;       //登录按钮
#     QPushButton *exitBtn;        //退出按钮


class SerialForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowTitle('串口设置')

        self.serial_name_label = QtWidgets.QLabel(parent)
        self.serial_port_label = QtWidgets.QLabel(parent)
        self.serial_baud_label = QtWidgets.QLabel(parent)

        self.serial_name_edit = QtWidgets.QLineEdit(parent)
        self.serial_port_edit = QtWidgets.QLineEdit(parent)
        self.serial_baud_edit = QtWidgets.QLineEdit(parent)

        # 移动到(70,80)位置(Label左上角坐标，相对于父窗体)
        self.serial_name_label.move(70,80)
        self.serial_name_label.setText("用户名:")
        self.serial_name_edit.move(120,80)

        self.serial_port_label.move(70,130)
        self.serial_port_label.setText("端口:")
        self.serial_port_edit.move(120,130)

        self.serial_baud_label.move(70,180)
        self.serial_baud_label.setText("波特率:")
        self.serial_baud_edit.move(120,180)



class MainWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.tabwidget = QtWidgets.QTabWidget(self)

        self.newConnect = QtWidgets.QPushButton(text='新建连接', parent=self.tabwidget)

        self.newConnect.clicked.connect(self.open_serial_form_slot)

        self.tabwidget.addTab(SerialWidget(), u'电影类别')
        self.tabwidget.addTab(SerialForm(), u'书籍类别')

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tabwidget)

        self.setLayout(self.layout)

    @QtCore.Slot()
    def open_serial_form_slot(self):
        print('clicked')



app = QtWidgets.QApplication()

# window.setFixedSize(400, 300)

mainWindow = MainWindow()
mainWindow.show()

sys.exit(app.exec_())
