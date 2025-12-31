"""
S&P 500 Dashboard
"""
import panel as pn
from smapi import SMAPI

pn.extension('plotly', 'tabulator')

# initialize API
api = SMAPI()
api.load_data("data/sp500_companies.csv")

# widgets
sector_select = pn.widgets.MultiChoice(
    name="Sectors",
    options=api.get_sectors(),
    value=['Technology', 'Healthcare'],
    solid=False
)

marketcap_range = pn.widgets.RangeSlider(
    name="Market Cap Range (Billions)",
    start=0,
    end=5000,
    value=(0, 5000),
    step=50
)

employee_range = pn.widgets.RangeSlider(
    name="Employee Range",
    start=0,
    end=1000000,
    value=(0, 1000000),
    step=10000
)

top_n = pn.widgets.IntSlider(
    name="Number of Companies",
    start=5,
    end=50,
    step=5,
    value=20
)

plot_width = pn.widgets.IntSlider(
    name="Width",
    start=800,
    end=1600,
    step=100,
    value=1200
)

plot_height = pn.widgets.IntSlider(
    name="Height",
    start=400,
    end=1000,
    step=100,
    value=600
)


# callback functions
def get_scatter(sectors, marketcap_range, employee_range, width, height):
    # make scatter plot
    filtered = api.filter_data(
        sectors=sectors,
        min_marketcap=marketcap_range[0],
        max_marketcap=marketcap_range[1],
        min_employees=employee_range[0],
        max_employees=employee_range[1]
    )

    if len(filtered) == 0:
        return pn.pane.Markdown("No data")

    fig = api.make_scatter(filtered, width=width, height=height)
    return pn.pane.Plotly(fig)


def get_sector_chart(sectors, marketcap_range, employee_range, width, height):
    # sector comparison
    filtered = api.filter_data(
        sectors=sectors,
        min_marketcap=marketcap_range[0],
        max_marketcap=marketcap_range[1],
        min_employees=employee_range[0],
        max_employees=employee_range[1]
    )

    if len(filtered) == 0:
        return pn.pane.Markdown("No data")

    fig = api.make_sector_chart(filtered, width=width, height=height)
    return pn.pane.Plotly(fig)


def get_table(sectors, marketcap_range, employee_range, n):
    # top performers table
    filtered = api.filter_data(
        sectors=sectors,
        min_marketcap=marketcap_range[0],
        max_marketcap=marketcap_range[1],
        min_employees=employee_range[0],
        max_employees=employee_range[1]
    )

    if len(filtered) == 0:
        return pn.pane.Markdown("No data")

    top = api.get_top_companies(filtered, n=n)
    # print(top)  # debugging
    table = pn.widgets.Tabulator(
        top,
        layout='fit_columns',
        selectable=False,
        page_size=20
    )
    return table


# bind callbacks
scatter_plot = pn.bind(get_scatter, sector_select, marketcap_range, employee_range, plot_width, plot_height)
sector_chart = pn.bind(get_sector_chart, sector_select, marketcap_range, employee_range, plot_width, plot_height)
top_table = pn.bind(get_table, sector_select, marketcap_range, employee_range, top_n)


# cards
card_width = 320

filter_card = pn.Card(
    pn.Column(
        sector_select,
        marketcap_range,
        employee_range
    ),
    title="Filters",
    width=card_width,
    collapsed=False
)

settings_card = pn.Card(
    pn.Column(
        top_n,
        plot_width,
        plot_height
    ),
    title="Settings",
    width=card_width,
    collapsed=True
)


# layout
layout = pn.template.FastListTemplate(
    title="S&P 500 Dashboard",
    sidebar=[
        filter_card,
        settings_card
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Scatter Plot", scatter_plot),
            ("Sector Analysis", sector_chart),
            ("Top Performers", top_table),
            active=0
        )
    ],
    header_background='#2E86AB'
).servable()

layout.show()