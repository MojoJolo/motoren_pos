# -*- coding: utf-8 -*-
import MySQLdb as mysql
import MySQLdb.cursors

from settings import HOST, USER, PASSWORD, DATABASE

class Db:
    def __init__(self):
        self.db = mysql.connect(HOST, USER, PASSWORD, DATABASE,
          use_unicode=True, charset="utf8", cursorclass=MySQLdb.cursors.DictCursor)

        self.cursor = self.db.cursor()

    def add_inventory(self, item):
        query = """INSERT INTO inventories (name, description, code, stock, price, supplier)
                    VALUES (%s, %s, %s, %s, %s, %s)"""

        self.cursor.execute(query, item)

        self.db.commit()
        self.db.close()

    def search_inventory(self, q):
        q = "%" + q + "%"
        query = """SELECT * from inventories where name like %s or description like %s"""

        self.cursor.execute(query, (q, q))
        self.db.close()

        results = self.cursor.fetchall()

        return list(results)

    def get_inventories(self):
        query = """SELECT * from inventories"""

        self.cursor.execute(query)
        self.db.close()

        results = self.cursor.fetchall()

        return list(results)