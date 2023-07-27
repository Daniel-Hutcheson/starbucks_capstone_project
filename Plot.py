import pandas as pd
import plotly.express as px


class Plot:
    '''This class has the sole purpose to generate nice plots for the blog post using Plotly.'''

    def __init__(self, data) -> None:
        self.data = data

        self.prep_data()

    def prep_data(self):
        self.anon_df = self.data[data.age.isna(
        ) | data.gender.isna() | data.income.isna()]
        self.doxed_df = self.data[data.age.notna(
        ) | data.gender.notna() | data.income.notna()]

    def generate_plots_for_blog_post(self):
        self.anon_doxed_comp()

    def anon_doxed_comp(self):
        anon_sum = self.anon_df[['offer_received','offer_viewed','offer_completed']].sum()
        anon_sum_df = pd.DataFrame({'Values': anon_sum.index, 'Count': anon_sum.values})

        anon_doxed_comp = px.histogram(
            data_frame=anon_sum_df,
            x='Values',
            y='Count',
        )

        anon_doxed_comp.show()


if __name__ == '__main__':

    data = pd.read_csv(r'data/data_clean.csv')
    Plots = Plot(data)
    Plots.generate_plots_for_blog_post()
    print('Done')
