# krakenbot

The kraken trading bot that can access public REST API endpoint of kraken.com cryptocurrency exchange (see docs https://docs.kraken.com/rest/), fetches the latest batch of transactions, saves them to a database table and repeats this action every 10 seconds for an hour.

### MVP 1

- [x] fetches the latest batch of transactions
- [x] saves transactions to a database table
- [x] repeats this action every 10 seconds for an hour
- [ ] write unit tests
- [ ] handle API errors relevant for the public endpoint

### Script execution example (windows)
```console
python run_bot.py --db_name=test.db --table_name=recent --batch_size=3 --duration=60 --interval=10
```

### In case of problems with finding the krakenbot module just run the following command.
```console
python -c "import sys; path = 'C:/Users/szgrad/repos/krakenbot/'; sys.path.append(path)"
```