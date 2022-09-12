# krakenbot

The kraken trading bot that can access public REST API endpoint of kraken.com cryptocurrency exchange (see docs https://docs.kraken.com/rest/), fetches the latest batch of transactions, saves them to a database table and repeats this action every 10 seconds for an hour.

### MVP 1

- [x] fetches the latest batch of transactions
- [ ] saves transactions to a database table
- [ ] repeats this action every 10 seconds for an hour
- [ ] write unit tests
- [ ] handle API errors relevant for the public endpoint
