import plotly.express as px
import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import dash_pivottable

# from data import data
import pandas as pd

data = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)
# data = data.columns + data.values

print([e.replace(" ", "") for e in list(data.columns)])
# print(data.values)
data = [[e.replace(" ", "") for e in list(data.columns)]] + data.values.tolist()
# print(data)
app = dash.Dash(__name__)
app.title = "My Dash example"

app.layout = html.Div(
    [
        dash_pivottable.PivotTable(
            id="pivot-table",
            data=data,
            cols=["year"],
            colOrder="key_a_to_z",
            # rows=['Party Size'],
            rows=["continent"],
            rowOrder="key_a_to_z",
            # rendererName="Grouped Column Chart",
            aggregatorName="Average",
            vals=["gdpPercap"],
            # valueFilter={'Day of Week': {'Thursday': False}}
        ),
        dcc.Download(id="download"),
        html.Button("Download Filtered Data", id="btn", n_clicks=0),
        dcc.Graph(id="box-plot"),  # Add this line
    ]
)


# @app.callback(Output('output', 'children'),
#               [Input('table', 'cols'),
#                Input('table', 'rows'),
#                Input('table', 'rowOrder'),
#                Input('table', 'colOrder'),
#                Input('table', 'aggregatorName'),
#                Input('table', 'rendererName')])
# def display_props(cols, rows, row_order, col_order, aggregator, renderer):
#     return [
#         html.P(str(cols), id='columns'),
#         html.P(str(rows), id='rows'),
#         html.P(str(row_order), id='row_order'),
#         html.P(str(col_order), id='col_order'),
#         html.P(str(aggregator), id='aggregator'),
#         html.P(str(renderer), id='renderer'),
#     ]

default = 0


@app.callback(
    Output("download", "data"),
    Input("btn", "n_clicks"),
    # Assume "pivot-table" is the id of your PivotTable component
    Input("pivot-table", "cols"),
    Input("pivot-table", "rows"),
    Input("pivot-table", "vals"),
    prevent_initial_call=True,
)
def download(n_clicks, cols, rows, vals):
    print(n_clicks)
    if n_clicks:
        print(cols)
        print(rows)
        print(vals)
        print("\n")
        # Filter the DataFrame
        # filtered_df = df.loc[rows, cols]
        # # Convert filtered DataFrame to CSV and return it
        # return dcc.send_data_frame(filtered_df.to_csv, "mydata.csv")
        # Assume "df" is your original DataFrame and "data" is your original data list
        df = pd.DataFrame(data[1:], columns=data[0])
        print(df)

        # Group by rows and columns and calculate the sum of vals
        reshaped_df = (
            df[rows + cols + vals].groupby(cols + rows)[vals].mean().reset_index()
        )

        # reshaped_df = df[[rows + cols]]
        # print(list(df.columns))
        # print(df[rows + cols])
        # print(df[["Bacteria"]])

        # Print the reshaped DataFrame
        # print(reshaped_df)
        reshaped_df = pd.pivot_table(
            df, index=rows, columns=cols, values=vals, aggfunc="mean"
        )
        reshaped_df[(cols[0], "Totals")] = reshaped_df.sum(axis=1)
        print(reshaped_df)

        # Return the reshaped DataFrame as a string so it can be displayed in the Dash app
        # return reshaped_df.to_string()


@app.callback(
    Output("box-plot", "figure"),  # Update this line
    Input("btn", "n_clicks"),
    Input("pivot-table", "cols"),
    Input("pivot-table", "rows"),
    Input("pivot-table", "vals"),
    prevent_initial_call=True,
)
def generate_box_plot(n_clicks, cols, rows, vals):
    if n_clicks != default:
        df = pd.DataFrame(data[1:], columns=data[0])

        # Group by rows and columns and calculate the mean of vals
        reshaped_df = pd.pivot_table(
            df, index=rows, columns=cols, values=vals, aggfunc="mean"
        )
        reshaped_df[(cols[0], "Totals")] = reshaped_df.sum(axis=1)

        # Generate a box plot
        fig = px.box(df, x=cols[0], y=vals[0], color=rows[0])

        return fig


if __name__ == "__main__":
    app.run_server(debug=True)
