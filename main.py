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

        self.bitcoin_db.update_historical_table("bitcoin")
        self.bitcoin_db.plot_recent_prices("bitcoin")

        self.bitcoin_db.update_historical_table("ethereum")
        self.bitcoin_db.plot_recent_prices("ethereum")
        
        self.bitcoin_db.update_historical_table("litecoin")
        self.bitcoin_db.plot_recent_prices("litecoin")

        '''self.bitcoin_db.plot_recent_prices("bitcoin")
        self.bitcoin_db.update_historical_table("bitcoin")
        self.bitcoin_db.plot_recent_prices("bitcoin")
        self.bitcoin_db.update_historical_table("bitcoin")
        self.bitcoin_db.plot_recent_prices("bitcoin")
        self.bitcoin_db.update_historical_table("bitcoin")'''

        self.tableWidget.cellClicked.connect(lambda row=1, column=0: self.handleBitcoin(row, column))


    def handleBitcoin(self, row, column):
        if not (row == 0 and column == 0): return

        pixmap = QPixmap('bitcoin_prices.png')
        self.label_2.setPixmap(pixmap)
        self.label.setText('Selected Crypto: Bitcoin')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
