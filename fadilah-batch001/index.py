import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from app import app
from app import server

from apps import home, visualization, hypothesis

app.layout = html.Div([
    dbc.NavbarSimple(
        children = [
            dbc.NavItem(dbc.NavLink("Home", href = '/apps/home')),
            dbc.DropdownMenu(
                children = [
                    dbc.DropdownMenuItem("Gross Income", header = True),
                    dbc.DropdownMenuItem("Visualization", href = '/apps/visualization'),
                    dbc.DropdownMenuItem("Hypothesis", href = '/apps/hypothesis'),
                ],
                nav = True,
                in_navbar = True,
                label = "Analysis",
            ),
            dbc.NavItem(dbc.NavLink("Github", href = 'https://github.com/imfdlh')),
        ],
        brand = "Supermarket Sales Analysis",
        brand_href = "/apps/home",
        color = "primary",
        dark = True,
        sticky = "top"
    ),
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content', children = [])
])

@app.callback(
    Output(component_id = 'page-content', component_property = 'children'),
    [Input(component_id = 'url', component_property = 'pathname')])
def display_page(pathname):
    if pathname == '/apps/visualization':
        return visualization.layout
    elif pathname == '/apps/hypothesis':
        return hypothesis.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug = True)