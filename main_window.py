import multiprocessing as mp
import sys
import time
import re
import json
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow,
                             QProgressBar, QPushButton)
import functools
from charting import charting
from other import luna, compute_hash


class Window(QMainWindow):
    def __init__(self) -> None:
        """Функция инициализации
        """
        super(Window, self).__init__()
        self.setWindowTitle('Поиск номера банковской карты')
        self.setFixedSize(600, 400)
        self.size = 1
        with open("setting.json") as json_file:
            self.setting = json.load(json_file)
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 600, 400)
        self.background.setPixmap(QPixmap("background.jpg").scaled(600, 400))
        self.background.setStyleSheet("background-color: #B0E0E6;")
        self.info = QLabel(self)
        self.info.setText("Известная часть карты:" +
                          self.setting["bins"][0]+" ****** " + self.setting["last_number"])
        self.info.setGeometry(150, 10, 300, 50)
        self.info1 = QLabel(self)
        self.info2 = QLabel(self)
        self.info2.setText("Выберите кол-во потоков:")
        self.info2.setGeometry(25, 60, 250, 100)
        self.info2.hide()
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.progress.setGeometry(115, 300, 400, 30)
        self.progress.setStyleSheet(
            ' background-color: #FFFFF0 ;border: 2px solid black;')
        self.progress.hide()
        self.button_card = QPushButton('Найти карту', self)
        self.button_card.setGeometry(200, 150, 200, 50)
        self.button_card.setStyleSheet(
            ' border-radius: 15%; background-color: #FFFFF0 ;border: 2px solid black;')
        self.button_card.clicked.connect(self.find_card)
        self.button_card.hide()
        self.result = QLabel(self)
        self.result.setGeometry(150, 250, 400, 200)
        self.pool_size = QtWidgets.QComboBox(self)
        self.pool_size.addItems([str(i) for i in range(1, mp.cpu_count()+1)])
        self.pool_size.setGeometry(200, 90, 200, 50)
        self.pool_size.activated[str].connect(self.choose_pool)
        self.pool_size.hide()
        self.graph = QPushButton('Построить график', self)
        self.graph.setGeometry(200, 215, 200, 50)
        self.graph.clicked.connect(self.show_graph)
        self.graph.setStyleSheet(
            ' border-radius: 15%; background-color: #FFFFF0 ;border: 2px solid black;')
        self.graph.hide()
        self.pool_size.show()
        self.button_card.show()
        self.info2.show()
        self.graph.show()
        self.show()

    def choose_pool(self, text: str):
        """Функция выбора кол-ва ядер
        """
        self.size = int(re.findall('(\d+)', text)[0])

    def find_card(self, start: float) -> None:
        """Функция поиска карты

        Args:
            start (float): время начала поиска
        """
        compute_hash_partial = functools.partial(compute_hash, CONFIG=self.setting)
        self.info.setText("\tИнициализация всех карт")
        start = time.time()
        self.progress.show()
        cards = []
        for i in range(0, 1000000):
            mid = str(i).zfill(6)
            for j in range(len(self.setting["bins"])):
                card = (self.setting["bins"][j] + mid +
                        self.setting["last_number"])
                cards.append(card)
                self.progress.setValue(int((i+1)*50/10**6))
                QApplication.processEvents()

        with mp.Pool(self.size) as p:
            self.progress.setValue(67)
            results = p.map(compute_hash_partial, cards)
        self.info.setText("\t Сверяем хэшы карт")
        for result, card in zip(results, cards):
            self.progress.setValue(85)
            if result:
                self.success(start, card)
                p.terminate()
                QApplication.processEvents()
                break
        else:
            self.info.setText('Карта не найдена')
            self.progress.setValue(0)

    def success(self, start: float, result: int):
        """Функция обновляет прогресс бар и выводит информацию о карте и времени поиска

        Args:
            start (float): время начала поиска
            result (int): времяя конца поиска
        """
        end = time.time() - start
        self.result_card = result
        self.progress.setValue(100)
        result_text = f'Расшифрованный номер: {str(result)[0:4]} {str(result)[4:8]} {str(result)[8:12]} {str(result)[12:]}\n'
        result_text += f'Проверка на алгоритм Луна: {luna(result)}\n'
        result_text += f'Время: {end:.2f} секунд'
        self.result.setText(result_text)
        self.info.setText("\t Карта найдена")

    def show_graph(self):
        """Функция отрисовки графика
        """
        cards = []
        compute_hash_partial = functools.partial(compute_hash, CONFIG=self.setting)
        self.info.setText("Инициализация всех карт")
        for i in range(0, 1000000):
            mid = str(i).zfill(6)
            for j in range(len(self.setting["bins"])):
                card = (self.setting["bins"][j] + mid +
                        self.setting["last_number"])
                cards.append(card)
        values = []
        for cpu in range(1, mp.cpu_count()+1):
            start = time.time()
            self.info.setText(
                f"Подождите идет процес оценки времени с {cpu} core")
            with mp.Pool(cpu)as p:

                results = p.map(compute_hash_partial, cards)
                for result, card in zip(results, cards):
                    if result:
                        end = time.time() - start
                        values.append((cpu, end))
                        p.terminate()
                        break
        charting(values)
        self.info.setText("График готов")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
