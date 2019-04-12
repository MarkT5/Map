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
        self.lon.setText("63.057663")
        self.lat.setText("57.683716")
        self.delta1.setText("0.002")
        self.delta2.setText("0.002")

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == 16777238:
            if float(self.delta1.text()) * 2 < 90:
                self.delta1.setText(str(float(self.delta1.text()) * 2))
            else:
                self.delta1.setText(str(90))
            if float(self.delta2.text()) * 2 < 90:
                self.delta2.setText(str(float(self.delta2.text()) * 2))
            else:
                self.delta2.setText(str(90))
            self.run()

        if event.key() == 16777239:
            if float(self.delta1.text()) / 2 > 0.001:
                self.delta1.setText(str(float(self.delta1.text()) / 2))
            else:
                self.delta1.setText(str(0.001))
            if float(self.delta2.text()) / 2 > 0.001:
                self.delta2.setText(str(float(self.delta2.text()) / 2))
            else:
                self.delta2.setText(str(0.001))
            self.run()
        if event.key() == 16777235:  # вверх
            if float(self.lat.text()) + float(self.delta1.text()) < 85:
                self.lat.setText(str(float(self.lat.text()) + float(self.delta1.text())))
                self.run()
            else:
                self.lat.setText(str(85))
                self.run()
        if event.key() == 16777237:  # вниз
            if float(self.lat.text()) - float(self.delta1.text()) > -86:
                self.lat.setText(str(float(self.lat.text()) - float(self.delta1.text())))
                self.run()
            else:
                self.lat.setText(str(-86))
                self.run()

        if event.key() == 16777234:  # влево 57.683716, 63.057663
            print(float(self.lon.text()) - float(self.delta2.text()))
            if float(self.lon.text()) - float(self.delta2.text()) > -178:
                self.lon.setText(str(float(self.lon.text()) - float(self.delta2.text())))
                self.run()
            else:
                self.lon.setText(str(-178))
                self.run()

        if event.key() == 16777236:  # вправо
            if float(self.lon.text()) + float(self.delta2.text()) < 178:
                self.lon.setText(str(float(self.lon.text()) + float(self.delta2.text())))
                self.run()
            else:
                self.lon.setText(str(178))
                self.run()

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
