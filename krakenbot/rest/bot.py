from typing import Any, Optional, Sequence
import requests
from requests.exceptions import HTTPError


class KrakenBot:

    def __init__(self, api_key: Optional[str] = None, api_sec: Optional[str] = None) -> None:
        self.api_key = api_key
        self.api_sec = api_sec

    def recent_trades(self, size: int = 1000, pair: str = 'XBTUSD') -> Sequence[Any]:
        """Returns the last n trades (1000 by default).

        Args:
            size (int): The batch size of trades.

        Returns:
            Sequence[Any]: Sequence containing the last n trades
        """

        try:
            response = requests.get(f'https://api.kraken.com/0/public/Trades?pair={pair}').json()
            error = response['error']
            if error:
                return error
            result = response['result']
            pair_name = list(result.keys())[0]
            return result[pair_name][0:size]

        except HTTPError as http_error:
            print(f'HTTP error occured: {http_error}')
            raise
