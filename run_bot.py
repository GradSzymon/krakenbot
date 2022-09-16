#!/usr/bin/python
'''
The main script for the kraken trading bot that can access public REST API endpoint of kraken.com cryptocurrency exchange (see docs https://docs.kraken.com/rest/), fetches the latest batch of transactions, saves them to a database table and repeats this action every 10 seconds for an hour.
'''

import argparse
import asyncio
import logging
from krakenbot.database.connectors.sqlite import SQLiteConnector

from krakenbot.rest.bot import KrakenBot

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def run_bot(api_url: str, db_name: str, table_name: str, batch_size: int, pair: str, duration: float, interval: float) -> None:
    connector = SQLiteConnector(db_name=db_name)
    bot = KrakenBot(db_connector=connector)
    columns = ['"pair name"', 'price', 'volume', 'time', '"buy(b)/sell(s)"', '"market(m)/limit(l)"', 'miscellaneous']
    columns_names = " ,".join(columns)
    bot.db_connector.execute(f'create table if not exists {table_name}  ("trade_id" integer primary key autoincrement, {columns_names})')
    loop = asyncio.get_event_loop()
    bot.repeat_action(action_name='update_recent_trades', event_loop=loop, duration=duration, interval=interval, table_name=table_name, api_url=api_url, size=batch_size, pair=pair)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--api_url',
        type=str,
        default='https://api.kraken.com',
        help='Kraken domain name for api access.',
    )
    parser.add_argument(
        '--db_name',
        type=str,
        help='Database name to which the bot has access to.',
    )
    parser.add_argument(
        '--table_name',
        type=str,
        default='recent_trades',
        help='The name of the table with recent trades.',
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=1000,
        help='The size of the latest batch of transactions',
    )
    parser.add_argument(
        '--pair',
        type=str,
        default='XBTUSD',
        help='The name of tradable asset pair to get data for.',
    )
    parser.add_argument(
        '--duration',
        type=float,
        default=3600,
        help='The time duration of actions repeating.',
    )
    parser.add_argument(
        '--interval',
        type=float,
        default=10,
        help='Time interval for actions repeating.',
    )
    args = parser.parse_args()
    try:
        run_bot(**vars(args))
    except Exception as e:
        raise e
