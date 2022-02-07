import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('./fcc-forum-pageviews.csv')

# Clean data
df.date = pd.to_datetime(df.date)
df.set_index('date', inplace=True)
c1 = df.value <= df.value.quantile(0.975)
c2 = df.value >= df.value.quantile(0.025)
df = df[(c1 & c2)]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.lineplot(data=df, palette=['r'], linewidth=2.5, legend=False)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df.index.year
    df_bar['month_name'] = df.index.strftime('%B')

    df_bar = (
        df_bar.groupby(['year', 'month_name'], 
        as_index=False, observed=True)
        .agg('mean')
    )

    months = (
        pd.date_range('2020-01', '2020-12', freq='MS')
        .strftime('%B')
        .tolist()
    )

    # Draw bar plot
    fig = plt.figure(figsize=(14,6))

    sns.barplot(
        data=df_bar,
        x="year",
        y="value",
        hue="month_name",
        hue_order=months,
    )

    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', loc='upper left')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    months = (
        pd.date_range('2020-01', '2020-12', freq='MS')
        .strftime('%b')
        .tolist()
    )

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sns.boxplot(data=df_box, 
                x="year", 
                y="value",
                ax=axes[0]
                )
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(data=df_box, x="month", y="value", order=months, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
