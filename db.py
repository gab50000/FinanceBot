import logging
from dataclasses import dataclass
import sqlite3


logger = logging.getLogger(__name__)


@dataclass
class Database:
    path: str
    purchase_table: str = "purchases"
    payment_table: str = "payments"

    def __post_init__(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

        try:
            self.cursor.execute(
                f"CREATE TABLE {self.purchase_table} (date text, name text, product name, price float)"
            )
        except sqlite3.OperationalError:
            logger.info("Skipping creation of table %s", self.purchase_table)

        try:
            self.cursor.execute(
                f"CREATE TABLE {self.payment_table} (date text, name text, amount float)"
            )
        except sqlite3.OperationalError:
            logger.info("Skipping creation of table %s", self.payment_table)

        self.connection.commit()

    def __del__(self):
        self.connection.close()

    def insert_payment(self, date, name, amount):
        self.cursor.execute(
            f"INSERT INTO {self.payment_table} VALUES (?, ?, ?)", (date, name, amount)
        )
        self.connection.commit()

    def insert_purchase(self, date, name, product, price):
        self.cursor.execute(
            f"INSERT INTO {self.purchase_table} VALUES (?, ?, ?, ?)",
            (date, name, product, price),
        )
        self.connection.commit()

    @property
    def payments(self):
        return list(self.cursor.execute(f"SELECT * FROM {self.payment_table}"))

    @property
    def purchases(self):
        return list(self.cursor.execute(f"SELECT * FROM {self.purchase_table}"))
