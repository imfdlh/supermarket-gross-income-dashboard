import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Container([
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Welcome to Supermarket Sales Dashboard!",
                className="text-center"
                ),
            className="mb-5 mt-5"
            )
        ),
        dbc.Row([
            dbc.Col([
                    html.H5(
                        'This dashboard contains analysis of supermarket sales in Myanmar.',
                    ),
                    html.H5(
                        children=[
                            'The dataset can be accessed from ',
                            html.A("here.", href="https://www.kaggle.com/aungpyaeap/supermarket-sales"),
                        ]
                    ),
                    html.Br(),
                    html.H5(
                        children=[
                            "The analysis is done by ",
                            html.Strong(
                                html.A("Fadilah Nur Imani", href="https://github.com/imfdlh",
                                className="link-nama"),
                            ),
                            " as Milestone 1 submission for FTDS batch 001 Phase 0."
                        ]
                    )
                ],
                className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardImg(src="/assets/img/github.png", top=True),
                    dbc.CardBody(
                        [
                            html.H4("My Github", className="card-title"),
                            html.P(
                                "You can find this project under the link below, "
                                "also don't forget to visit my github for more repository!",
                                className="card-text",
                            ),
                            dbc.Button("Fadilah's Milestone Repo", color="primary", href = "https://github.com/FTDS-001/MilestoneP0/tree/FadilahNurImani"),
                        ]
                    ),
                ],
                style={"width": "18rem"},
                ),
            className = "mb-5 mt-5"
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardImg(src="/assets/img/visualization.png", top=True),
                    dbc.CardBody(
                        [
                            html.H4("Visualization", className="card-title"),
                            html.P(
                                "To view visualization of supermarket sales data, visit the button below.",
                                className="card-text",
                            ),
                            dbc.Button("Visualization", color="info", href = '/apps/visualization'),
                        ]
                    ),
                ],
                style={"width": "18rem"},
                ),
            className = "mb-5 mt-5"
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardImg(src="/assets/img/hypothesis.png", top=True),
                    dbc.CardBody(
                        [
                            html.H4("Hypothesis", className="card-title"),
                            html.P(
                                "To view hypothesis of supermarket sales data, visit the button below.",
                                className="card-text",
                            ),
                            dbc.Button("Hypothesis", color="info", href = '/apps/hypothesis'),
                        ]
                    ),
                ],
                style={"width": "18rem"},
                ),
            className = "mb-5 mt-5"
            )
        ])
    ])
])