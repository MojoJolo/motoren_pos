# -*- coding: utf-8 -*-
import MySQLdb as mysql
import MySQLdb.cursors
import arrow

from settings import HOST, USER, PASSWORD, DATABASE

class Db:
    def __init__(self):
        self.db = mysql.connect(HOST, USER, PASSWORD, DATABASE,
          use_unicode=True, charset="utf8", cursorclass=MySQLdb.cursors.DictCursor)

        self.cursor = self.db.cursor()

    def add_inventory(self, item):
        query = """INSERT INTO inventories (name, description, code, stock, price, supplier, category)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        self.cursor.execute(query, item)

        self.db.commit()
        self.db.close()

    def search_inventory(self, q):
        q = "%" + q + "%"
        query = """SELECT * from inventories where name like %s or description like %s or supplier like %s or category like %s"""

        self.cursor.execute(query, (q, q, q, q))
        self.db.close()

        results = self.cursor.fetchall()

        return list(results)

    def get_inventories(self):
        query = """SELECT * from inventories order by id desc limit 50"""

        self.cursor.execute(query)
        self.db.close()

        results = self.cursor.fetchall()

        return list(results)

    def add_transaction(self, srp_total, selling_total):
        query = """INSERT INTO transactions (date, total, actual)
                    VALUES (%s, %s, %s)"""

        datetime = arrow.now().format('YYYY-MM-DD HH:mm:ss')

        self.cursor.execute(query, (datetime, srp_total, selling_total))
        transaction_id = self.cursor.lastrowid

        self.db.commit()
        self.db.close()

        return transaction_id

    def add_sales(self, sales):
        query = """INSERT INTO sales (inventory_id, quantity, price, actual, transaction_id)
                    VALUES (%s, %s, %s, %s, %s)"""

        self.cursor.executemany(query, sales)
        self.db.commit()
        self.db.close()

    def update_inventory(self, inventories):
        query = """UPDATE inventories SET stock = %s where id = %s"""

        self.cursor.executemany(query, inventories)
        self.db.commit()
        self.db.close()

    def add_category(self, category):
        query = """INSERT INTO  categories (name) VALUES (%s)"""

        self.cursor.execute(query, [category])

        self.db.commit()
        self.db.close()

    def get_categories(self):
        query = """SELECT * from categories"""

        self.cursor.execute(query)
        self.db.close()

        results = self.cursor.fetchall()

        return list(results)

    def delete_category(self, category_id):
        query = """DELETE FROM categories WHERE id = %s"""

        self.cursor.execute(query, [category_id])

        self.db.commit()
        self.db.close()

    def add_supplier(self, supplier):
        query = """INSERT INTO  suppliers (name) VALUES (%s)"""

        self.cursor.execute(query, [supplier])

        self.db.commit()
        self.db.close()

    def get_suppliers(self):
        query = """SELECT * from suppliers"""

        self.cursor.execute(query)
        self.db.close()

        results = self.cursor.fetchall()

        return list(results)

    def delete_supplier(self, supplier_id):
        query = """DELETE FROM suppliers WHERE id = %s"""

        self.cursor.execute(query, [supplier_id])

        self.db.commit()
        self.db.close()

    def delete_inventory(self, item_id):
        query = """DELETE FROM inventories WHERE id = %s"""

        self.cursor.execute(query, [item_id])

        self.db.commit()
        self.db.close()

    def view_inventory(self, item_id):
        query = """SELECT * FROM inventories WHERE id = %s"""

        self.cursor.execute(query, [item_id])
        self.db.close()

        return self.cursor.fetchone()

    def edit_inventory(self, item):
        query = """UPDATE inventories SET
            name = %s,
            description = %s,
            code = %s,
            stock = %s,
            price = %s,
            supplier = %s,
            category = %s
            where id = %s"""

        self.cursor.execute(query, item)
        
        self.db.commit()
        self.db.close()

    def view_transactions(self, date):
        date = date + "%"
        query = """SELECT * from sales left join transactions on transactions.id = transaction_id
                    left join inventories on inventories.id = inventory_id
                    where date like %s
                    and inventories.id is not NULL"""

        self.cursor.execute(query, [date])
        self.db.close()

        results = self.cursor.fetchall()

        return list(results)

    def delete_sale(self, sale_id):
        query = """DELETE FROM sales WHERE id = %s"""

        self.cursor.execute(query, [sale_id])

        self.db.commit()
        self.db.close()

    def update_sale(self, sale_id, quantity, returnee):
        divisor = 1.0 * (quantity - returnee) / quantity

        query = """UPDATE sales SET quantity = %s,
            price = price * %s,
            actual = actual * %s
            where id = %s"""

        self.cursor.execute(query, (quantity - returnee, divisor, divisor, sale_id))
        
        self.db.commit()
        self.db.close()

    def add_return(self, item_id, quantity, date):
        query = """INSERT INTO  returns (inventory_id, quantity, date) VALUES (%s, %s, %s)"""

        self.cursor.execute(query, (item_id, quantity, date))

        self.db.commit()
        self.db.close()

    def add_item_quantity(self, item_id, quantity):
        query = """UPDATE inventories SET stock = stock + %s where id = %s"""

        self.cursor.execute(query, (quantity, item_id))
        
        self.db.commit()
        self.db.close()


