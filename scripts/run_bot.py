#!/usr/bin/python
"""
The main script for the kraken trading bot that can access public REST API endpoint of kraken.com cryptocurrency exchange (see docs https://docs.kraken.com/rest/), fetches the latest batch of transactions, saves them to a database table and repeats this action every 10 seconds for an hour.
"""

import argparse
from krakenbot.database.connector import DatabaseConnector

from krakenbot.rest.bot import KrakenBot


def run_bot(api_url: str, db_name: str, size: int, pair: str) -> None:
    connector = DatabaseConnector(db_name=db_name)
    bot = KrakenBot(db_name=db_name, api_url=api_url)
    recent_trades = bot.recent_trades(size=size, pair=pair)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api_url",
        type=str,
        default="https://api.kraken.com",
        help="Kraken domain name for api access.",
    )
    parser.add_argument(
        "--db_name",
        type=str,
        help="Database name to which save data from api requests.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=1000,
        help="The size of the latest batch of transactions",
    )
    parser.add_argument(
        "--pair",
        type=str,
        default='XBTUSD',
        help="The name of tradable asset pair to get data for.",
    )
    args = parser.parse_args()
    try:
        run_bot(**vars(args))
    except Exception as e:
        raise e
