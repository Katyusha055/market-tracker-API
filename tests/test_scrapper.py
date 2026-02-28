import pytest
import requests
from program.scrapper import web_scrapper as ws


# fixture to neutralize sleep in all tests
@pytest.fixture(autouse=True)
def disable_sleep(monkeypatch):
    monkeypatch.setattr(ws.time, "sleep", lambda *_: None)


# testing the "happy path" or normal case (single page)
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
        return FakeResponse(FAKE_HTML)

    monkeypatch.setattr(ws.requests, "get", fake_get)

    result = ws.newegg_scrapper(total_pages=1)

    assert result == [{'description': 'RAM stick', 'price': '123', 'source': 'Newegg'}]


# testing the case where the connection goes wrong
def test_scrapper_2(monkeypatch):
    def fake_get(url, timeout):
        raise requests.exceptions.ConnectionError('No connection')

    monkeypatch.setattr(ws.requests, "get", fake_get)

    with pytest.raises(ConnectionError):
        ws.newegg_scrapper()


# testing invalid result of request (5 failed pages should raise)
def test_scrapper_3(monkeypatch):
    class FakeResponse:
        def __init__(self, status_code=200):
            self.status_code = status_code

    def fake_get(url, timeout):
        return FakeResponse(404)

    monkeypatch.setattr(ws.requests, "get", fake_get)

    with pytest.raises(ConnectionError):
        ws.newegg_scrapper()


# testing case where the data is incomplete
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
        return FakeResponse(FAKE_HTML)

    monkeypatch.setattr(ws.requests, "get", fake_get)

    with caplog.at_level("WARNING"):
        result = ws.newegg_scrapper(total_pages=1)

    assert result == []  # item has been skipped
    assert "does not have price and/or description" in caplog.text


# testing that total_pages works for custom value
# should call requests.get exactly total_pages times when total_pages <= 20
def test_scrapper_5(monkeypatch):
    calls = []
    FAKE_HTML = """
    <html><body>
      <div class='item-cell'>
        <div class='price-current'>50</div>
        <div class='item-title'>RAM A</div>
      </div>
    </body></html>
    """

    class FakeResponse:
        def __init__(self, text, status_code=200):
            self.text = text
            self.status_code = status_code

    def fake_get(url, timeout):
        calls.append(url)
        return FakeResponse(FAKE_HTML)

    monkeypatch.setattr(ws.requests, "get", fake_get)

    ws.newegg_scrapper(total_pages=3)

    assert len(calls) == 3
    assert calls == [
        'https://www.newegg.com/p/pl?d=ram&page=1',
        'https://www.newegg.com/p/pl?d=ram&page=2',
        'https://www.newegg.com/p/pl?d=ram&page=3',
    ]


# testing that total_pages is capped to 20
# should not request more than 20 pages even if a bigger value is passed
def test_scrapper_6(monkeypatch):
    calls = []
    FAKE_HTML = """
    <html><body>
      <div class='item-cell'>
        <div class='price-current'>60</div>
        <div class='item-title'>RAM B</div>
      </div>
    </body></html>
    """

    class FakeResponse:
        def __init__(self, text, status_code=200):
            self.text = text
            self.status_code = status_code

    def fake_get(url, timeout):
        calls.append(url)
        return FakeResponse(FAKE_HTML)

    monkeypatch.setattr(ws.requests, "get", fake_get)

    ws.newegg_scrapper(total_pages=100)

    assert len(calls) == 20
    assert calls[0].endswith('page=1')
    assert calls[-1].endswith('page=20')


# testing pagination with 3 different html pages and recurrent extraction
# should aggregate all valid items from all pages
def test_scrapper_7(monkeypatch):
    page_html = {
        1: """
            <div class='item-cell'><div class='price-current'>101</div><div class='item-title'>RAM P1</div></div>
        """,
        2: """
            <div class='item-cell'><div class='price-current'>202</div><div class='item-title'>RAM P2</div></div>
        """,
        3: """
            <div class='item-cell'><div class='price-current'>303</div><div class='item-title'>RAM P3</div></div>
        """,
    }

    class FakeResponse:
        def __init__(self, text, status_code=200):
            self.text = f"<html><body>{text}</body></html>"
            self.status_code = status_code

    def fake_get(url, timeout):
        page = int(url.split('page=')[1])
        return FakeResponse(page_html[page])

    monkeypatch.setattr(ws.requests, "get", fake_get)

    result = ws.newegg_scrapper(total_pages=3)

    assert result == [
        {'description': 'RAM P1', 'price': '101', 'source': 'Newegg'},
        {'description': 'RAM P2', 'price': '202', 'source': 'Newegg'},
        {'description': 'RAM P3', 'price': '303', 'source': 'Newegg'},
    ]


# testing pagination where pages do not contain complete info
# should return empty list because all item-cells are missing description or price
def test_scrapper_8(monkeypatch):
    page_html = {
        1: """
            <div class='item-cell'><div class='item-title'>RAM no price</div></div>
        """,
        2: """
            <div class='item-cell'><div class='price-current'>777</div></div>
        """,
        3: """
            <div class='item-cell'><div class='item-title'>RAM missing</div></div>
        """,
    }

    class FakeResponse:
        def __init__(self, text, status_code=200):
            self.text = f"<html><body>{text}</body></html>"
            self.status_code = status_code

    def fake_get(url, timeout):
        page = int(url.split('page=')[1])
        return FakeResponse(page_html[page])

    monkeypatch.setattr(ws.requests, "get", fake_get)

    result = ws.newegg_scrapper(total_pages=3)

    assert result == []


# testing partial failure in 3-page pagination
# if one page fails, it should be discarded and scrape should continue with successful pages
def test_scrapper_9(monkeypatch):
    page_html = {
        1: """
            <div class='item-cell'><div class='price-current'>111</div><div class='item-title'>RAM OK 1</div></div>
        """,
        3: """
            <div class='item-cell'><div class='price-current'>333</div><div class='item-title'>RAM OK 3</div></div>
        """,
    }

    class FakeResponse:
        def __init__(self, text='', status_code=200):
            self.text = f"<html><body>{text}</body></html>"
            self.status_code = status_code

    def fake_get(url, timeout):
        page = int(url.split('page=')[1])
        if page == 2:
            return FakeResponse(status_code=500)
        return FakeResponse(page_html[page], status_code=200)

    monkeypatch.setattr(ws.requests, "get", fake_get)

    result = ws.newegg_scrapper(total_pages=3)

    assert result == [
        {'description': 'RAM OK 1', 'price': '111', 'source': 'Newegg'},
        {'description': 'RAM OK 3', 'price': '333', 'source': 'Newegg'},
    ]
