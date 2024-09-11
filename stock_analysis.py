import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors

class Stock:
    def __init__(self, app):
        self.app = app
        self.df = None
        self.future_df = None
        self.figure = None
        self.canvas = None
        self.percent_change_today = None

    def load_stock_data(self, stock_name, period):
        stock_data = yf.Ticker(stock_name)
        self.df = stock_data.history(period=period)
        self.df['Date'] = self.df.index
        self.df.reset_index(drop=True, inplace=True)

        self.calculate_percent_change(stock_data)

    def calculate_percent_change(self, stock_data):
        previous_close = stock_data.info.get('previousClose')
        day_high = stock_data.info.get('dayHigh')
        day_low = stock_data.info.get('dayLow')  # Pentru scădere

        if previous_close and day_high and day_low:
            change_high = (day_high / previous_close - 1) * 100
            change_low = (day_low / previous_close - 1) * 100  # Calculați schimbarea minimă
            self.percent_change_today = change_high if change_high >= 0 else change_low
        else:
            self.percent_change_today = None

    def plot_prediction_graph(self):
        if self.df is None:
            return

        fig, ax = plt.subplots()

        ax.plot(self.df['Date'], self.df['Close'])

        if self.future_df is not None:
            ax.plot(self.future_df['Date'], self.future_df['Prediction'], label='Prediction', linestyle='--')

        ax.set_xlabel("Date")
        ax.set_ylabel("")
       

        if self.percent_change_today is not None:
            if self.percent_change_today >= 0:
                percent_change_label = f"+{self.percent_change_today:.2f}%"
                bbox_props = dict(facecolor='green', alpha=0.5)
            else:
                percent_change_label = f"{self.percent_change_today:.2f}%"
                bbox_props = dict(facecolor='red', alpha=0.5)

            ax.text(0.05, 0.95, percent_change_label, transform=ax.transAxes, fontsize=12,
                    verticalalignment='top', horizontalalignment='left', bbox=bbox_props)

        if 'Prediction' in ax.get_legend_handles_labels()[1]:
            ax.legend()

        if self.canvas is not None:
            self.canvas.get_tk_widget().pack_forget()

        self.figure = fig
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.app.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        mplcursors.cursor(self.figure.axes[0], hover=True)
