import sqlite3
import time
import requests

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

    def continuously_update_data(self, interval=1):
        # Update data continuously at specified interval (in seconds)
        while True:
            timestamp, price, volume = self.fetch_realtime_data()
            self.add_data(timestamp, price, volume)
            time.sleep(interval)

    def close_connection(self):
        self.conn.close()
