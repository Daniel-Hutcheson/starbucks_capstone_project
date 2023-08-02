import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Plot:
    '''This class has the sole purpose to generate nice plots for the blog post using Plotly.'''

    def __init__(self, data) -> None:
        '''Initializes the object.'''
        self.data = data

        self.prep_data()

    def prep_data(self):
        '''This method preps the data for generating the plots.'''
        self.anon_df = self.data[data.age.isna(
        ) | data.gender.isna() | data.income.isna()]
        self.doxed_df = self.data[data.age.notna(
        ) | data.gender.notna() | data.income.notna()]

    def generate_plots_for_blog_post(self):
        '''This method calls all methods that generate the desired plots, so we just have to call this method to generate all of them at once.'''
        self.bar_anon_doxed_offer_comp()
        self.bar_anon_doxed_transaction_comp()
        self.hist_bogo_age_dist()
        self.hist_bogo_income_dist()
        self.hist_discount_age_dist()
        self.hist_discount_income_dist()

    def bar_anon_doxed_transaction_comp(self):
        '''This method generates a bar chart that compares the spending behavior of anon and doxed customers.'''

        anon_data = {
            'Transactions': self.anon_df.transaction.sum(),
            'Customer count': self.anon_df.shape[0],
        }
        doxed_data = {
            'Transactions': self.doxed_df.transaction.sum(),
            'Customer count': self.doxed_df.shape[0],
        }

        anon_df = pd.DataFrame.from_dict(anon_data, orient='index', columns=[
                                         'anon_counts']).reset_index()
        doxed_df = pd.DataFrame.from_dict(doxed_data, orient='index', columns=[
                                          'doxed_counts']).reset_index()
        anon_doxed_df = pd.merge(anon_df, doxed_df, on=['index'])
        anon_doxed_df = anon_doxed_df.iloc[[1, 0]].reset_index(drop=True)

        # Create the grouped bar chart with two y-axes
        anon_doxed_comp = make_subplots(specs=[[{"secondary_y": True}]])

        anon_doxed_comp.add_trace(
            go.Bar(
                x=anon_doxed_df['index'],
                y=anon_doxed_df['anon_counts'],
                width=0.3,
                offset=-0.3,
                name='Anon data',
                text=anon_doxed_df['anon_counts'].tolist(),
                marker=dict(color=px.colors.qualitative.Vivid[2]),
            ),
            secondary_y=False,
        )

        anon_doxed_comp.add_trace(
            go.Bar(
                x=anon_doxed_df['index'],
                y=anon_doxed_df['doxed_counts'],
                width=0.3,
                offset=0,
                name='Doxed data',
                text=anon_doxed_df['doxed_counts'].tolist(),
                marker=dict(color=px.colors.qualitative.Vivid[5]),
            ),
            secondary_y=True,
        )

        # anon_doxed_comp.update_traces(color=[px.colors.qualitative.Vivid[2], px.colors.qualitative.Vivid[5]])

        anon_doxed_comp.update_layout(
            title='Customer numbers vs transaction ratio - Anon / Doxed',
            xaxis_title='Customer counts and transactions in total',
            yaxis_title='Anon counts',
            yaxis2_title='Doxed counts',
            template='seaborn',
            legend=dict(
                x=0.75,
                y=0.95,
                bgcolor='rgba(0, 0, 0, 0)',
                bordercolor='rgba(0, 0, 0, 0.5)',
                borderwidth=1,
                font=dict(
                    size=10,
                ),
            ),
        )

        # Set y-axis ranges to align the bars properly
        anon_doxed_comp.update_yaxes(
            range=[0, max(anon_doxed_df['anon_counts']) + 10000], secondary_y=False)
        anon_doxed_comp.update_yaxes(
            range=[0, max(anon_doxed_df['doxed_counts']) + 10000], secondary_y=True)

        anon_doxed_comp.write_image(
            r'output/bar_anon_doxed_transaction_comp.png', scale=6, width=1080,  height=480)

    def bar_anon_doxed_offer_comp(self):
        '''This method generates a grouped bar plot, comparing the sums of all offer responses of anon and doxed customers'''

        anon_sum = self.anon_df[['offer_received',
                                 'offer_viewed', 'offer_completed']].sum()
        doxed_sum = self.doxed_df[['offer_received',
                                   'offer_viewed', 'offer_completed']].sum()

        anon_sum_df = pd.DataFrame(
            {'values': anon_sum.index, 'anon_counts': anon_sum.values})
        doxed_sum_df = pd.DataFrame(
            {'values': doxed_sum.index, 'doxed_counts': doxed_sum.values})

        anon_doxed_df = pd.merge(anon_sum_df, doxed_sum_df, on=['values'])
        anon_doxed_df['values'] = ['Offer received',
                                   'Offer viewed', 'Offer completed']

        # Create the grouped bar chart with two y-axes
        anon_doxed_comp = make_subplots(specs=[[{"secondary_y": True}]])

        anon_doxed_comp.add_trace(
            go.Bar(
                x=anon_doxed_df['values'],
                y=anon_doxed_df['anon_counts'],
                width=0.3,
                offset=-0.3,
                name='Anon offer responses',
                text=anon_doxed_df['anon_counts'].tolist(),
            ),
            secondary_y=False,
        )

        anon_doxed_comp.add_trace(
            go.Bar(
                x=anon_doxed_df['values'],
                y=anon_doxed_df['doxed_counts'],
                width=0.3,
                offset=0,
                name='Doxed offer responses',
                text=anon_doxed_df['doxed_counts'].tolist(),
            ),
            secondary_y=True,
        )

        anon_doxed_comp.update_layout(
            title='Offer responses: Anon customers vs. Doxed customers',
            xaxis_title='Offer responses',
            yaxis_title='Anon counts',
            yaxis2_title='Doxed counts',
            template='seaborn',
            legend=dict(
                x=0.75,
                y=0.95,
                bgcolor='rgba(0, 0, 0, 0)',
                bordercolor='rgba(0, 0, 0, 0.5)',
                borderwidth=1,
                font=dict(
                    size=10,
                ),
            ),
        )

        # Set y-axis ranges to align the bars properly
        anon_doxed_comp.update_yaxes(
            range=[0, max(anon_doxed_df['anon_counts']) + 10000], secondary_y=False)
        anon_doxed_comp.update_yaxes(
            range=[0, max(anon_doxed_df['doxed_counts']) + 10000], secondary_y=True)

        anon_doxed_comp.write_image(
            r'output/bar_anon_doxed_offer_comp.png', scale=6, width=1080,  height=480)

    def hist_bogo_age_dist(self):
        '''This method generates a histogram showing all "bogo" offer responses as an age distribution.'''

        bogo_data = self.doxed_df[self.doxed_df.offer_type == 'bogo']
        bogo_data = bogo_data.rename(columns={
            'offer_received': 'Offer received', 
            'offer_viewed':'Offer viewed',
            'offer_completed':'Offer completed'})

        hist_bogo_age_dist = px.histogram(
            data_frame=bogo_data,
            x='age',
            y=['Offer received', 'Offer viewed', 'Offer completed'],
            color_discrete_map={'Offer received': 'lightblue',
                                'Offer viewed': 'blue', 
                                'Offer completed': 'darkblue'},
            nbins=80,
            barmode='stack',
        )

        hist_bogo_age_dist.update_layout(
            title='Age distribution - "Buy one, get one" offer',
            xaxis_title='Age',
            yaxis_title='Counts',
            template='seaborn',
            legend=dict(
                title='Offer type',
                x=0.8,
                y=0.95,
                bgcolor='rgba(0, 0, 0, 0)',
                bordercolor='rgba(0, 0, 0, 0.5)',
                borderwidth=1,
                font=dict(
                    size=10,
                ),
            ),
        )

        hist_bogo_age_dist.write_image(
            r'output/hist_bogo_age_dist.png', scale=6, width=1080,  height=480)

    def hist_bogo_income_dist(self):
        '''This method generates a histogram showing all "bogo" offer responses as an income distribution.'''
        
        bogo_data = self.doxed_df[self.doxed_df.offer_type == 'bogo']
        bogo_data = bogo_data.rename(columns={
            'offer_received': 'Offer received', 
            'offer_viewed':'Offer viewed',
            'offer_completed':'Offer completed'})

        hist_bogo_income_dist = px.histogram(
            data_frame=bogo_data,
            x='income',
            y=['Offer received', 'Offer viewed', 'Offer completed'],
            color_discrete_map={'Offer received': 'rgb(255, 192, 192)',
                                'Offer viewed': 'red', 
                                'Offer completed': 'rgb(139, 0, 0)'},
            nbins=80,
        )

        hist_bogo_income_dist.update_layout(
            title='Income distribution - "Buy one, get one" offer',
            xaxis_title='Income',
            yaxis_title='Counts',
            template='seaborn',
            legend=dict(
                title='Offer type',
                x=0.8,
                y=0.95,
                bgcolor='rgba(0, 0, 0, 0)',
                bordercolor='rgba(0, 0, 0, 0.5)',
                borderwidth=1,
                font=dict(
                    size=10,
                ),
            ),
        )

        hist_bogo_income_dist.write_image(
            r'output/hist_bogo_income_dist.png', scale=6, width=1080,  height=480)

    def hist_discount_age_dist(self):
        '''This method generates a histogram showing all "discount" offer responses as an age distribution.'''

        discount_data = self.doxed_df[self.doxed_df.offer_type == 'discount']
        discount_data = discount_data.rename(columns={
            'offer_received': 'Offer received', 
            'offer_viewed':'Offer viewed',
            'offer_completed':'Offer completed'})

        hist_discount_age_dist = px.histogram(
            data_frame=discount_data,
            x='age',
            y=['Offer received', 'Offer viewed', 'Offer completed'],
            color_discrete_map={'Offer received': 'lightblue',
                                'Offer viewed': 'blue', 
                                'Offer completed': 'darkblue'},
            nbins=80,
        )

        hist_discount_age_dist.update_layout(
            title='Age distribution - Discount offer',
            xaxis_title='Age',
            yaxis_title='Counts',
            template='seaborn',
            legend=dict(
                title='Offer type',
                x=0.8,
                y=0.95,
                bgcolor='rgba(0, 0, 0, 0)',
                bordercolor='rgba(0, 0, 0, 0.5)',
                borderwidth=1,
                font=dict(
                    size=10,
                ),
            ),
        )

        hist_discount_age_dist.write_image(
            r'output/hist_discount_age_dist.png', scale=6, width=1080,  height=480)

    def hist_discount_income_dist(self):
        '''This method generates a histogram showing all "discount" offer responses as an income distribution.'''
        
        discount_data = self.doxed_df[self.doxed_df.offer_type == 'discount']
        discount_data = discount_data.rename(columns={
            'offer_received': 'Offer received', 
            'offer_viewed':'Offer viewed',
            'offer_completed':'Offer completed'})

        hist_discount_income_dist = px.histogram(
            data_frame=discount_data,
            x='income',
            y=['Offer received', 'Offer viewed', 'Offer completed'],
            color_discrete_map={'Offer received': 'rgb(255, 192, 192)',
                                'Offer viewed': 'red', 
                                'Offer completed': 'rgb(139, 0, 0)'},
            nbins=80,
        )

        hist_discount_income_dist.update_layout(
            title='Income distribution - Discount offer',
            xaxis_title='Income',
            yaxis_title='Counts',
            template='seaborn',
            legend=dict(
                title='Offer type',
                x=0.8,
                y=0.95,
                bgcolor='rgba(0, 0, 0, 0)',
                bordercolor='rgba(0, 0, 0, 0.5)',
                borderwidth=1,
                font=dict(
                    size=10,
                ),
            ),
        )

        hist_discount_income_dist.write_image(
            r'output/hist_discount_income_dist.png', scale=6, width=1080,  height=480)


if __name__ == '__main__':

    data = pd.read_csv(r'data/data_clean.csv')
    Plots = Plot(data)
    Plots.generate_plots_for_blog_post()
    print('Done')
