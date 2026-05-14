import dash_bootstrap_components as dbc
from dash import html

def create_dashboard1_layout():
    return dbc.Card(
        dbc.CardBody([
            html.H3("Visão Executiva", className="card-title text-warning"),
            html.P("Layout aqui...", className="text-muted")
        ]),
        className="mt-3 border-secondary"
    )
