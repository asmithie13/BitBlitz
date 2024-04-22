import sqlite3
import time
import requests
import matplotlib.pyplot as plt
from datetime import datetime

class CryptoDatabase:
    def __init__(self, db_name='bitcoin.db'):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table()
        #self.update_historical_table()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS bitcoin_data (
                            id INTEGER PRIMARY KEY,
                            timestamp INTEGER,
                            symbol TEXT,
                            price REAL,
                            volume REAL)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS ethereum_data (
                            id INTEGER PRIMARY KEY,
                            timestamp INTEGER,
                            symbol TEXT,
                            price REAL,
                            volume REAL)''')
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS dogecoin_data (
                            id INTEGER PRIMARY KEY,
                            timestamp INTEGER,
                            symbol TEXT,
                            price REAL,
                            volume REAL)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS solana_data (
                            id INTEGER PRIMARY KEY,
                            timestamp INTEGER,
                            symbol TEXT,
                            price REAL,
                            volume REAL)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS avalanche_data (
                            id INTEGER PRIMARY KEY,
                            timestamp INTEGER,
                            symbol TEXT,
                            price REAL,
                            volume REAL)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS tether_data (
                            id INTEGER PRIMARY KEY,
                            timestamp INTEGER,
                            symbol TEXT,
                            price REAL,
                            volume REAL)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS tron_data (
                            id INTEGER PRIMARY KEY,
                            timestamp INTEGER,
                            symbol TEXT,
                            price REAL,
                            volume REAL)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS stellar_data (
                            id INTEGER PRIMARY KEY,
                            timestamp INTEGER,
                            symbol TEXT,
                            price REAL,
                            volume REAL)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS litecoin_data (
                            id INTEGER PRIMARY KEY,
                            timestamp INTEGER,
                            symbol TEXT,
                            price REAL,
                            volume REAL)''')
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS userData (
                            coin VARCHAR,
                            coinTotal REAL,
                            initial_USD REAL,
                            initial_Coin_Price REAL,
                            current_Coin_Price REAL,
                            percentProfit REAL)''')
        self.conn.commit()

    def add_data(self, symbol, timestamp, price, volume):
        table_name = f"{symbol.lower()}_data"
        self.cur.execute(f'''INSERT INTO {table_name} (timestamp, symbol, price, volume)
                            VALUES (?, ?, ?, ?)''', (timestamp, symbol, price, volume))
        self.conn.commit()

    def get_data(self, symbol):
        # Fetch historical data from the database for the specified symbol
        query = f"SELECT timestamp, price FROM {symbol.lower()}_data"
        self.cur.execute(query)
        rows = self.cur.fetchall()

        # Process fetched data into a dictionary
        historical_data = {}
        for row in rows:
            timestamp, price = row
            historical_data[timestamp] = price

        return historical_data


    def fetch_realtime_data(self, symbol):
        api_url = f'https://api.coincap.io/v2/assets/{symbol.lower()}'
        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            timestamp = int(time.time())  # Current timestamp
            price = float(data['data']['priceUsd'])  # USD rate
            volume = None  # CoinCap API doesn't provide volume, set it to None

            return timestamp, price, volume
        else:
            print(f"Failed to fetch data for {symbol}: {data['error']}")
            return None, None, None
        
    def continuously_update_data(self, symbol, interval=60):
        while True:
            timestamp, price, _ = self.fetch_realtime_data(symbol)
            self.add_data(symbol, timestamp, price, 0)
            print(f"Added data for {symbol}: Timestamp={timestamp}, Price={price}")
            time.sleep(interval)

    def update_historical_table(self, symbol):
        # Clear the existing data from the table
        table_name = f"{symbol.lower()}_data"
        self.cur.execute(f'''DELETE FROM {table_name}''')
        self.conn.commit()

        # Fetch historical data for the last 24 hours
        historical_data = self.fetch_historical_data(symbol, hours=24)

        # Insert fetched historical data into the table
        for timestamp, price in historical_data.items():
            self.add_data(symbol, timestamp, price, 0)  # Volume is set to 0 for historical data

        print(f"Historical table updated for {symbol}.")
              
    def fetch_historical_data(self, symbol, hours=24):
        end_time = int(time.time()) * 1000  # in milliseconds
        start_time = end_time - hours * 60 * 60 * 1000  # hours ago

        api_url = f'https://api.coincap.io/v2/assets/{symbol}/history?interval=m1&start={start_time}&end={end_time}'
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
            print(f"Failed to fetch historical data for {symbol}: {data['error']}")
            return {}

    def plot_recent_prices(self, symbol):
        historical_data = self.get_data(symbol)
        if not historical_data:
            print(f"No historical data fetched for {symbol}.")
            return

        timestamps = list(historical_data.keys())
        prices = list(historical_data.values())

        # Convert prices to numerical values (floats)
        prices = [float(price) for price in prices]

        dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]

        plt.figure()

        plt.plot(dates, prices, linestyle='-')
        plt.xlabel('Time')
        plt.ylabel('Price (USD)')
        plt.title(f'{symbol.upper()} Prices in the Last 24 Hours')

        # Adjusting the number of price ticks
        num_ticks = 8
        price_min = min(prices)
        price_max = max(prices)
        price_step = (price_max - price_min) / (num_ticks - 1)
        price_ticks = [price_min + i * price_step for i in range(num_ticks)]
        plt.yticks(price_ticks)

        plt.tight_layout()
        plt.savefig(f'{symbol}_prices.png')
        # plt.show()

    def get_newest_data(self, symbol):
        table_name = f"{symbol.lower()}_data"
        query = f"SELECT timestamp, price FROM {table_name} ORDER BY timestamp DESC LIMIT 1"
        self.cur.execute(query)
        row = self.cur.fetchone()

        if row:
            timestamp, price = row
            return timestamp, float(price)
        else:
            print(f"No data found for {symbol}.")
            return None, None

    def purchaseCoin(self,dollars,symbol):
        tableName = "userData"
        latestTime, price = self.get_newest_data(symbol)
        coinTotal = dollars/price

        self.cur.execute(f'''INSERT INTO {tableName} (coin, coinTotal, initial_USD, initial_Coin_Price, current_Coin_Price, percentProfit)
                            VALUES (?, ?, ?, ?, ?, ?)''', (symbol, coinTotal, dollars, price, price,0))
        self.conn.commit()


    def close_connection(self):
        self.conn.close()

