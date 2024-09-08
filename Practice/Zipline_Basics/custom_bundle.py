import os
import pandas as pd
from zipline.utils.calendars import get_calendar
from zipline.utils.events import date_rules, time_rules
from zipline.utils.cli import maybe_show_progress
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

def custom_ingest(environ,
                  asset_db_writer,
                  minute_bar_writer,
                  daily_bar_writer,
                  adjustment_writer,
                  calendar,
                  cache,
                  show_progress,
                  output_dir):
    # Define the directory containing your CSV files
    csvdir = '/home/ankit/AI_for_trading/Data/data/eod-quotemedia/daily'

    # Ingest the data using the csvdir_equities function
    csvdir_equities(
        csvdir,
        asset_db_writer,
        daily_bar_writer,
        adjustment_writer,
        calendar,
        show_progress,
        output_dir
    )

# Register the custom bundle
register(
    'eod-quotemedia',
    custom_ingest,
    calendar_name='NYSE',
    start_session = pd.Timestamp('2013-07-01'),
    end_session = pd.Timestamp('2017-06-30'),
    minutes_per_day=390
)
