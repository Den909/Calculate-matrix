import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QMessageBox, QGridLayout)

class MatrixCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Калькулятор матриц')
        self.setGeometry(100, 100, 500, 300)

        main_layout = QVBoxLayout()

        # Ввод матриц
        self.matrixA_inputs = self.create_matrix_input("Матрица A:")
        self.matrixB_inputs = self.create_matrix_input("Матрица B:")

        main_layout.addLayout(self.matrixA_inputs)
        main_layout.addLayout(self.matrixB_inputs)

        # Выбор операции
        self.operation_combo = QComboBox(self)
        self.operation_combo.addItems(["Сложение", "Вычитание", "Умножение", "Детерминант"])
        main_layout.addWidget(self.operation_combo)

        # Кнопки
        button_layout = QHBoxLayout()
        self.calculate_button = QPushButton('Рассчитать', self)
        self.calculate_button.clicked.connect(self.calculate)
        button_layout.addWidget(self.calculate_button)

        self.clear_button = QPushButton('Очистить', self)
        self.clear_button.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.clear_button)
        main_layout.addLayout(button_layout)

        # Результат
        self.result_label = QLabel('Результат:', self)
        main_layout.addWidget(self.result_label)
        self.result_output = QLabel(self)
        main_layout.addWidget(self.result_output)

        self.setLayout(main_layout)

    def create_matrix_input(self, label_text):
        layout = QVBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)

        grid_layout = QGridLayout()
        self.input_fields = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                input_field = QLineEdit(self)
                grid_layout.addWidget(input_field, i, j)
                self.input_fields[i][j] = input_field
        layout.addLayout(grid_layout)
        return layout

    def get_matrix_from_input(self, input_fields):
        matrix = []
        rows = 0
        cols = 0
        for i in range(3):
            row = []
            for j in range(3):
                value = self.input_fields[i][j].text()
                if value:
                    try:
                        row.append(int(value))
                        cols += 1
                    except ValueError:
                        QMessageBox.warning(self, "Ошибка", "Введите числовые значения.")
                        return None
            if row:
                matrix.append(row)
                rows += 1
                cols = len(row)
            elif any(self.input_fields[i][j].text() for j in range(3)):  # Проверка на пустые ячейки в заполненной строке
                QMessageBox.warning(self, "Ошибка", "Матрица не должна содержать пустые ячейки внутри.")
                return None
        if matrix:
            return np.array(matrix), rows, cols
        else:
            QMessageBox.warning(self, "Ошибка", "Матрица не может быть пустой.")
            return None

    def calculate(self):
        matrixA, rowsA, colsA = self.get_matrix_from_input(self.matrixA_inputs)
        matrixB, rowsB, colsB = self.get_matrix_from_input(self.matrixB_inputs)

        if matrixA is None or matrixB is None:
            return

        operation = self.operation_combo.currentText()

        try:
            if operation == "Сложение":
                if rowsA != rowsB or colsA != colsB:
                    raise ValueError("Для сложения матрицы должны быть одинакового размера.")
                result = matrixA + matrixB
            elif operation == "Вычитание":
                if rowsA != rowsB or colsA != colsB:
                    raise ValueError("Для вычитания матрицы должны быть одинакового размера.")
                result = matrixA - matrixB
            elif operation == "Умножение":
                if colsA != rowsB:
                    raise ValueError("Количество столбцов в первой матрице должно быть равно количеству строк во второй матрице.")
                result = np.dot(matrixA, matrixB)
            elif operation == "Детерминант":
                if rowsA != colsA:
                    raise ValueError("Для вычисления детерминанта матрица должна быть квадратной.")
                result = np.linalg.det(matrixA)
            else:
                raise ValueError("Неверная операция.")

            self.display_result(result)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def display_result(self, result):
        if isinstance(result, np.ndarray):
            result_str = ""
            for row in result:
                row_str = " ".join(str(int(x)) for x in row)
                result_str += row_str + "\n"
            self.result_output.setText(result_str)
        else:
            self.result_output.setText(str(result))

    def clear_inputs(self):
        for row in self.input_fields:
            for input_field in row:
                input_field.clear()
        self.result_output.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = MatrixCalculator()
    calculator.show()
    sys.exit(app.exec_())