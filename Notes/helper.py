import pandas as pd 

color_scheme = {
    'index': '#B6B2CF',
    'etf': '#2D3ECF',
    'tracking_error': '#6F91DE',
    'df_header': 'silver',
    'df_value': 'white',
    'df_line': 'silver',
    'heatmap_colorscale': [(0, '#6F91DE'), (0.5, 'grey'), (1, 'red')],
    'background_label': '#9dbdd5',
    'low_value': '#B6B2CF',
    'high_value': '#2D3ECF',
    'y_axis_2_text_color': 'grey',
    'shadow': 'rgba(0, 0, 0, 0.75)',
    'major_line': '#2D3ECF',
    'minor_line': '#B6B2CF',
    'main_line': 'black'}


def generate_config():
    return {'showLink': False, 'displayModeBar': False, 'showAxisRangeEntryBoxes': True}


def convert_quotemedia_to_yformat(ticker_data):
    # remove a column
    ticker_data.drop(columns=['Unnamed: 0'],inplace=True)

    # Set 'date' as the index
    ticker_data.set_index('date', inplace=True)
    # Pivot the DataFrame
    ticker_data = ticker_data.pivot_table(index=ticker_data.index, columns='ticker')

    # Flatten the MultiIndex columns
    ticker_data.columns = pd.MultiIndex.from_product([ticker_data.columns.levels[1], ticker_data.columns.levels[0]])

    return ticker_data