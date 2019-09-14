from flask import render_template, jsonify
from app import app
import random
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import datetime as datetime
import numpy as np

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import os


def saveplot(filename, extension):
    strFile = filename + '.' + extension
    if os.path.isfile(strFile):
        os.remove(strFile)   # Opt.: os.system("rm "+strFile)
        plt.savefig(strFile)
    plt.savefig(strFile)

data = pd.read_csv("DIS.csv")
data['Date'] = pd.to_datetime(data['Date']).dt.date
#data = data.set_index('Date')

data90 = data[len(data)-90:]

preds_d1 = pd.read_csv("preds_d1.csv")
preds_d1['Date'] = pd.to_datetime(preds_d1['Date']).dt.date
#preds_dt = preds_d1.set_index('Date')


preds = pd.read_csv("preds.csv")
preds['Date'] = pd.to_datetime(preds['Date']).dt.date
#preds = preds.set_index('Date')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/dif1.png')
def dif_png():
    fig = create_dif1()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_dif1():
    d1 = plt.figure(1)

    fig, ax = plt.subplots()
    ax.plot(preds_d1['Date'], preds_d1['Adj Close'], label='close')
    ax.plot(preds_d1['Date'], preds_d1['reg'], label='reg')
    ax.plot(preds_d1['Date'], preds_d1['krr'], label='krr')
    ax.plot(preds_d1['Date'], preds_d1['mlp'], label='mlp')

    months = mdates.MonthLocator()   # every month
    mdays = mdates.DayLocator(bymonthday=range(1, 32))  # every day
    months_fmt = mdates.DateFormatter('%Y-%m-%d')

    # format the ticks
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(months_fmt)
    ax.xaxis.set_minor_locator(mdays)

    # round to nearest years.
    datemin = np.datetime64(np.amin(preds_d1['Date']), 'D')
    datemax = np.datetime64(np.amax(preds_d1['Date']), 'D')
    ax.set_xlim(datemin, datemax)

    # format the coords message box
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = lambda x: '$%1.2f' % x  # format the price.
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)

    #d1.show()
    saveplot('dif1', 'png')
    return fig

@app.route('/price.png')
def price_png():
    fig = create_price()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_price():
    #plt.clf()

    pr = plt.figure(2)

    fig, ax = plt.subplots()
    ax.plot(preds['Date'], preds['Adj Close'], label='close')
    ax.plot(preds['Date'], preds['reg'], label='reg')
    ax.plot(preds['Date'], preds['krr'], label='krr')
    ax.plot(preds['Date'], preds['mlp'], label='mlp')

    months = mdates.MonthLocator()   # every month
    mdays = mdates.DayLocator(bymonthday=range(1, 32))  # every day
    months_fmt = mdates.DateFormatter('%Y-%m-%d')

    # format the ticks
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(months_fmt)
    ax.xaxis.set_minor_locator(mdays)

    # round to nearest years.
    datemin = np.datetime64(np.amin(preds['Date']), 'D')
    datemax = np.datetime64(np.amax(preds['Date']), 'D')
    ax.set_xlim(datemin, datemax)

    # format the coords message box
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = lambda x: '$%1.2f' % x  # format the price.
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)

    #pr.show()

    saveplot('price', 'png')
    return fig