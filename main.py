import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
from BitcoinDatabase import BitcoinDatabase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("StartScreen.ui", self)

        bitcoin_db = BitcoinDatabase()
        bitcoin_db.plot_recent_prices()
        bitcoin_db.update_historical_table

        #bitcoin_db = BitcoinDatabase()
        #bitcoin_db.continuously_update_data() 

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
