# CloudWalk Monitoring analyst test

This project consists of five Python scripts that work together to monitor transaction data and detect anomalies.

The first script, initializeDatabase.py, creates the necessary database structure. Please ensure that you change the username, host, and password in the script to match your database configuration.

The second script, server.py, initializes the endpoint which allows us to receive transaction data.

The third script, generateCharges.py, creates valid and invalid transaction data which is then fed into the endpoint.

The fourth script, summarizesql.py, processes the transaction data received by the endpoint, summarizes it, and inserts it into a SQL table.

Finally, the fifth script, telegrambot.py, reads the SQL table populated by summarizesql.py and executes queries to detect any anomalies. If an anomaly is detected, a message is sent to the monitoring team via Telegram.

We recommend running these scripts in sequence to ensure proper functioning of the monitoring system.