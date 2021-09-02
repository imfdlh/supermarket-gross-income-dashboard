import plotly.express as px
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app

# preprocessing
df = pd.read_csv('supermarket_sales_preprocessed.csv')
df["date_time"] = pd.to_datetime(df["date_time"])
df1 = pd.pivot_table(df, values = "gross_income", index = [df.date_time.dt.date], columns = ["branch_location"], aggfunc = np.mean)
# fill na with interpolate
df1.interpolate(inplace = True)
# get day name
df1["day"] = pd.to_datetime(df1.index.to_series()).dt.day_name()
df1['All Branches'] = np.mean(df1[['A - Yangon', 'B - Mandalay', 'C - Naypyitaw']], axis = 1)
df1 = df1[['day', 'All Branches', 'A - Yangon', 'B - Mandalay', 'C - Naypyitaw']]

df = df.set_index(["date_time"])
df2 = df.groupby(["branch_location"]).sum().reset_index()
df3 = pd.pivot_table(df, values = "gross_income", index = [df.product_line], columns = ["branch_location"], aggfunc = np.sum).reset_index()
df3['All Branches'] = np.sum(df3[['A - Yangon', 'B - Mandalay', 'C - Naypyitaw']], axis = 1)
df3 = df3[['product_line', 'All Branches', 'A - Yangon', 'B - Mandalay', 'C - Naypyitaw']]

df4 = pd.pivot_table(df, values = "gross_income", index = [df.payment], columns = ["branch_location"], aggfunc = np.sum).reset_index()
df4['All Branches'] = np.sum(df4[['A - Yangon', 'B - Mandalay', 'C - Naypyitaw']], axis = 1)
df4 = df4[['payment', 'All Branches', 'A - Yangon', 'B - Mandalay', 'C - Naypyitaw']]

df5 = pd.pivot_table(df, values = "gross_income", index = [df.customer_type], columns = ["branch_location"], aggfunc = np.sum).reset_index()
df5['All Branches'] = np.sum(df5[['A - Yangon', 'B - Mandalay', 'C - Naypyitaw']], axis = 1)
df5 = df5[['customer_type', 'All Branches', 'A - Yangon', 'B - Mandalay', 'C - Naypyitaw']]

# figure 1
fig1 = px.bar(
    df2, x = "branch_location", y = "gross_income", color = "branch_location",
    title = "Total of Gross Income by Branch",
    color_discrete_map = {
        'A - Yangon':'#18bc9c',
        'B - Mandalay':'#3498db',
        'C - Naypyitaw':'#e83e8c'
    },
    labels = {
        "branch_location": "Branch - Location",
        "gross_income": "Gross Income"
    }
)
fig1.update_traces(hovertemplate='<b>%{x}</b><br><br>Total Gross Income: %{y:.2f}<extra></extra>')

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.H1(
                    "Store Branches' Gross Income - Q1 2019",
                    className = "text-center",
                ),
                className = "mb-2 mt-5"
            ),
        ]),
        dbc.Spinner([
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        figure = fig1
                    ),
                    className="mb-5"
                )
            ])
        ]),
        dbc.Row([
            dbc.Col(
                html.H3(
                    id="chosen-branch",
                    className = "text-center",
                ),
                className = "mb-2 mt-5"
            ),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Select Branch:"),
                dbc.RadioItems(
                    id="selected_branch1",
                    options=[
                        {"label": branch_location, "value": branch_location} for branch_location in df1.columns[1:]
                    ],
                    value='All Branches',
                    inline=True,
                ),
                dbc.Spinner([
                    dcc.Graph(
                        id='chart1'
                    )
                ])
            ],
            className = "mb-4"),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Spinner([
                    dcc.Graph(
                        id='chart3'
                    )
                ])
            ],
            className = "mb-4"),
            dbc.Col([
                dbc.Spinner([
                    dcc.Graph(
                        id='chart4'
                    )
                ])
            ],
            className = "mb-4"),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Spinner([
                    dcc.Graph(
                        id='chart5'
                    )
                ])
            ],
            className = "mb-5"),
        ]),
        # dbc.Row([
        #     dbc.Col([
        #         dcc.Markdown([
        #             '''
        #             ## Insights & Recommendations
        #             '''
        #         ]),
        #         dcc.Markdown([
        #             '''
        #             - Across all branches, customer with membership contributes the most for the gross income.
        #             - Each branch has different contribution towards income per product:
        #                 - Branch A: Most contributed by Home & Lifestyle products
        #                 - Branch B: Most contributed by Sports & Travel products
        #                 - Branch C: Most contributed by Food & Beverages products
        #             - The contribution of payment type in each branch is different:
        #                 - Branch A: Most contributed by E-wallet, least contributed by Credit Card
        #                 - Branch B: Most contributed by Credit Card, least contributed by E-wallet
        #                 - Branch C: Most contributed by Cash, least contributed by Credit Card


        #             **Recommendations:**
        #             - Create mobile application for membership rewards program that is fun to use to retain more members.
        #             - Build a product-based specialization branding, so more people will know where to go to find variety of product choices.
        #             - Increase the number of tenants that provide E-wallet and Credit Card payment option for customer loyalty, so it'll be easier to attract and retain customers.
        #             '''
        #         ],
        #         className = "mb-3 mt-3 content-m"),
        #     ],
        #     className = "mb-5 mt-5"
        #     )
        # ]),
    ])
])

@app.callback(
    Output('chart1', 'figure'),
    Input('selected_branch1', 'value'))
def update_chart1(branch_location):
    fig = px.line(
        df1, x = df1.index, y = branch_location, title = "Average of Gross Income per Day",
        labels = {
            "date_time": "Date of Time"
        }
    )
    fig.update_traces(text = df1['day'], hovertemplate='<b>%{text}<br>%{x}</b><br><br>Avg Gross Income: %{y:.1f}')
    return fig

@app.callback(
    Output('chart3', 'figure'),
    Input('selected_branch1', 'value'))
def update_chart2(branch_location):
    fig = px.pie(df3,
        values=branch_location, names="product_line", color='product_line',
        title = "Gross Income by Product: " + branch_location,
        color_discrete_map = {
            'Electronic accessories':'#e74c3c',
            'Fashion accessories':'#18bc9c',
            'Food and beverages':'#f39c12',
            'Health and beauty':'#6f42c1',
            'Home and lifestyle':'#e83e8c',
            'Sports and travel':'#3A3335'
        },
        labels = {
            'product_line' : 'Product'
        }
    )
    fig.update_traces(hovertemplate='<b>%{label}</b><br><br>Total Gross Income: %{value:.2f}')
    return fig

@app.callback(
    Output('chart4', 'figure'),
    Input('selected_branch1', 'value'))
def update_chart2(branch_location):
    fig = px.pie(
        df4, values=branch_location, names="payment", color='payment',
        title = "Gross Income by Payment: " + branch_location,
        color_discrete_map = {
            'Ewallet':'#f39c12',
            'Cash':'#18bc9c',
            'Credit card':'#3A3335'
        },
        labels = {
            'payment' : 'Payment'
        }, hole=.3
    )
    fig.update_traces(hovertemplate='<b>%{label}</b><br><br>Total Gross Income: %{value:.2f}')
    return fig

@app.callback(
    Output('chart5', 'figure'),
    Input('selected_branch1', 'value'))
def update_chart2(branch_location):
    fig = px.bar(
        df5, x=branch_location, y="customer_type", color='customer_type',
        title = "Gross Income by Customer Type: " + branch_location,
        color_discrete_map = {
            'Member':'#6f42c1',
            'Normal':'#f39c12'
        },
        labels = {
            "customer_type": "Type of Customer"
        }
    )
    fig.update_traces(hovertemplate='<b>%{y}</b><br><br>Total Gross Income: %{x:.2f}<extra></extra>')
    return fig

@app.callback(
    Output('chosen-branch', 'children'),
    Input('selected_branch1', 'value'))
def update_chart2(branch_location):
    text_branch = "Gross Income of " + branch_location + " - Q1 2019"
    return text_branch