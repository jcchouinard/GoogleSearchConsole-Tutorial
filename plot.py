import matplotlib.pyplot as plt
import pandas as pd

from file_manip import date_to_index

def plot_data(df,grouping,data,figsize=(6,6)):
    df = df.groupby(['date',grouping])[data].nunique().reset_index()
    df = df.set_index(['date',grouping])[data].unstack()
    df = df.reset_index().rename_axis(None, axis=1)
    df = date_to_index(df,'date')
    print(f'Ploting {data} by {grouping}')
    df.plot(subplots=True,
            sharex=True,
            figsize=figsize,
            sharey=False)
    plt.title(f'Number of unique {data} by {grouping}')
    plt.xlabel('Date')
    plt.ylabel(data)
    plt.show()