import pytest

from krakenbot.database.connectors.sqlite import SQLiteConnector
from krakenbot.rest.bot import KrakenBot


@pytest.fixture
def krakenbot(sqlite_connector):
    return KrakenBot(db_connector=sqlite_connector)


@pytest.mark.parametrize("pair", ["XBTUSD", "ETHUSD", "LUNAUSD"])
@pytest.mark.parametrize("size", [5, 10, 20])
def test_recent_trades(krakenbot, size, pair):
    recent_trades = krakenbot.recent_trades(size=size, pair=pair)
    assert recent_trades["status"] == 200
    assert recent_trades["error"] == ""
    assert len(recent_trades[pair]) == size
    for trade in recent_trades[pair]:
        assert len(trade) == 6


def test_recent_trades_bad_url(krakenbot):
    recent_trades_with_error = krakenbot.recent_trades(api_url="https://apikrakenbad.com")
    assert recent_trades_with_error["error"] == "Connection refused by the server"


def test_update_table(krakenbot):
    trades_before_update = krakenbot.db_connector.execute("select * from recent_trades")
    krakenbot.update_recent_trades("recent_trades", 3, "XBTUSD")
    trades_after_update = krakenbot.db_connector.execute("select * from recent_trades")
    for trade_before, trade_after in zip(trades_before_update, trades_after_update):
        assert trade_before[0:2] == trade_after[0:2]
        assert trade_before[2:] != trade_after[2:]
