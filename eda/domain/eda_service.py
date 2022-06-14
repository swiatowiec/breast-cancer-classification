from domain.data_series import DataSeries
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
import pandas as pd


class EdaService:
    def plotter(self, data_series: DataSeries, input_params):
        plots_data = self._prepare_plots_data(
            data_series, input_params.target_column)

        plots = {}
        plots['count_of_' + input_params.target_column] = self.generate_bar_plot(malignant_columns=plots_data['malignant_columns'],
                                                                                 benign_columns=plots_data['benign_columns'])
        plots['percentage_of_' + input_params.target_column] = self.generate_pie_plot(malignant_columns=plots_data['malignant_columns'],
                                                                                      benign_columns=plots_data['benign_columns'])
        plots['correlation_matrix'] = self.generate_correlation_matrix(
            correlation=plots_data['correlation'])

        return plots, plots_data

    def _prepare_plots_data(self, data_series: DataSeries, target_column: str):
        malignant_columns = data_series.get_malignant_columns(
            target_column=target_column)
        benign_columns = data_series.get_benign_columns(
            target_column=target_column)
        correlation = data_series.get_corelation_matrix()

        return {
            "correlation": correlation,
            "malignant_columns": malignant_columns,
            "benign_columns": benign_columns
        }

    def generate_bar_plot(self, malignant_columns: pd.DataFrame, benign_columns: pd.DataFrame):
        fig = go.Figure()
        trace = go.Bar(x=(len(malignant_columns), len(benign_columns)), y=['malignant', 'benign'], orientation='h', opacity=0.8, marker=dict(
            color=['gold', 'lightskyblue'],
            line=dict(color='#000000', width=1.5)))
        fig.add_trace(trace)
        return fig

    def generate_pie_plot(self, malignant_columns: pd.DataFrame, benign_columns: pd.DataFrame):
        fig = go.Figure()
        trace = go.Pie(
            labels=['benign', 'malignant'],
            values=(len(malignant_columns), len(benign_columns)),
            textfont=dict(size=15), opacity=0.8,
            marker=dict(colors=['lightskyblue', 'gold'],
                        line=dict(color='#000000', width=1.5))
        )
        fig.add_trace(trace)
        return fig

    def generate_correlation_matrix(self, correlation: pd.DataFrame):
        matrix_cols = correlation.columns.tolist()
        corr_array = np.array(correlation)
        fig = go.Figure()
        trace = go.Heatmap(z=corr_array,
                           x=matrix_cols,
                           y=matrix_cols,
                           xgap=2,
                           ygap=2,
                           colorscale='Viridis',
                           colorbar=dict(),
                           )
        layout = go.Layout(dict(title='Correlation Matrix for variables',
                                autosize=False,
                                height=720,
                                width=800,
                                margin=dict(r=0, l=210,
                                            t=25, b=210,
                                            ),
                                yaxis=dict(tickfont=dict(size=9)),
                                xaxis=dict(tickfont=dict(size=9)),
                                )
                           )

        fig.add_trace(trace)
        fig.update_layout(layout)
        return fig

    def generate_distribution_plot(self, feature_name: str, size_bin: float, malignant_columns: pd.DataFrame, benign_columns: pd.DataFrame):
        tmp1 = malignant_columns[feature_name]
        tmp2 = benign_columns[feature_name]
        hist_data = [tmp1, tmp2]
        group_labels = ['malignant', 'benign']
        colors = ['#FFD700', '#7EC0EE']

        fig = ff.create_distplot(hist_data, group_labels, colors=colors,
                                 show_hist=True, bin_size=size_bin, curve_type='kde')
        fig['layout'].update(title=feature_name)
        return fig

    def generate_correlated_features_plot(self, feature_1: str, feature_2: str,  malignant_columns: pd.DataFrame, benign_columns: pd.DataFrame):

        fig = go.Figure()
        trace0 = go.Scatter(
            x=malignant_columns[feature_1],
            y=malignant_columns[feature_2],
            name='malignant',
            mode='markers',
            marker=dict(color='#FFD700',
                        line=dict(
                            width=1)))

        trace1 = go.Scatter(
            x=benign_columns[feature_1],
            y=benign_columns[feature_2],
            name='benign',
            mode='markers',
            marker=dict(color='#7EC0EE',
                        line=dict(
                            width=1)))

        layout = dict(title=feature_1 + " "+"vs"+" " + feature_2,
                      yaxis=dict(title=feature_2, zeroline=False),
                      xaxis=dict(title=feature_1, zeroline=False)
                      )

        fig.add_trace(trace0)
        fig.add_trace(trace1)
        fig.update_layout(layout)
        return fig
