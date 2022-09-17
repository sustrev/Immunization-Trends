import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings("ignore")

def demo_profile(df, name=None):
    if name==None:
        c_title = "Full UTD Profile"
    else:
        c_title = "Full UTD Profile: {}".format(name)
    fig = px.line(df)
    fig.update_layout(
        title=c_title,
        yaxis_title = "UTD",
        xaxis_title = "YEAR",
        legend_title = "Key",
        yaxis=dict(tickformat=".1%"))
    return fig

def compare_lines(nested_list, immunization_type):
    # nested_list format = [name, df]

    fig = go.Figure()
    for t in nested_list:
        t_name = t[0]
        t_df = t[1]
        fig.add_trace(go.Scatter(x=t_df.index, y=t_df[immunization_type], name = t_name, mode="lines"))

    fig.update_layout(
        title="{} Comparison".format(immunization_type),
        yaxis_title = "UTD",
        xaxis_title = "YEAR",
        legend_title = "Key",
        yaxis=dict(tickformat=".1%"))
    return fig