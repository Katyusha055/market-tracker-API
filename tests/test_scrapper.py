import pytest
from program import web_scrapper as ws

def test_scrapper(monkeypatch):
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
