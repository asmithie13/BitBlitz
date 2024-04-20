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

        # Plot historical prices for the past 30 days
        end_date = time.strftime('%Y-%m-%d')
        start_date = (time.time() - 30 * 24 * 3600)  # 30 days ago
        start_date = time.strftime('%Y-%m-%d', time.gmtime(start_date))

        bitcoin_db.plot_recent_prices()


        #bitcoin_db = BitcoinDatabase()
        #bitcoin_db.continuously_update_data() 

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
