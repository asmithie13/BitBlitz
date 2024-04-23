import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi
from CryptoDatabase import CryptoDatabase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("StartScreen.ui", self)

        self.bitcoin_db = CryptoDatabase()
        self.bitcoin_db.create_table()

        cryptos = ["bitcoin","ethereum", "dogecoin", "solana", "avalanche", "tether", "tron", "stellar", "litecoin"]

        for crypto in cryptos:
            self.bitcoin_db.update_historical_table(crypto)
            self.bitcoin_db.plot_recent_prices(crypto)

        self.updateData()

        self.tableWidget.cellClicked.connect(self.handleCellClick)
        self.lineEdit.returnPressed.connect(self.buyCoin)



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

    def buyCoin(self):
        crypto_names = ["bitcoin", "ethereum", "dogecoin", "solana", "avalanche", "tether", "tron", "stellar", "litecoin"]
        symbol = self.tableWidget.currentItem().text()

        dollars = float(self.lineEdit.text())

        if symbol.lower() not in crypto_names: return
        self.bitcoin_db.purchaseCoin(dollars,symbol)
        self.updateData()

    def updateData(self):
        cryptos = ["bitcoin", "ethereum", "dogecoin", "solana", "avalanche", "tether", "tron", "stellar", "litecoin"]
        priceList = []

        for coin in cryptos: priceList.append(self.bitcoin_db.getExtremePrices(coin))
        invested, gain = self.bitcoin_db.updatePurchaseTable(priceList)

        self.label_5.setText("$" + (str(invested)))
        self.label_7.setText(str(format(gain, ".00%")))

        for i in range(9):
            perf = (float(priceList[i][0]) / float(priceList[i][1])) * 100 - 100
            perf = f"{perf:.2f}" + "%"
            self.tableWidget.setItem(i, 1, QTableWidgetItem(perf))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
