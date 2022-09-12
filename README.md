# krakenbot

Write a program that can access public REST API endpoint of kraken.com cryptocurrency exchange (see docs https://docs.kraken.com/rest/), fetches the latest batch of transactions, saves them to a database table and repeats this action every 10 seconds for an hour.
Write unit tests and handle API errors relevant for the public endpoint.



Use requests library or aiohttp.
