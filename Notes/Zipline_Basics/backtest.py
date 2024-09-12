import pandas as pd
from zipline.api import order, record, symbol, schedule_function, attach_pipeline, pipeline_output,order_target_percent
from zipline.utils.events import date_rules, time_rules
from zipline import run_algorithm
from zipline.data.bundles import register
from zipline.utils.calendar_utils import get_calendar
from zipline.utils.events import date_rules, time_rules
from zipline.utils.cli import maybe_show_progress
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities
from zipline.pipeline.factors import AverageDollarVolume
from zipline.pipeline import Pipeline
import pyfolio as pf
import pytz

from datetime import datetime

# Define your trading algorithm
def initialize(context):
    context.asset = symbol('AAPL')
    
    context.index_average_window = 100

def handle_data(context, data):
    # Get the average dollar volume for the index
    equities_hist = data.history(context.asset, 'close', context.index_average_window, '1d')
    
    if equities_hist[-1]> equities_hist.mean():
        order_target_percent(context.asset, 1)
    else:
        order_target_percent(context.asset, 0)


def analyse(context,perf):
    returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(perf)

    pf.create_simple_tear_sheet(returns)


# Define the start and end dates for the backtest
start = datetime(2014, 5, 1, 0, 0, 0, 0,tzinfo=pytz.UTC)
end = datetime(2016, 5, 1, 0, 0, 0, 0,tzinfo=pytz.UTC)

# Register the custom data bundle
# Run the backtest
data = run_algorithm(
    start=start,
    end=end,
    initialize=initialize,
    analyse=analyse,
    handle_data=handle_data,
    bundle='yahoo_NYSE',
    trading_frequency='daily',
    capital_base=10000,
)

# # Print the results
# print(data.head())
