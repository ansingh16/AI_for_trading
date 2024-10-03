import numpy as np
import pandas as pd 
from zipline.assets._assets import Equity  # Required for USEquityPricing
from zipline.pipeline.data import USEquityPricing
from zipline.pipeline.classifiers import Classifier
from zipline.pipeline.engine import SimplePipelineEngine
from zipline.pipeline.loaders import USEquityPricingLoader
from zipline.utils.numpy_utils import int64_dtype
from zipline.data.bundles import register, yahoo_NYSE
import zipline.data.bundles as bundles



class PricingLoader(object):
    def __init__(self, bundle_data):
        self.loader = USEquityPricingLoader(
            bundle_data.equity_daily_bar_reader,
            bundle_data.adjustment_reader)

    def get_loader(self, column):
        if column not in USEquityPricing.columns:
            raise Exception('Column not in USEquityPricing')
        return self.loader


class Sector(Classifier):
    dtype = int64_dtype  # Assuming sector IDs are integers
    window_length = 0
    inputs = ()
    missing_value = -1  # Use -1 for missing sectors

    def __init__(self):

        register(
        'yahoo_NYSE',
        yahoo_NYSE.yahoo_NYSE(
            tframes=["daily"],
            csvdir="/home/ankit/AI_for_trading/Data/data/eod-quotemedia/"
            )
        )

        bundle_data = bundles.load('yahoo_NYSE')

        asset_finder = bundle_data.asset_finder

        # Load the CSV with stock symbols and sector IDs
        self.sector_data = pd.read_csv('../../Data/sectors.csv').set_index('ticker')['sector'].to_dict()

       # Create a reverse mapping from SIDs to symbols
        self.symbol_to_sector = self.sector_data
        self.asset_finder = asset_finder

    def _compute(self, arrays, dates, assets, mask):

        
        # Check the type of assets
        # Convert zipline assets (Asset objects) to stock symbols
        symbols = [self.asset_finder.retrieve_asset(asset).symbol for asset in assets]
       

        # Map symbols to their sector IDs using the CSV data
        sectors = np.array([self.sector_data.get(symbol, self.missing_value) for symbol in symbols])


        # Return sectors where mask is True, otherwise return missing_value
        return np.where(mask, sectors, self.missing_value)



def build_pipeline_engine(bundle_data, trading_calendar):
    pricing_loader = PricingLoader(bundle_data)

    engine = SimplePipelineEngine(
        get_loader=pricing_loader.get_loader,
        calendar=trading_calendar.all_sessions,
        asset_finder=bundle_data.asset_finder)

    return engine


def get_factor_exposures(factor_betas, weights):
    return factor_betas.loc[weights.index].T.dot(weights)
