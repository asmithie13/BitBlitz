import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi
from CryptoDatabase import CryptoDatabase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("StartScreen.ui", self)

        self.bitcoin_db = CryptoDatabase()
        self.bitcoin_db.create_table()

        cryptos = ["bitcoin", "ethereum", "dogecoin", "solana", "avalanche", "tether", "tron", "stellar", "litecoin"]

        for crypto in cryptos:
            self.bitcoin_db.update_historical_table(crypto)
            self.bitcoin_db.plot_recent_prices(crypto)

        self.tableWidget.cellClicked.connect(self.handleCellClick)


    def handleCellClick(self, row, column):
        crypto_names = ["bitcoin", "ethereum", "dogecoin", "solana", "avalanche", "tether", "tron", "stellar", "litecoin"]
        crypto_item = self.tableWidget.item(row, column)
        if crypto_item is None:
            return

        crypto = crypto_item.text().lower()
        if crypto in crypto_names:
            pixmap = QPixmap(f'{crypto}_prices.png')
            self.label_2.setPixmap(pixmap)
            self.label.setText(f'Selected Crypto: {crypto.capitalize()}')


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
