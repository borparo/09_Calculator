from fbs_runtime.application_context.PySide2 import ApplicationContext
from PySide2.QtWidgets import QMainWindow

import sys

from src.main.python.calculator import Calculator

if __name__ == '__main__':
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    print(appctxt.get_resource())
    stylesheet = appctxt.get_resource('calculator.qss')
    appctxt.app.setStyleSheet(open(stylesheet).read())
    window = Calculator()
    window.setMaximumWidth(250)
    window.show()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
