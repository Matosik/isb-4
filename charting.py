
import matplotlib.pyplot as plt


def charting(results) -> list:
    """
    Функция для рисования графика
    """
    cores, times = zip(*results)  # разделяем данные на два списка
    plt.bar(cores, times, align='center', alpha=0.5)
    plt.title('Время выполнения от количества ядер')
    plt.xlabel('Количество ядер')
    plt.ylabel('Время выполнения (с)')
    plt.show()