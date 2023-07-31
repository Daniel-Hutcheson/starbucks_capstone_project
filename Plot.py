import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
        anon_sum = self.anon_df[['offer_received',
                                 'offer_viewed', 'offer_completed']].sum()
        doxed_sum = self.doxed_df[['offer_received',
                                   'offer_viewed', 'offer_completed']].sum()

        anon_sum_df = pd.DataFrame(
            {'values': anon_sum.index, 'anon_counts': anon_sum.values})
        doxed_sum_df = pd.DataFrame(
            {'values': doxed_sum.index, 'doxed_counts': doxed_sum.values})

        anon_doxed_df = pd.merge(anon_sum_df, doxed_sum_df, on=['values'])

        # Create the grouped bar chart with two y-axes
        anon_doxed_comp = make_subplots(specs=[[{"secondary_y": True}]])

        anon_doxed_comp.add_trace(
            go.Bar(
                x=anon_doxed_df['values'], 
                y=anon_doxed_df['anon_counts'], 
                name='anon_counts',
                width=0.3,
                offset=-0.3,
                ),
            secondary_y=False,
        )

        anon_doxed_comp.add_trace(
            go.Bar(
                x=anon_doxed_df['values'], 
                y=anon_doxed_df['doxed_counts'], 
                name='doxed_counts',
                width=0.3,
                offset=0,
                ),
            secondary_y=True,
        )

        anon_doxed_comp.update_layout(
            title='Offer responses: Anon customers vs. Doxed customers',
            xaxis_title='Offer Responses',
            yaxis_title='Anon Counts',
            yaxis2_title='Doxed Counts',
            template='seaborn',
            legend=dict(
                x=0.8,
                y=0.95,
                bgcolor='rgba(0, 0, 0, 0)',
                bordercolor='rgba(0, 0, 0, 0.5)',
                borderwidth=1,
            ),
        )

        # Set y-axis ranges to align the bars properly
        anon_doxed_comp.update_yaxes(
            range=[0, max(anon_doxed_df['anon_counts']) + 10000], secondary_y=False)
        anon_doxed_comp.update_yaxes(
            range=[0, max(anon_doxed_df['doxed_counts']) + 10000], secondary_y=True)
                
        label_mapping = {
            'offer_received': 'Offer received',
            'offer_viewed': 'Offer viewed',
            'offer_completed': 'Offer completed'
        }

        anon_doxed_comp.update_xaxes(
            ticktext=[label_mapping[label] for label in label_mapping.keys()],
        )

        anon_doxed_comp.show()

        print('This is for a breakpoint only.')


if __name__ == '__main__':

    data = pd.read_csv(r'data/data_clean.csv')
    Plots = Plot(data)
    Plots.generate_plots_for_blog_post()
    print('Done')
