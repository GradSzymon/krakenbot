from typing import Any, Sequence
import requests
from requests.exceptions import HTTPError
from krakenbot.database.connector import DatabaseConnector

class KrakenBot:

    def __init__(self, connector: DatabaseConnector, api_url: str = 'https://api.kraken.com') -> None:
        self.api_url = api_url
        self.connector = connector

    def recent_trades(self, size: int = 1000, pair: str = 'XBTUSD') -> Sequence[Any]:
        """Returns the last n trades (1000 by default).

        Args:
            size (int): The batch size of trades.

        Returns:
            Sequence[Any]: Sequence containing the last n trades
        """

        try:
            response = requests.get(f'{self.api_url}/0/public/Trades?pair={pair}').json()
            error = response['error']
            if error:
                return error
            result = response['result']
            pair_name = list(result.keys())[0]
            return result[pair_name][0:size]

        except HTTPError as http_error:
            print(f'HTTP error occured: {http_error}')
            raise
