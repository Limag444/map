import os
import sys
import io
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt6 import uic
from PyQt6.QtCore import Qt
SCREEN_SIZE = [600, 450]
template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Map</class>
 <widget class="QWidget" name="Map">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1037</width>
    <height>670</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QLabel" name="map">
   <property name="geometry">
    <rect>
     <x>190</x>
     <y>200</y>
     <width>741</width>
     <height>401</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QLineEdit" name="coords">
   <property name="geometry">
    <rect>
     <x>100</x>
     <y>50</y>
     <width>421</width>
     <height>22</height>
    </rect>
   </property>
  </widget>
  <widget class="QPushButton" name="search">
   <property name="geometry">
    <rect>
     <x>540</x>
     <y>50</y>
     <width>93</width>
     <height>28</height>
    </rect>
   </property>
   <property name="text">
    <string>Поиск</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="mashtab">
   <property name="geometry">
    <rect>
     <x>700</x>
     <y>50</y>
     <width>113</width>
     <height>22</height>
    </rect>
   </property>
  </widget>
  <widget class="QPushButton" name="mashtab_button">
   <property name="geometry">
    <rect>
     <x>830</x>
     <y>50</y>
     <width>93</width>
     <height>28</height>
    </rect>
   </property>
   <property name="text">
    <string>Применить</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class Example(QWidget):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.x = '52.317632'
        self.y = '54.886474'
        self.mash_api = '0.0008'
        self.getImage()
        self.initUI()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = '5f3b13d9-8561-40d2-8233-7ab951740aee'
        ll_spn = f'll={self.x},{self.y}8&spn=0.001,{self.mash_api}'
        # Готовим запрос.

        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)
        self.mashtab_button.clicked.connect(self.m_move)
        self.search.clicked.connect(self.map_move)

    def map_move(self):
        cord = self.coords.text().split(', ')
        self.y, self.x = cord[0], cord[1]
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)

    def m_move(self):
        self.mash_api = self.mashtab.text()
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key.Key_A:
    #         pass
    #     if event.key() == Qt.Key.Key_W:
    #         pass
    #     if event.key() == Qt.Key.Key_S:
    #         pass
    #     if event.key() == Qt.Key.Key_D:
    #         pass
    #     if event.key() == Qt.Key.Key_Up:
    #         pass
    #     if event.key() == Qt.Key.Key_Down:
    #         pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
