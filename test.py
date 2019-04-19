import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtGui import QPixmap
import requests


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main1.ui', self)


        self.newans = False

        self.pushButton.clicked.connect(self.run)
        self.sbros.clicked.connect(self.sbro_s)
        self.lon.setText("63.057663")
        self.lat.setText("57.683716")
        self.delta1.setText("0.002")
        self.delta2.setText("0.002")

    def sbro_s(self):

        self.newans = False
        self.fulladres.setText("")
        self.run()

    def keyPressEvent(self, event):

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

        if self.place.text() != "":

            self.newans = True

            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

            geocoder_params = {"geocode": self.place.text(), "format": "json"}

            response = requests.get(geocoder_api_server, params=geocoder_params)
            if not response:
                # обработка ошибочной ситуации
                pass

            # Преобразуем ответ в json-объект
            json_response = response.json()

            # Получаем первый топоним из ответа геокодера.
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            # Координаты центра топонима:
            toponym_coodrinates = toponym["Point"]["pos"]
            # Долгота и широта:
            toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

            delta1Down = toponym["boundedBy"]['Envelope']['lowerCorner'].split(" ")
            delta1Up = toponym["boundedBy"]['Envelope']['upperCorner'].split(" ")

            self.org_point = "{0},{1}".format(toponym_longitude, toponym_lattitude)
            self.fulladres.setText(toponym["metaDataProperty"]["GeocoderMetaData"]["text"])
            # Собираем параметры для запроса к StaticMapsAPI:
            vid = ""
            if self.map_2.isChecked():
                vid = "map"
            if self.sat.isChecked():
                vid = "sat"
            if self.skl.isChecked():
                vid = "sat,skl"

            params = {
                "ll": ",".join([toponym_longitude, toponym_lattitude]),
                "spn": ",".join([str((float(delta1Up[0]) - float(delta1Down[0])) / 2),
                                 str((float(delta1Up[1]) - float(delta1Down[1])) / 2)]),
                "l": vid,
                "pt": "{0},pm2dgl".format(self.org_point)
            }
            self.lon.setText(str(toponym_longitude))
            self.lat.setText(toponym_lattitude)
            self.delta1.setText(str((float(delta1Up[0]) - float(delta1Down[0])) / 2))
            self.delta2.setText(str((float(delta1Up[1]) - float(delta1Down[1])) / 2))

        response = None
        api_server = "http://static-maps.yandex.ru/1.x/"
        vid = ""
        if self.map_2.isChecked():
            vid = "map"
        if self.sat.isChecked():
            vid = "sat"
        if self.skl.isChecked():
            vid = "sat,skl"
        if self.place.text() == "":
            lon = self.lon.text()
            lat = self.lat.text()
            delta1 = self.delta1.text()
            delta2 = self.delta2.text()

            params = {
                "ll": ",".join([lon, lat]),
                "spn": ",".join([delta1, delta2]),
                "l": vid
            }
        if self.newans == True:
            lon = self.lon.text()
            lat = self.lat.text()
            delta1 = self.delta1.text()
            delta2 = self.delta2.text()
            params = {
                "ll": ",".join([lon, lat]),
                "spn": ",".join([delta1, delta2]),
                "l": vid,
                "pt": "{0},pm2dgl".format(self.org_point)
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
        if self.map_2.isChecked():
            map_file = "map.png"

        if self.sat.isChecked() or self.skl.isChecked():
            map_file = "map.jpg"

        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)
        pixmap = QPixmap(map_file)
        self.map.setPixmap(pixmap)
        self.map.resize(pixmap.width(), pixmap.height())
        self.place.setText("")


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
