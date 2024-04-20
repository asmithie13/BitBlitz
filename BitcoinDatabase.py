import sqlite3
import time
import requests
import matplotlib.pyplot as plt
from datetime import datetime

class BitcoinDatabase:
    def __init__(self, db_name='bitcoin.db'):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS bitcoin_data (
                            id INTEGER PRIMARY KEY,
                            timestamp INTEGER,
                            price REAL,
                            volume REAL)''')
        self.conn.commit()

    def add_data(self, timestamp, price, volume):
        self.cur.execute('''INSERT INTO bitcoin_data (timestamp, price, volume)
                            VALUES (?, ?, ?)''', (timestamp, price, volume))
        self.conn.commit()

    def get_data(self):
        self.cur.execute('''SELECT * FROM bitcoin_data''')
        return self.cur.fetchall()

    def fetch_realtime_data(self):
        api_url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        response = requests.get(api_url)
        data = response.json()

        timestamp = int(time.time())  # Current timestamp
        price = data['bpi']['USD']['rate_float']  # USD rate
        volume = None  # Since CoinDesk API doesn't provide volume, set it to None

        return timestamp, price, volume

    def fetch_historical_data(self, hours=24):
        end_time = int(time.time())
        start_time = end_time - hours * 3600  # hours ago

        api_url = f'https://api.coindesk.com/v1/bpi/historical/close.json?start={start_time}&end={end_time}&index=USD'
        response = requests.get(api_url)
        data = response.json()
        
        historical_data = {}
        for date, price in data['bpi'].items():
            timestamp = int(datetime.strptime(date, '%Y-%m-%d').timestamp())
            historical_data[timestamp] = price

        return historical_data



    def plot_recent_prices(self):
        historical_data = self.fetch_historical_data(hours=24)
        if not historical_data:
            print("No historical data fetched.")
            return

        dates = []
        prices = []

        for timestamp, price in historical_data.items():
            dates.append(datetime.fromtimestamp(int(timestamp)))
            prices.append(price)

        plt.plot(dates, prices, marker='o', linestyle='-')
        plt.xlabel('Time')
        plt.ylabel('Price (USD)')
        plt.title('Bitcoin Prices in the Last 24 Hours')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()



    def close_connection(self):
        self.conn.close()
