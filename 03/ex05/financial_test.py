import pytest
import os
from financial import prepare_html, extract_info
import urllib.request
from urllib.error import URLError
@pytest.fixture


def setup_html():
    ticker_name = "MSFT"
    filename = "financial.html"
    prepare_html(filename, ticker_name)
    yield filename
    #os.remove(filename)

##Tests for prepare_html
def test_prepare_html(setup_html):
    filename = setup_html
    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0

def test_prepare_html_invalid_ticker():
    ticker_name = "INVALID"
    filename = "financial.html"
    with pytest.raises(ValueError, match="Incorrect URL!"):
        prepare_html(filename, ticker_name)


def test_prepare_html_network_error():
    ticker_name = "AAPL"
    filename = "financial.html"
    def urlopen_mock(request):
        raise URLError("Network error")

    original_urlopen = urllib.request.urlopen
    urllib.request.urlopen = urlopen_mock

    try:
        with pytest.raises(ValueError, match="Error! Network error"):
            prepare_html(filename, ticker_name)
    finally:
        urllib.request.urlopen = original_urlopen

    
###Tests for extract_info
def test_extract_info_total_revenue(setup_html):
    filename = setup_html
    input_field = "Total Revenue"
    result = extract_info(filename, input_field)
    assert isinstance(result, tuple)
    assert result[0] == "Total Revenue"
    assert len(result) > 1

def test_extract_info_invalid_field(setup_html):
    filename = setup_html
    input_field = "Invalid Field"
    with pytest.raises(ValueError, match="Incorrect requested field name!"):
        extract_info(filename, input_field)

def test_extract_info_empty_file():
    filename = "financial.html"
    input_field = "Total Revenue"
    with open(filename, "w") as f:
        f.write("")
    with pytest.raises(ValueError, match="Incorrect requested field name!"):
        extract_info(filename, input_field)


