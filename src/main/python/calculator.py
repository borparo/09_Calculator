# calculator.py
from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QWidget, QApplication, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QMessageBox
from collections import deque


class Calculator(QWidget):
    """
    A simple Qt Calculator for learning purposes. This version stores values and operands in
    separated queues and does the calculations when the operators or equal buttons are pressed,
    displaying the result in the numbers field.
    """
    main_window = QApplication.activeWindow()

    def __init__(self, parent=main_window):
        super(Calculator, self).__init__(parent)
        self.setWindowTitle("QtCalculator")

        self.values = deque()
        self.operands = deque()
        self.add_digit_state = True  # True for typing first digit in the field. False for inserting the following ones.
        self.rounding = 4  # result digits to round for after decimal.
        self.result = 0

        self.characters = ["C", "<-", "%", "/", "7", "8", "9", "*", "4", "5", "6", "-", "1", "2", "3", "+", "0", ".",
                           "="]
        self.buttons = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.result_field = QLineEdit(str(self.result))
        self.result_field.setAlignment(Qt.AlignRight)
        self.result_field.setEnabled(False)
        self.result_field.setObjectName("result_field")
        self.buttons = [QPushButton(button) for button in self.characters]
        self.buttons_page = QWidget()
        for button in self.buttons:
            if button.text() == "C":
                button.setShortcut(QKeySequence(Qt.Key_C))
                button.setFixedSize(65, 65)
                button.setObjectName("clear")
            elif button.text() == "=":
                button.setShortcut("return")
                button.setFixedSize(130, 65)
                button.setObjectName("equal")
            elif button.text() == "<-":
                button.setShortcut("backspace")
                button.setFixedSize(65, 65)
                button.setObjectName("backspace")
            elif button.text() == ".":
                button.setShortcut(button.text())
                button.setFixedSize(65, 65)
                button.setObjectName("decimal")
            else:
                button.setShortcut(button.text())
                button.setFixedSize(65, 65)
                button.setObjectName(button.text())

    def create_layouts(self):
        buttons_grid = QGridLayout(self.buttons_page)
        buttons_grid.setSpacing(1)
        buttons_grid.setContentsMargins(0, 0, 0, 0)
        index = 0
        for row in range(5):
            for col in range(4):
                button = self.buttons[index]
                buttons_grid.addWidget(button, row, col)
                if row == 4 and col == 2:
                    buttons_grid.addWidget(button, row, col, 1, 2)
                    break
                index += 1

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.result_field)
        main_layout.addWidget(self.buttons_page)

    def create_connections(self):
        for button in self.buttons:
            if button.text() == "C":
                button.clicked.connect(self.reset)
            elif button.text() == "/" or button.text() == "*" or button.text() == "-" or button.text() == "+":
                button.clicked.connect(self.operation)
            elif button.text() == "=":
                button.clicked.connect(self.equal)
            elif button.text() == "%":
                button.clicked.connect(self.convert_to_percent)
            elif button.text() == "<-":
                button.clicked.connect(self.correct_character)
            else:
                button.clicked.connect(self.type_value)

    def reset(self):
        """
        Resets calculator to init state.
        """
        self.result = 0
        self.result_field.setText(str(self.result))
        self.add_digit_state = True
        self.values.clear()
        self.operands.clear()

    def convert_to_percent(self):
        """
        Converts to percent of current result_field value.
        """
        current_value = float(self.result_field.text())
        current_value *= 0.01
        self.result_field.setText(str(current_value))
        self.add_digit_state = False

    def operation(self):
        """
        Manages and calculates the expressions for 2 stored values.
        """
        # store values and operands for their use
        current_value = float(self.result_field.text())

        self.values.append(current_value)
        self.operands.append(self.sender().text())

        # with 2 values in queue, apply operand to them and update result accordingly the resulting expression.
        if len(self.values) == 2:
            if self.operands[0] == "+":
                self.result = self.values[0] + self.values[1]
            elif self.operands[0] == "-":
                self.result = self.values[0] - self.values[1]
            elif self.operands[0] == "*":
                self.result = self.values[0] * self.values[1]
            elif self.operands[0] == "/":
                try:
                    self.result = self.values[0] / self.values[1]
                except ZeroDivisionError:
                    QMessageBox.warning(self, 'ZeroDivisionError',
                                        'Division by zero is not allowed.')
            # Update and clear after calculating expression.
            self.values.clear()
            self.values.append(self.result)
            self.operands.popleft()

            if not self.add_digit_state:
                self.result_field.setText(str(round(self.result, self.rounding)))
        self.add_digit_state = True

    def equal(self):
        """
        Complete and display the final result of the operations queues.
        """
        self.operation()
        self.result_field.setText(str(round(self.result, self.rounding)))
        self.add_digit_state = True

    def correct_character(self):
        """
        Deletes the last digit written in the result_field or sets it to 0 if one digit is left, and
        we delete it.
        """
        if len(self.result_field.text()) > 1:
            self.result_field.setText(self.result_field.text()[:-1])
            self.result = float(self.result_field.text())
        else:
            self.result_field.setText("0")
            self.add_digit_state = True

    def type_value(self):
        """
        Assigns to self.result the value written in the result_field.
        """
        start_with_percent  = "0."
        if self.add_digit_state:
            # user can type smaller than 1 values starting with the decimal button.
            if self.sender().text() == '.':
                self.result_field.setText(start_with_percent)
            else:
                self.result_field.setText(self.sender().text())
            self.add_digit_state = False
        else:
            self.result_field.insert(self.sender().text())
        self.result = float(self.result_field.text())
