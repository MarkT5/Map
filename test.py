import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QPixmap
import requests

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main1.ui', self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        response = None
        api_server = "http://static-maps.yandex.ru/1.x/"

        lon = self.lon.text()
        lat = self.lat.text()
        delta1 = self.delta1.text()
        delta2 = self.delta2.text()

        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([delta1, delta2]),
            "l": "map"
        }

        try:

            response = requests.get(api_server, params=params)

            if not response:
                print("Ошибка выполнения запроса:")

                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
        except:
            print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        map_file = "map.png"
        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)
        pixmap = QPixmap("map.png")
        self.map.setPixmap(pixmap)
        self.map.resize(pixmap.width(), pixmap.height())



app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())