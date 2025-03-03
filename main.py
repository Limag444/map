import os
import sys
import io
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt6 import uic
from PyQt6.QtCore import Qt
template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Map</class>
 <widget class="QWidget" name="Map">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>593</width>
    <height>574</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QLabel" name="map">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>140</y>
     <width>571</width>
     <height>421</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QLineEdit" name="coords">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>30</y>
     <width>341</width>
     <height>22</height>
    </rect>
   </property>
  </widget>
  <widget class="QPushButton" name="search">
   <property name="geometry">
    <rect>
     <x>350</x>
     <y>30</y>
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
     <x>0</x>
     <y>90</y>
     <width>113</width>
     <height>22</height>
    </rect>
   </property>
  </widget>
  <widget class="QPushButton" name="mashtab_button">
   <property name="geometry">
    <rect>
     <x>120</x>
     <y>90</y>
     <width>93</width>
     <height>28</height>
    </rect>
   </property>
   <property name="text">
    <string>Применить</string>
   </property>
  </widget>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>140</x>
     <y>10</y>
     <width>71</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Координаты</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_2">
   <property name="geometry">
    <rect>
     <x>30</x>
     <y>70</y>
     <width>61</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Масштаб</string>
   </property>
  </widget>
  <widget class="QPushButton" name="vvod">
   <property name="geometry">
    <rect>
     <x>500</x>
     <y>50</y>
     <width>93</width>
     <height>28</height>
    </rect>
   </property>
   <property name="text">
    <string>Ввод</string>
   </property>
  </widget>
  <widget class="QPushButton" name="ok">
   <property name="geometry">
    <rect>
     <x>500</x>
     <y>80</y>
     <width>93</width>
     <height>28</height>
    </rect>
   </property>
   <property name="text">
    <string>Готово</string>
   </property>
  </widget>
  <widget class="QPushButton" name="theme_butn">
   <property name="geometry">
    <rect>
     <x>492</x>
     <y>20</y>
     <width>101</width>
     <height>28</height>
    </rect>
   </property>
   <property name="text">
    <string>Изменить тему</string>
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
        self.x = 52.317632
        self.y = 54.886474
        self.mash_api = 0.001
        self.theme = 'theme=light'
        self.getImage()
        self.initUI()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = '5f3b13d9-8561-40d2-8233-7ab951740aee'
        ll_spn = f'll={self.x},{self.y}8&spn=0.001,{self.mash_api}'

        map_request = f"{server_address}{ll_spn}&{self.theme}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)

    def initUI(self):
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)
        self.mashtab_button.clicked.connect(self.mash_move)
        self.search.clicked.connect(self.map_move)
        self.vvod.clicked.connect(self.vvod_api)
        self.ok.clicked.connect(self.ok_api)
        self.theme_butn.clicked.connect(self.theme_fun)

    def vvod_api(self):
        self.coords.setReadOnly(False)
        self.mashtab.setReadOnly(False)
    def ok_api(self):
        self.coords.setReadOnly(True)
        self.mashtab.setReadOnly(True)

    def map_move(self):
        cord = self.coords.text().split(', ')
        self.y, self.x = float(cord[0]), float(cord[1])
        self.getImage()

    def mash_move(self):
        self.mash_api = float(self.mashtab.text())
        self.getImage()

    def theme_fun(self):
        if self.theme == 'theme=light':
            self.theme = 'theme=dark'
        else:
            self.theme = 'theme=light'
        self.getImage()

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_A:
            if self.x - self.mash_api / 2 >= -170:
                self.x -= self.mash_api / 2
                self.getImage()
        if event.key() == Qt.Key.Key_W:
            if self.y + self.mash_api / 2 <= 85:
                self.y += self.mash_api / 2
                self.getImage()
        if event.key() == Qt.Key.Key_S:
            if self.y - self.mash_api / 2 >= -85:
                self.y -= self.mash_api / 2
                self.getImage()
        if event.key() == Qt.Key.Key_D:
            if self.x + self.mash_api / 2 <= 170:
                self.x += self.mash_api / 2
                self.getImage()
        if event.key() == Qt.Key.Key_Up:
            if self.mash_api * 10 <= 10:
                self.mash_api *= 10
                self.getImage()

        if event.key() == Qt.Key.Key_Down:
            if self.mash_api / 10 >= 0.0001:
                self.mash_api /= 10
                self.getImage()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
