import pandas as pd
import numpy as np



class stratergy:
    def __init__(self, data):
        self.data = data
        self.data['SMA'] = self.data['Close'].rolling(window=20).mean()
        self.data['std'] = self.data['Close'].rolling(window=20).std()
        self.data['upper'] = self.data['SMA'] + (self.data['std'] * 2)
        self.data['lower'] = self.data['SMA'] - (self.data['std'] * 2)
        self.data['position'] = None
        self.data['position'] = np.where(self.data['Close'] > self.data['upper'], -1, np.nan)
        self.data['position'] = np.where(self.data['Close'] < self.data['lower'], 1, self.data['position'])
        self.data['position'] = np.where(self.data['Close'] < self.data['SMA'], 1, self.data['position'])
        self.data['position'] = np.where(self.data['Close'] > self.data['SMA'], -1, self.data['position'])
        self.data['position'] = self.data['position'].ffill()
        self.data['strategy'] = self.data['position'].shift(1) * self.data['returns']
        self.data['creturns'] = self.data['returns'].cumsum().apply(np.exp)
        self.data['cstrategy'] = self.data['strategy'].cumsum().apply(np.exp)
        self.data.dropna(inplace=True)
        print(self.data.head())


def get_yesterday_high_low(data):
    yesterday = data.iloc[-2]  # Second-to-last row is "yesterday"
    yesterday_high = yesterday['High']
    yesterday_low = yesterday['Low']
    return yesterday_high, yesterday_low


def batman_pattern(data):
    # Get last 3 candles to check for Batman pattern
    last_three = data.iloc[-3:]

    # Separate the 3 candles
    first_candle, second_candle, third_candle = last_three.iloc[0], last_three.iloc[1], last_three.iloc[2]

    # Define parameters for what constitutes a "long" and "short" candle
    long_candle_threshold = 0.01  # This could be adjusted based on currency volatility
    short_candle_threshold = 0.005

    # Check for the Batman pattern structure
    if (
        abs(first_candle['Open'] - first_candle['Close']) > long_candle_threshold
        and abs(third_candle['Open'] - third_candle['Close']) > long_candle_threshold
        and abs(second_candle['Open'] - second_candle['Close']) < short_candle_threshold
    ):
        # Check that highs and lows of the first and third candles are relatively symmetric
        first_third_high_diff = abs(first_candle['High'] - third_candle['High'])
        first_third_low_diff = abs(first_candle['Low'] - third_candle['Low'])

        if first_third_high_diff < long_candle_threshold and first_third_low_diff < long_candle_threshold:
            return True  # Batman pattern detected
    return False  # No Batman pattern



