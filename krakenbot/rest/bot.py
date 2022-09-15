import asyncio
import datetime
import logging
from typing import Callable, Dict, Optional

import requests
from requests.exceptions import HTTPError

from krakenbot.database.connectors.sqlite import SQLiteConnector

LOGGER = logging.getLogger(__name__)


class KrakenBot:
    def __init__(self, db_connector: SQLiteConnector, api_url: str = "https://api.kraken.com") -> None:
        self.api_url = api_url
        self.db_connector = db_connector
        self.actions: Dict[str, Callable] = {
            "recent_trades": self.recent_trades,
            "update_recent_trades": self.update_recent_trades,
        }

    def recent_trades(self, size: int = 1000, pair: str = "XBTUSD") -> dict:
        """Return the last n trades (1000 by default).

        Args:
            size (int): The batch size of trades.

        Returns:
            dict: Dict containing the last n trades for a given tradable asset pair.
        """

        try:
            response = requests.get(f"{self.api_url}/0/public/Trades?pair={pair}").json()
            error = response["error"]
            if error:
                return error
            result = response["result"]
            pair_name = list(result.keys())[0]
            trades = result[pair_name][0:size]
            return {f"{pair}": trades}

        except HTTPError:
            error = HTTPError("HTTP error occured")
            LOGGER.error(f"HTTP error occured: {error}")
            raise error

    def update_recent_trades(self, table_name: str, size: int = 1000, pair: str = "XBTUSD") -> None:
        """Update the table with recent trades

        Args:
            table_name (str): the recent trades table name in created database
            size (int): The batch (up to 1000 positions).
            pair (str): Tradable pair name. Defaults to 'XBTUSD'.
        """
        select_table = self.db_connector.execute(f"select * from {table_name}")
        recent_trades = self.recent_trades(size=size, pair=pair)
        trades = recent_trades[pair]
        data = [[idx, pair] + row for idx, row in enumerate(trades)]
        ids = [row[0] for row in select_table] if select_table else []  # type: ignore # noqa
        columns = [fields[1] for fields in self.db_connector.execute(f"PRAGMA table_info({table_name})")]  # type: ignore # noqa
        set_columns = [f'"{name}"=?' for name in columns]  # type: ignore # noqa

        for trade in data:
            value_id = trade[0]
            data = trade[1:]
            if value_id in ids:
                update_query = f'UPDATE {table_name} SET {", ".join(set_columns[1:])} WHERE trade_id={value_id} '
            else:
                update_query = f'INSERT INTO {table_name} VALUES ({value_id}, {", ".join(["?"]*len(data))})'
            self.db_connector.execute(query=update_query, data=[data], autoclose=False)
            LOGGER.info(
                f"Updated row: {self.db_connector.execute(f'select * from {table_name} where trade_id={value_id}')}"
            )

    async def __async__repeat_action(
        self, action_name: str, duration: float = 3600.0, interval: float = 10.0, *args, **kwargs
    ) -> None:
        try:
            cur_time = 0.0
            while cur_time < duration:
                action = self.actions.get(action_name, None)
                if action is None:
                    raise ValueError(
                        f"The action name {action_name} is invalid. Input one of possible actions: {self.actions}"
                    )
                _ = action(*args, **kwargs)
                LOGGER.info(f"The action {action_name} executed on date {datetime.datetime.now()}")
                await asyncio.sleep(interval)
                cur_time += interval
            LOGGER.info(
                f"The action {action_name} has been repeated every {interval} seconds for overall {duration} seconds."
            )
        except Exception as ex:
            LOGGER.error(f"The action exception {ex}")

    def repeat_action(
        self,
        action_name: str,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
        duration: float = 3600.0,
        interval: float = 10.0,
        *args,
        **kwargs,
    ) -> None:
        """Repeat the bot action asynchronously every interval for a given time.

        Args:
            action_name (str): the available action name to be executed
            event_loop (Optional[asyncio.AbstractEventLoop], optional): Optional existed event loop. Defaults to None.
            duration (float, optional): The overall duration time for action repeating. Defaults to 3600.0.
            interval (float, optional): Time interval what action is to be performed. Defaults to 10.0.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            if not event_loop:
                loop = asyncio.get_event_loop()
            else:
                loop = event_loop
        try:
            task = loop.create_task(
                self.__async__repeat_action(str(action_name), float(duration), float(interval), *args, **kwargs)
            )
            if not loop.is_running():
                loop.run_until_complete(task)
        except KeyboardInterrupt:
            loop.stop()
            loop.close()
