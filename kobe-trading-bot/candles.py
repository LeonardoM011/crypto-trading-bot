# Created by Robert N. 030715
# Updated 031115
# Candle labels
# Source: tradingview.com
import sys
import math
sys.path.insert(1, "../deps/binance")
from binance.client import Client

from fun import *

def convert_candles(candles, num):
    list = []
    for item in candles[:-5:-1]:
        list.append(float(item[num]))
    if not list:
        output.print_failed("List is empty.")
        assert False
    return list

def flip_side(side):
    if side == Client.SIDE_BUY:
        return Client.SIDE_SELL
    if side == Client.SIDE_BUY:
        return Client.SIDE_SELL

def get_side(candle_info):
    for item in candle_info:
        if item['trend'] == 'upwards':
            return Client.SIDE_BUY
        elif item['trend'] == 'downwards':
            return Client.SIDE_SELL
    return None

def get_candle_info(candles, doji_size=0.05):
    info = []
    doji_size = float(max(0.01, doji_size))
    #study(title = "Candles", overlay = true)
    #DojiSize = input(0.05, minval=0.01, title="Doji size")

    open = convert_candles(candles, 1)
    high = convert_candles(candles, 2)
    low = convert_candles(candles, 3)
    close = convert_candles(candles, 4)

    if abs(open[0] - close[0]) <= (high[0] - low[0]) * doji_size:
        info.append({ 'name': 'Doji', 'color': 'white', 'trend': 'neutral' })
    #data=(abs(open - close) <= (high - low) * DojiSize)
    #plotchar(data, title="Doji", text='Doji', color=white)

    if close[2] > open[2] and min(open[1], close[1]) > close[2] and open[0] < min(open[1], close[1]) and close[0] < open[0]:
        info.append({ 'name': 'Evening Star', 'color': 'red', 'trend': 'downwards' })
    #data2=(close[2] > open[2] and min(open[1], close[1]) > close[2] and open < min(open[1], close[1]) and close < open )
    #plotshape(data2, title= "Evening Star", color=red, style=shape.arrowdown, text="Evening\nStar")

    if close[2] < open[2] and max(open[1], close[1]) < close[2] and open[0] > max(open[1], close[1]) and close[0] > open[0]:
        info.append({ 'name': 'Morning Star', 'color': 'lime', 'trend': 'upwards' })
    #data3=(close[2] < open[2] and max(open[1], close[1]) < close[2] and open > max(open[1], close[1]) and close > open )
    #plotshape(data3,  title= "Morning Star", location=location.belowbar, color=lime, style=shape.arrowup, text="Morning\nStar")

    if open[1] < close[1] and open[0] > close[1] and high[0] - max(open[0], close[0]) >= abs(open[0] - close[0]) * 3 and min(close[0], open[0]) - low[0] <= abs(open[0] - close[0]):
        info.append({ 'name': 'Morning Star', 'color': 'lime', 'trend': 'upwards' })
    #data4=(open[1] < close[1] and open > close[1] and high - max(open, close) >= abs(open - close) * 3 and min(close, open) - low <= abs(open - close))
    #plotshape(data4, title= "Shooting Star", color=red, style=shape.arrowdown, text="Shooting\nStar")

    if ((high[0] - low[0]) > 3 * (open[0] - close[0])) and ((close[0] - low[0]) / (0.001 + high[0] - low[0]) > 0.6) and ((open[0] - low[0]) / (0.001 + high[0] - low[0]) > 0.6):
        info.append({ 'name': 'Hammer', 'color': 'white', 'trend': 'neutral' })
    #data5=(((high - low)>3*(open -close)) and  ((close - low)/(.001 + high - low) > 0.6) and ((open - low)/(.001 + high - low) > 0.6))
    #plotshape(data5, title= "Hammer", location=location.belowbar, color=white, style=shape.diamond, text="H")

    if ((high[0] - low[0]) > 3 * (open[0] - close[0])) and ((high[0] - close[0]) / (0.001 + high[0] - low[0]) > 0.6) and ((high[0] - open[0]) / (0.001 + high[0] - low[0]) > 0.06):
        info.append({ 'name': 'Inverted Hammer', 'color': 'white', 'trend': 'neutral' })
    #data5b=(((high - low)>3*(open -close)) and  ((high - close)/(.001 + high - low) > 0.6) and ((high - open)/(.001 + high - low) > 0.6))
    #plotshape(data5b, title= "Inverted Hammer", location=location.belowbar, color=white, style=shape.diamond, text="IH")

    if close[1] > open[1] and open[0] > close[0] and open[0] <= close[1] and open[1] <= close[0] and open[0] - close[0] < close[1] - open[1]:
        info.append({ 'name': 'Bearish Harami', 'color': 'red', 'trend': 'downwards' })
    #data6=(close[1] > open[1] and open > close and open <= close[1] and open[1] <= close and open - close < close[1] - open[1] )
    #plotshape(data6, title= "Bearish Harami",  color=red, style=shape.arrowdown, text="Bearish\nHarami")

    if open[1] > close[1] and close[0] > open[0] and close[0] <= open[1] and close[1] <= open[0] and close[0] - open[0] < open[1] - close[1]:
        info.append({ 'name': 'Bullish Harami', 'color': 'lime', 'trend': 'upwards' })
    #data7=(open[1] > close[1] and close > open and close <= open[1] and close[1] <= open and close - open < open[1] - close[1] )
    #plotshape(data7,  title= "Bullish Harami", location=location.belowbar, color=lime, style=shape.arrowup, text="Bullish\nHarami")

    if close[1] > open[1] and open[0] > close[0] and open[0] >= close[1] and open[1] >= close[0] and open[0] - close[0] > close[1] - open[1]:
        info.append({ 'name': 'Bearish Engulfing', 'color': 'red', 'trend': 'downwards' })
    #data8=(close[1] > open[1] and open > close and open >= close[1] and open[1] >= close and open - close > close[1] - open[1] )
    #plotshape(data8,  title= "Bearish Engulfing", color=red, style=shape.arrowdown, text="Bearish\nEngulfing")

    if open[1] > close[1] and close[0] > open[0] and close[0] >= open[1] and close[1] >= open[0] and close[0] - open[0] > open[1] - close[1]:
        info.append({ 'name': 'Bullish Engulfing', 'color': 'lime', 'trend': 'upwards' })
    #data9=(open[1] > close[1] and close > open and close >= open[1] and close[1] >= open and close - open > open[1] - close[1] )
    #plotshape(data9, title= "Bullish Engulfing", location=location.belowbar, color=lime, style=shape.arrowup, text="Bullish\nEngulfling")

    if close[1] < open[1] and open[0] < low[1] and close[0] > close[1] + ((open[1] - close[1])/2) and close[0] < open[1]:
        info.append({ 'name': 'Piercing Line', 'color': 'lime', 'trend': 'upwards' })
    #upper = highest(10)[1]
    #data10=(close[1] < open[1] and  open < low[1] and close > close[1] + ((open[1] - close[1])/2) and close < open[1])
    #plotshape(data10, title= "Piercing Line", location=location.belowbar, color=lime, style=shape.arrowup, text="Piercing\nLine")

    # TODO: Do this candle
    #if low[0] == open[0] and open[0] < lower[0] and open[0] < close[0] and close[0] > ((high[1] - low[1]) / 2) + low[1]:
    #    info.append({ 'name': 'Bullish Belt', 'color': 'lime', 'trend': 'upwards' })
    #lower = lowest(10)[1]
    #data11=(low == open and  open < lower and open < close and close > ((high[1] - low[1]) / 2) + low[1])
    #plotshape(data11, title= "Bullish Belt", location=location.belowbar, color=lime, style=shape.arrowup, text="Bullish\nBelt")

    if open[1] > close[1] and open[0] >= open[1] and close[0] > open[0]:
        info.append({ 'name': 'Bullish Kicker', 'color': 'lime', 'trend': 'upwards' })
    #data12=(open[1]>close[1] and open>=open[1] and close>open)
    #plotshape(data12, title= "Bullish Kicker", location=location.belowbar, color=lime, style=shape.arrowup, text="Bullish\nKicker")

    if open[1] < close[1] and open[0] <= open[1] and close[0] <= open[0]:
        info.append({ 'name': 'Bearish Kicker', 'color': 'red', 'trend': 'downwards' })
    #data13=(open[1]<close[1] and open<=open[1] and close<=open)
    #plotshape(data13, title= "Bearish Kicker", color=red, style=shape.arrowdown, text="Bearish\nKicker")

    if ((high[0] - low[0] > 4 * (open[0] - close[0])) and ((close[0] - low[0]) / (0.001 + high[0] - low[0]) >= 0.75) and ((open[0] - low[0]) / (0.001 + high[0] - low[0]) >= 0.75)) and high[1] < open[0] and high[2] < open[0]:
        info.append({ 'name': 'Hanging Man', 'color': 'red', 'trend': 'downwards' })
    #data14=(((high-low>4*(open-close))and((close-low)/(.001+high-low)>=0.75)and((open-low)/(.001+high-low)>=0.75)) and high[1] < open and high[2] < open)
    #plotshape(data14,  title= "Hanging Man", color=red, style=shape.arrowdown, text="Hanging\nMan")

    if (close[1] > open[1]) and (((close[1] + open[1]) / 2) > close[0]) and (open[0] > close[0]) and (open[0] > close[1]) and (close[0] > open[1]) and ((open[0] - close[0]) / (0.001 + (high[0] - low[0])) > 0.6):
        info.append({ 'name': 'Dark Cloud Cover', 'color': 'red', 'trend': 'downwards' })
    #data15=((close[1]>open[1])and(((close[1]+open[1])/2)>close)and(open>close)and(open>close[1])and(close>open[1])and((open-close)/(.001+(high-low))>0.6))
    #plotshape(data15, title= "Dark Cloud Cover", color=red, style=shape.arrowdown, text="Dark\nCloudCover")
    
    # Additional candlesticks (Made by LeonardoM011)
    if open[0] > close[0] and open[1] > close[1] and open[2] > close[2]:
        info.append({ 'name': 'Three Black Crows', 'color': 'red', 'trend': 'downwards' })
    
    if close[0] > open[0] and close[1] > open[1] and close[2] > open[2]:
        info.append({ 'name': 'Three White Soldiers', 'color': 'lime', 'trend': 'upwards' })

    return info
