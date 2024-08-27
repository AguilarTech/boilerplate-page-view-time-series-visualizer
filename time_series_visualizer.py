import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import calendar
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


print("Installed Seaborn version:", sns.__version__)
print("Installed numpy version:", np.__version__)

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')

# Clean data
df =  df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)


def draw_line_plot():

    fig, ax = plt.subplots(figsize=(12,6))

    # Draw line plot
    df.plot(ax=ax)

    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    df_bar['year'] = df.index.year
    df_bar['month'] = df.index.strftime('%B')  # Get month name
    df_bar['month_num'] = df.index.month  # Get month number for sorting

    # Draw bar plot

    # Group by year and month and calculate the average page views
    df_grouped = df_bar.groupby(['year', 'month', 'month_num'])['value'].mean().reset_index()

    # Sort by year and month number
    df_grouped.sort_values(by=['year', 'month_num'], inplace=True)
    
    # Pivot the table for plotting
    df_grouped = df_grouped.pivot(index='year', columns='month', values='value')

    months_full = [
    "January", "February", "March", "April", "May", 
    "June", "July", "August", "September", "October", 
    "November", "December"
    ]
    df_grouped = df_grouped[months_full]

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    df_grouped.plot(kind='bar', ax=ax)

    # Set the labels and title
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Daily Page Views for Each Month Grouped by Year')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    # Set up the matplotlib figure and axes
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 7))

    # Define custom color palettes
    year_palette = sns.color_palette("Set2", len(df_box['year'].unique()))
    month_palette = sns.color_palette("husl", len(df_box['month'].unique()))

    # Year-wise box plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0], palette=year_palette)
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')


    # Month-wise box plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=[calendar.month_abbr[i] for i in range(1, 13)], palette=month_palette)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')



    # Adjust layout for better fit
    plt.tight_layout()



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
