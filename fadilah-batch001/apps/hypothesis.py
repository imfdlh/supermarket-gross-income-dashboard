import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dtab
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np

df_f = pd.DataFrame({
    '':["branch_location", "Residual"],
    'df':[2.0,997.0],
    'sum_sq':[242.602644, 136716.894906],
    'mean_sq':[121.301322, 137.128280],
    'F':[0.884583, "NaN"],
    'PR(>F)':[0.41321, "NaN"]
})

df = pd.read_csv('supermarket_sales_preprocessed.csv')
df_h = df[["branch_location", "gross_income"]]
df_viz = df.groupby(["branch", "city"]).mean().round(1).reset_index().rename(columns={'branch':'Branch','city':'Location', 'gross_income':'Average of Gross Income'})[['Branch', 'Location', 'Average of Gross Income']]

fig1 = ff.create_table(df_viz, height_constant=60)
fig1.update_layout(margin = {'t':50, 'l':170, 'r':170, 'b':50},)

fig2 = px.box(
    df_h, x="branch_location", y="gross_income",
    labels = {
        "branch_location": "Branch - Location",
        "gross_income": "Gross Income"
    },
    color = "branch_location",
    category_orders=dict(branch_location=['A - Yangon', 'B - Mandalay', 'C - Naypyitaw'])
)
fig2.update_layout(showlegend=False)

df = pd.read_csv("supermarket_sales_preprocessed.csv")
df_h = df[["branch_location", "gross_income"]]
observed_variance = df_h.groupby("branch_location").mean().var()[0]
df_pv = pd.read_csv('perm_variance.csv')
perm_variance = df_pv['column']
fig3 = px.histogram(
    perm_variance, nbins=20
)
fig3.add_vline(x = observed_variance, line_width=2.5, line_dash="dash", line_color="#3A3335")
fig3.add_annotation(
    text="Observed<br>Variance", showarrow=False,bordercolor="#000000",borderwidth=1,borderpad=4,bgcolor="#ffffff",
    font=dict(
        size=16,
        color="#000000"
    ),
    x = 0.65, y = 640,align="center"
)
fig3.update_layout(showlegend=False, xaxis_title_text='Variance', yaxis_title_text='Frequency')

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1([
                    "Hypothesis Test",
                    html.Br(),
                    "Store Branches' Gross Income"
                ],
                className = "text-center"),
            ],
            className = "mb-2 mt-5"
            )
        ]),
        dbc.Row([
            dbc.Col([
               dcc.Markdown([
                    '''
                    ## Average of Gross Income per Branch - Q1 2019                
                    '''
                ]),
                dbc.Spinner([
                    dcc.Graph(
                        figure = fig1
                    ),
                ]),
                dcc.Markdown([
                    '''
                    At a glance, we can see that the average gross income of 3 store branches is similar.
                    But, there's one unit difference between branch A and B towards branch C.
                    So, before making any assumption, we have to make sure that the difference is statistically significant and is not happening by chance.
                    Therefore, we need to conduct hypothesis testing to prove our assumption.
                    '''
                ],
                className = "mb-3 mt-3 content-m"),
            ],
            className = "mb-2 mt-5"
            ),
        ]),
        dbc.Row([
            dbc.Col([
               dcc.Markdown([
                    '''
                    ## Distribution of Gross Income - Q1 2019                  
                    '''
                ]),
                dbc.Spinner([
                    dcc.Graph(
                        figure = fig2
                    ),
                ]),
                dcc.Markdown([
                    '''
                    We have to check the distribution of gross income for each branch fefore conducting hypothesis testing.
                    '''
                ],
                className = "mb-3 mt-3 content-m"),
            ],
            className = "mb-2 mt-5"
            )
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Markdown([
                    '''
                    ## Hypothesis'''
                ]),
                dcc.Markdown([
                    '''
                    - Null hypothesis: There are no significant differences between the average of gross income amongst 3 store branches.
                    - Alternate hypothesis: There are significant differences between the average of gross income amongst 3 store branches.
                    '''
                ],
                className = "mb-3 mt-3 content-m"),
            ],
            className = "mb-2 mt-5"
            )
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Markdown([
                    '''
                    ## Methodology'''
                ]),
                dcc.Markdown([
                    '''
                    Since we want to compare the average of 3 store branches, we will use ANOVA (Analysis of Variance) test.
                    This methodology was chosen because we have multiple categories of a categorical variable and a continuous variable.
                    '''
                ],
                className = "mb-3 mt-3 content-m"),
            ],
            className = "mb-2 mt-5"
            )
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Markdown([
                    '''
                    ## ANOVA Testing
                    '''
                ]),
                dcc.Markdown([
                    '''
                    We set the level of significance to 0.05. If the probability of the test is greater than 0.05, we can accept the Null hypothesis.
                    '''
                ],
                className = "mb-3 mt-3 content-m")
            ],
            className = "mb-2 mt-5"
            )
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Markdown([
                    '''
                    ### Using Permutation Test
                    '''
                ]),
                dcc.Markdown([
                    '''
                    - Observed means:
                        - A - Yangon: 14.9
                        - B - Mandalay: 15.2
                        - C - Naypyitaw: 16.1
                    - Gross income variance: 0.365
                    - Permutation test variance: 0.014
                    '''
                ],
                className = "mb-3 mt-3 content-m"),
                dbc.Spinner([
                    dcc.Graph(
                        figure = fig3
                    ),
                ]),
                dcc.Markdown([
                    '''
                    The permutation test is done in 3000 times and resulted in Probability of 0.432.
                    This is greater than the level of significance that we have set.
                    '''
                ],
                className = "mb-3 mt-3 content-m"),
            ],
            className = "mb-2 mt-5"
            )
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Markdown([
                    '''
                    ### Using F-Statistic
                    '''
                ],
                className = "mb-3"),
                # dtab.DataTable(
                #     columns=[{"name": i, "id": i} for i in df_f.columns],
                #     data = df_f.to_dict('records')
                # ),
                dcc.Markdown([
                    '''
                    After conducting ANOVA test, we get f-statistic and p-value as follows:
                    - F-Statistic: 0.442
                    - P-value: 0.207

                    P-value is greater than the level of significance that we have set.
                    '''
                ],
                className = "mb-3 mt-3 content-m"),
            ],
            className = "mb-2 mt-5"
            )
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Markdown([
                    '''
                    ## Conclusion
                    '''
                ]),
                dcc.Markdown([
                    '''
                    From both of the test, the probability/p-value is greater than level of significance.
                    Based on that, we can say there's a high chance that the variance of gross income of each branch happened by chance.
                    Thus, we fail to reject null hypothesis.

                    Finally, we can conclude that there are no significant differences between the average of gross income amongst 3 store branches.
                    '''
                ],
                className = "mb-3 mt-3 content-m"),
            ],
            className = "mb-5 mt-5"
            )
        ]),
    ])
])