"""
API for S&P 500 data
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class SMAPI:
    def __init__(self):
        self.sp500 = None
        self.clean_data = None

    def load_data(self, filename):
        # load csv file
        self.sp500 = pd.read_csv(filename)
        self._clean_data()

    def _clean_data(self):
        # remove rows with missing data
        self.clean_data = self.sp500.dropna(subset=['Revenuegrowth', 'Ebitda']).copy()

        # convert to billions
        self.clean_data['Ebitda_B'] = self.clean_data['Ebitda'] / 1e9
        self.clean_data['Marketcap_B'] = self.clean_data['Marketcap'] / 1e9

        # revenue growth as percentage
        self.clean_data['Rev_Growth_Pct'] = self.clean_data['Revenuegrowth'] * 100

    def get_sectors(self):
        # return list of sectors
        sectors = self.clean_data['Sector'].dropna().unique()
        return sorted(sectors.tolist())

    def filter_data(self, sectors=None, min_marketcap=0, max_marketcap=5000,
                    min_employees=0, max_employees=1000000):
        # filter based on selections
        filtered = self.clean_data.copy()

        # filter by sector
        if sectors and len(sectors) > 0:
            filtered = filtered[filtered['Sector'].isin(sectors)]

        # filter by market cap
        filtered = filtered[
            (filtered['Marketcap_B'] >= min_marketcap) &
            (filtered['Marketcap_B'] <= max_marketcap)
        ]

        # filter by employees
        filtered = filtered[
            (filtered['Fulltimeemployees'] >= min_employees) &
            (filtered['Fulltimeemployees'] <= max_employees)
        ]

        return filtered

    def make_scatter(self, filtered_data, width=1200, height=600):
        # scatter plot of revenue growth vs ebitda
        fig = px.scatter(
            filtered_data,
            x='Ebitda_B',
            y='Rev_Growth_Pct',
            color='Sector',
            size='Marketcap_B',
            hover_data={
                'Shortname': True,
                'Ebitda_B': ':.2f',
                'Rev_Growth_Pct': ':.2f',
                'Marketcap_B': ':.2f',
                'Sector': True,
                'Industry': True
            },
            labels={
                'Ebitda_B': 'EBITDA (Billions)',
                'Rev_Growth_Pct': 'Revenue Growth (%)',
                'Marketcap_B': 'Market Cap (Billions)'
            },
            title='Revenue Growth vs EBITDA',
            width=width,
            height=height
        )

        fig.update_layout(template='plotly_white')
        return fig

    def make_sector_chart(self, filtered_data, width=1200, height=500):
        # bar chart by sector
        sector_stats = filtered_data.groupby('Sector').agg({
            'Rev_Growth_Pct': 'mean',
            'Ebitda_B': 'mean',
            'Symbol': 'count'
        }).reset_index()

        sector_stats.columns = ['Sector', 'Avg_Rev_Growth', 'Avg_EBITDA', 'Count']
        sector_stats = sector_stats.sort_values('Avg_Rev_Growth', ascending=False)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=sector_stats['Sector'],
            y=sector_stats['Avg_Rev_Growth'],
            name='Avg Revenue Growth (%)',
            marker_color='steelblue'
        ))

        fig.update_layout(
            title='Average Revenue Growth by Sector',
            xaxis_title='Sector',
            yaxis_title='Avg Revenue Growth (%)',
            template='plotly_white',
            width=width,
            height=height,
            xaxis_tickangle=-45
        )

        return fig

    def get_top_companies(self, filtered_data, n=20):
        # get top n companies by revenue growth
        top = filtered_data.nlargest(n, 'Rev_Growth_Pct')[
            ['Symbol', 'Shortname', 'Sector', 'Industry', 'Rev_Growth_Pct',
             'Ebitda_B', 'Marketcap_B']
        ].copy()

        top.columns = ['Symbol', 'Company', 'Sector', 'Industry',
                       'Revenue Growth (%)', 'EBITDA (B)', 'Market Cap (B)']

        # round numbers
        top['Revenue Growth (%)'] = top['Revenue Growth (%)'].round(2)
        top['EBITDA (B)'] = top['EBITDA (B)'].round(2)
        top['Market Cap (B)'] = top['Market Cap (B)'].round(2)

        return top


def main():
    api = SMAPI()
    api.load_data("data/sp500_companies.csv")

    filtered = api.filter_data(sectors=['Technology'], min_marketcap=100)
    print(f"Companies: {len(filtered)}")

    top = api.get_top_companies(filtered, n=10)
    print(top)


if __name__ == '__main__':
    main()