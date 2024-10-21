import numpy as np
import pandas as pd
import time
import os
import matplotlib.pyplot as plt
import os
from zipline.data import bundles
import zipline.data.bundles as bundles
import pandas as pd
from zipline.data.bundles import register, yahoo_NYSE, csvdir
from zipline.pipeline import Pipeline
from zipline.pipeline.factors import AverageDollarVolume
from zipline.utils.calendar_utils import get_calendar
from zipline.pipeline import engine as pipeline_engine
from zipline.pipeline.loaders import USEquityPricingLoader
from zipline.pipeline.data import USEquityPricing
from zipline.pipeline.domain import US_EQUITIES
from zipline.data.data_portal import DataPortal

def get_pricing(data_portal, trading_calendar, assets, start_date, end_date, field='close'):
    end_dt = pd.Timestamp(end_date.strftime('%Y-%m-%d'))
    start_dt = pd.Timestamp(start_date.strftime('%Y-%m-%d'))

    end_loc = trading_calendar.closes.index.get_loc(end_dt)
    start_loc = trading_calendar.closes.index.get_loc(start_dt)

    return data_portal.get_history_window(
        assets=assets,
        end_dt=end_dt,
        bar_count=end_loc - start_loc,
        frequency='1d',
        field=field,
        data_frequency='daily')

def get_data_returns():

    # # Specify the bundle name
    # bundle_name = 'yahoo_NYSE'

    # start_session = pd.Timestamp('2013-07-01')  # Timezone-naive
    # end_session = pd.Timestamp('2017-06-30')    # Timezone-naive


    register(
        'yahoo_NYSE',
        yahoo_NYSE.yahoo_NYSE(
            tframes=["daily"],
            csvdir="/home/ankit/AI_for_trading/Data/data/eod-quotemedia/"
        )
    )

    bundle_data = bundles.load('yahoo_NYSE')
    ### Build pipeline engine

    def choose_price_loader(column):
        if column not in USEquityPricing.columns:
            print("Column not in USEquityPricing.columns")
        return pricing_loader

    universe = AverageDollarVolume(window_length=120).top(500) 
    trading_calendar = get_calendar('NYSE') 

    # Set the dataloader
    pricing_loader = USEquityPricingLoader(bundle_data.equity_daily_bar_reader, bundle_data.adjustment_reader,fx_reader=None)


    engine = pipeline_engine.SimplePipelineEngine(choose_price_loader,asset_finder=bundle_data.asset_finder)


    universe_end_date = pd.Timestamp('2017-01-06')

    universe_tickers = engine\
        .run_pipeline(
            Pipeline(screen=universe,domain=US_EQUITIES),
            universe_end_date,
            universe_end_date)\
        .index.get_level_values(1)\
        .values.tolist()
        

    data_portal = DataPortal(
        bundle_data.asset_finder,
        trading_calendar=trading_calendar,
        first_trading_day=bundle_data.equity_daily_bar_reader.first_trading_day,
        equity_minute_reader=None,
        equity_daily_reader=bundle_data.equity_daily_bar_reader,
        adjustment_reader=bundle_data.adjustment_reader)



    return get_pricing(
            data_portal,
            trading_calendar,
            universe_tickers,
            universe_end_date - pd.DateOffset(years=2),
            universe_end_date)\
        .pct_change()[1:].fillna(0) #convert prices into returns

   