from dataclasses import dataclass
import sqlite3


@dataclass
class Database:
    path: str
    purchase_table: str = "purchases"
    payment_table: str = "payments"

    def __post_init__(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            f"CREATE TABLE {self.purchase_table} (date text, name text, price float)"
        )
        self.cursor.execute(
            f"CREATE TABLE {self.payment_table} (date text, amount float)"
        )
        self.connection.commit()
