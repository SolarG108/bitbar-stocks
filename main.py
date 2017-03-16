#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
# -*- coding: utf-8 -*-
# <bitbar.title>Stock Ticker</bitbar.title>
# <bitbar.version>0.1.0</bitbar.version>
# <bitbar.author>Chase Ries</bitbar.author>
# <bitbar.author.github>chaseries</bitbar.author.github>
# <bitbar.desc>BitBar plugin for ticker data</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
import urllib.request as request
import json

colors = {
  'green': '#0CD560',
  'red': '#F60E39'
  }

def make_google_finance_url(ticker):
  url = 'https://google.com/finance?q='
  return url + ticker

class StockTicker:

  def __init__(self, ticker, current_price, delta):
    self.ticker = ticker
    self.current_price = current_price
    self.delta = delta

  def _ticker_display(self):
    '''
    General formatting for ticker display
    '''
    def append_color(base, color):
      return base + ' | color={} href={}'.format(color, make_google_finance_url(self.ticker))
    is_pos = True if self.delta >= 0 else False
    symbol = '+' if is_pos else ''
    color = colors['green'] if is_pos else colors['red']
    base = '{}  {}  {}{}'.format(self.ticker, self.current_price, symbol, self.delta)
    return append_color(base, color)

  def __repr__(self):
    return self._ticker_display()


def strip_google_bullshit(url):
  '''
  Google returns four leading characters to invalidate the JSON response
  in order to discourage developers from using it. This fixes that.
  '''
  return url[4:]

def request_to_utf8(url):
  bytes_resp = request.urlopen(url).read()
  return bytes_resp.decode('utf-8')

def request_tickers(tickers):
  base_url = 'http://finance.google.com/finance/info?client=ig&q='
  query = ','.join(tickers)
  resp = request_to_utf8(base_url + query)
  return json.loads(resp[4:])

if __name__ == '__main__':
  tickers = { '.DJI', '.INX', 'MSFT', 'AAPL', 'GOOGL', 'AMZN', 'BRK.B' }
  results = request_tickers(tickers)
  menu = [ StockTicker(res['t'], res['l'], float(res['c'])) for res in results]
  for item in menu:
    print(item)
