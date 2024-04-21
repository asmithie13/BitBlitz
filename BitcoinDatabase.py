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
        self.update_historical_table()

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
        api_url = 'https://api.coincap.io/v2/assets/bitcoin'
        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            timestamp = int(time.time())  # Current timestamp
            price = float(data['data']['priceUsd'])  # USD rate
            volume = None  # CoinCap API doesn't provide volume, set it to None

            return timestamp, price, volume
        else:
            print(f"Failed to fetch data: {data['error']}")
            return None, None, None
        
    def continuously_update_data(self, interval=60):
        while True:
            timestamp, price, _ = self.fetch_realtime_data()
            self.add_data(timestamp, price,0)
            print(f"Added data: Timestamp={timestamp}, Price={price}")
            time.sleep(interval)

    def update_historical_table(self):
        # Clear the existing data from the table
        self.cur.execute('''DELETE FROM bitcoin_data''')
        self.conn.commit()

        # Fetch historical data for the last 24 hours
        historical_data = self.fetch_historical_data(hours=24)

        # Insert fetched historical data into the table
        for timestamp, price in historical_data.items():
            self.add_data(timestamp, price, 0)  # Volume is set to 0 for historical data

        print("Historical table updated.")

    def fetch_historical_data(self, hours=24):
        end_time = int(time.time()) * 1000  # in milliseconds
        start_time = end_time - hours * 60 * 60 * 1000  # hours ago

        api_url = f'https://api.coincap.io/v2/assets/bitcoin/history?interval=m1&start={start_time}&end={end_time}'
        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            historical_data = {}
            for point in data['data']:
                timestamp = point['time']
                price = point['priceUsd']
                historical_data[timestamp] = price

            return historical_data
        else:
            print(f"Failed to fetch historical data: {data['error']}")
            return {}

    def plot_recent_prices(self):
        historical_data = self.fetch_historical_data(hours=24)
        if not historical_data:
            print("No historical data fetched.")
            return

        timestamps = list(historical_data.keys())
        prices = list(historical_data.values())

        # Convert prices to numerical values (floats)
        prices = [float(price) for price in prices]

        dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]

        plt.plot(dates, prices, linestyle='-')
        plt.xlabel('Time')
        plt.ylabel('Price (USD)')
        plt.title('Bitcoin Prices in the Last 24 Hours')

        # Adjusting the number of price ticks
        num_ticks = 8
        price_min = min(prices)
        price_max = max(prices)
        price_step = (price_max - price_min) / (num_ticks - 1)
        price_ticks = [price_min + i * price_step for i in range(num_ticks)]
        plt.yticks(price_ticks)

        plt.tight_layout()
        plt.savefig('bitcoin_prices.png')
        plt.show()

    def close_connection(self):
        self.conn.close()
