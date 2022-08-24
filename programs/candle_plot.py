import plotly.graph_objects as go

def candle_plot(data):
    fig = go.Figure(data = [
        go.Candlestick(
            x = data.index,
            open = data.Open,
            high = data.High,
            low = data.Low,
            close = data.Close,
            )
    ])
    return fig.show()