#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
 Создать БД автоматизации учёта транспортных средств
 сотрудниками государственной дорожно – транспортной службы региона РФ
"""

import sys
import psycopg2
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)
from PyQt5 import QtCore

app = QApplication(sys.argv)


class View(QWidget):
    def __init__(self):
        super().__init__()
        self.tb = Tb()
        self.setWindowTitle("Программа учёта")
        self.setGeometry(700, 710, 700, 710)
        self.name = QLabel("Система учета транспортных средств Ставропольского края")
        self.name.setStyleSheet(
            """
            font: bold;
            font-size: 20px;
            """
        )
        self.setStyleSheet(
            """
            font-size: 15px;
            """
        )
        self.btn1 = QPushButton("Добавить")
        self.btn2 = QPushButton("Удалить")
        self.inp1_prompt = QLabel("Имя владельца")
        self.inp1 = QLineEdit()
        self.inp2_prompt = QLabel("Номер")
        self.inp2 = QLineEdit()
        self.inp3_prompt = QLabel("Вин-код")
        self.inp3 = QLineEdit()
        self.inp4_date = QDateEdit()
        self.inp4_prompt = QLabel("Дата постановки на учет")
        self.inp5_prompt = QLabel("Модель")
        self.inp5 = QLineEdit()
        self.inp4_date.setCalendarPopup(True)
        self.inp4_date.setTimeSpec(QtCore.Qt.LocalTime)
        self.inp4_date.setGeometry(QtCore.QRect(220, 31, 133, 20))
        self.inp1.setFixedWidth(400)
        self.inp2.setFixedWidth(400)
        self.inp3.setFixedWidth(400)
        self.inp4_date.setFixedWidth(250)
        self.inp5.setFixedWidth(400)
        self.remove_item = ""
        self.create_view()

    def create_view(self):
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.name)
        vbox.addWidget(self.tb)
        vbox.addWidget(self.inp1_prompt)
        vbox.addWidget(self.inp1)
        vbox.addWidget(self.inp2_prompt)
        vbox.addWidget(self.inp2)
        vbox.addWidget(self.inp3_prompt)
        vbox.addWidget(self.inp3)
        vbox.addWidget(self.inp5_prompt)
        vbox.addWidget(self.inp5)
        vbox.addWidget(self.inp4_prompt)
        vbox.addWidget(self.inp4_date)
        hbox.addStretch(1)
        hbox.addWidget(self.btn1)
        hbox.addWidget(self.btn2)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


class Tb(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(10, 10, 300, 500)
        self.setColumnCount(5)
        self.verticalHeader().hide()
        self.setEditTriggers(QTableWidget.NoEditTriggers)


class Model(View):
    def __init__(self):
        super().__init__()
        self.conn = psycopg2.connect(
            user="postgres", password="1234", host="127.0.0.1", port="5432"
        )
        self.tb.cellClicked.connect(self.cell_click)
        self.btn1.clicked.connect(self.ins)
        self.btn2.clicked.connect(self.dels)
        self.cur = self.conn.cursor()
        self.updt()

    def updt(self):
        self.tb.clear()
        self.tb.setRowCount(0)
        self.tb.setHorizontalHeaderLabels(
            ["ФИО", "Номер", "VIN", "Дата регистрации", "Модель"]
        )
        self.cur.execute("select * from cars")
        rows = self.cur.fetchall()
        i = 0
        for elem in rows:
            self.tb.setRowCount(self.tb.rowCount() + 1)
            j = 0
            for t in elem:
                self.tb.setItem(i, j, QTableWidgetItem(str(t).strip()))
                j += 1
            i += 1

    def cell_click(self, row, col):
        self.remove_item = self.tb.item(row, 0).text()

    def ins(self):
        self.cur.execute(
            f"insert into cars values ('{self.inp1.text()}', '{self.inp2.text()}',"
            f" '{self.inp3.text()}', '{self.inp4_date.text()}', '{self.inp5.text()}')"
        )
        self.update_view()
        self.show_info_messagebox("Добавлено")

    def dels(self):
        self.cur.execute(f"delete from cars where vin_id like '{self.remove_item}'")
        self.update_view()
        self.show_info_messagebox(
            f"Транспорт с vin-номером  {self.remove_item}  удален"
        )

    def update_view(self):
        self.conn.commit()
        self.updt()
        self.inp1.setText("")
        self.inp2.setText("")
        self.inp3.setText("")
        self.inp5.setText("")

    def show_info_messagebox(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("Уведомление")
        retval = msg.exec_()

    def create_db(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cars(
            vin_id TEXT NOT NULL,
            owner_name TEXT NOT NULL,
            gos_number TEXT NOT NULL,
            date_reg TEXT NOT NULL,
            model TEXT NOT NULL
            )
            """
        )


if __name__ == "__main__":
    application = Model()
    application.show()
    sys.exit(app.exec_())
