
# BitBlitz

## Design Overview

![BitBlitz Logo](BitBlitz.png)

BitBlitz is an application designed to be able to simulate cryptocurrecny trades. The software was developed utilizing QtDesigner and pyqt signals for both frontend and backend communication. It interfaces with the Coincap API to get accurate 24 hour data of the latest cryptocurrency prices. This data is fetched upon the start up of the program and is stored and used in databases utilizing sqLite. When the user clicks on the coin on the menu to the right, a plot of the latest 24 hour coin movements is displayed using matplotlib. The user also can simulate purchasing a coin by typing in the amount in USD in the left hand corner and hitting enter. In the class CrypoDatabase.py, there is the use of scripting SQL to manipulate and fetch from various databases holding information of different coins and the current user information of simulated sales. The software used to interface and view the databases is DBeaver, a universal database application. Here different tables are listed for Bitcoin, Ethereum, Dogecoin, Solana, Avalanche, Tether, TRON, Stellar, and Litecoin showing data that includes prices. UserData is a menu that shows what coins have already been bought, profits, and performance of each coin.

![dBeaver view](dBeaver.png)

The original design concepts used were most of what is contained in this finalzied design. Going in, I always planned on using python, QtDesigner, APIs, and databases to construct the application. There are two aspects from my original design that are not yet in the application but will be in the future.

1. A CoinDesk API will eventually be used to execute the trades instead of just simulating them.
2. Machine learning will be implemented to allow for autonomous trading. This algorithm will be taught utilizing traditional indicators to try to time the price changes to make a profit. This will be a much more time intensive aspect of the application that will be done in the months to come.

This project is able to be a 6-week application because of what has already been implemented. The system already has the ability to get accurate coin data, display this to the user, and simulate trades. Adding real trading functionality will not be a challenging step. Additionally adding machine learning that learns from successful and failure trades will take time that will be done over the following months as I expand on this to be an intensive personal project.

## Preliminary Design Verification