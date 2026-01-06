import pytest
import requests
from program import web_scrapper as ws

#testing the "happy path" or normal case
def test_scrapper_1(monkeypatch):
    FAKE_HTML = """
    <html>
      <body>
        <div class='item-cell'>
          <div class='price-current'>123</div>
          <div class='item-title'>RAM stick</div>
        </div>
      </body>
    </html>
    """

    class FakeResponse:
        def __init__(self, text, status_code=200):
            self.text = text
            self.status_code = status_code

    def fake_get(url, timeout):
        time = timeout
        return FakeResponse(FAKE_HTML)

    monkeypatch.setattr(ws.requests, "get", fake_get)

    result = ws.newegg_scrapper()

    assert result == [{'description':'RAM stick', 'price':'123'}]

#testing the case where the connection goes wrong
def test_scrapper_2(monkeypatch):
    def fake_get(url, timeout):
        raise requests.exceptions.ConnectionError('No connection')

    monkeypatch.setattr(ws.requests, "get", fake_get)

    with pytest.raises(ConnectionError):
        ws.newegg_scrapper()

#testing invalid result of request
def test_scrapper_3(monkeypatch):
    class FakeResponse:
        def __init__(self, status_code=200):
            self.status_code = status_code

    def fake_get(url, timeout):
        time = timeout
        return FakeResponse(404)

    monkeypatch.setattr(ws.requests, "get", fake_get)

    with pytest.raises(ConnectionError):
        ws.newegg_scrapper()

#testing case where the data is incomplete
def test_scrapper_4(monkeypatch, caplog):
    FAKE_HTML = """
    <html>
      <body>
        <div class="item-cell">
          <div class="item-title">Broken RAM</div>
        </div>
      </body>
    </html>
    """

    class FakeResponse:
        def __init__(self, text, status_code=200):
            self.text = text
            self.status_code = status_code

    def fake_get(url, timeout):
        timeout = timeout
        return FakeResponse(FAKE_HTML)

    monkeypatch.setattr(ws.requests, "get", fake_get)

    with caplog.at_level("WARNING"):
        result = ws.newegg_scrapper()

    assert result == []  # item has been skipped
    assert "does not have price and/or description" in caplog.text
