import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from pyodide.http import open_url
import pandas as pd
from collections import defaultdict

DEFAULT_COLOR = "#4a95c7"


type_to_color = {
    "Referral": "#faea5f",
    "Shares information with": "#4a95c7",
    "Funds": "#e0634c",
}
strength_to_linetype = {
    "Strong": "solid",
    "Medium": "dash",
    "Weak": "dot",
}


def setup_network(df) -> nx.Graph:
    source = list(df["source"].unique())
    destination = list(df["destination"].unique())

    node_list = set(source + destination)
    G = nx.Graph()
    for i in node_list:
        G.add_node(i)
    for i, j in df.iterrows():
        G.add_edge(
            j["source"],
            j["destination"],
            type=j["type"],
            strength=j["strength"],
            color=j["color"],
            linetype=j["linetype"],
        )

    pos = nx.spring_layout(G, k=0.5, iterations=50)
    for n, p in pos.items():
        G.nodes[n]["pos"] = p
    return G


def create_trace_line(properties):
    line = dict(width=3)
    line["color"] = properties.get("color", None) or DEFAULT_COLOR
    line["dash"] = properties.get("linetype", None) or "solid"
    return line


def create_edge_traces(G: nx.Graph):
    edge_traces = []
    in_legend: dict[str, bool] = defaultdict(lambda: False)

    for edge in G.edges.data():
        x0, y0 = G.nodes[edge[0]]["pos"]
        x1, y1 = G.nodes[edge[1]]["pos"]
        line = create_trace_line(edge[-1])
        if in_legend[line["color"] + line["dash"]] is False:
            in_legend[line["color"] + line["dash"]] = True
            name = f"<b>type</b>: {edge[-1]['type']} <br /> <b>strength</b>: {edge[-1]['strength']}"
        else:
            name = None
        edge_x = []
        edge_y = []
        edge_x.append(x0)
        edge_x.append(x1)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=line,
            mode="lines",
            name=name,
            showlegend=name is not None,
        )
        edge_traces.append(edge_trace)

    return edge_traces


def create_node_trace(G: nx.Graph):
    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        hoverinfo="text",
        marker=dict(
            showscale=False,
            colorscale="YlGnBu",
            reversescale=True,
            size=10,
        ),
        showlegend=False,
    )

    node_adjacencies = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    return node_trace


def main(df):
    st.title("EH network")

    df["linetype"] = df["strength"].map(strength_to_linetype)
    df["color"] = df["type"].map(type_to_color)

    G = setup_network(df)
    edge_traces = create_edge_traces(G)
    node_trace = create_node_trace(G)

    fig = go.Figure(
        data=edge_traces + [node_trace],
        layout=go.Layout(
            title="<br>Network graph made with Python",
            titlefont_size=16,
            showlegend=True,
            legend=dict(x=0, y=0, orientation='h'),
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    fig.update_traces(hoverinfo="text")

    st.plotly_chart(fig)


def run_with_upload():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, delimiter=";")
        main(df)


def run_with_github_data():
    url = "https://raw.githubusercontent.com/SocialFinanceDigitalLabs/sf-nova/main/examples/network/data.csv"
    df = pd.read_csv(open_url(url), delimiter=";")
    main(df)


run_with_github_data()