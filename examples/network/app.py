import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from pyodide.http import open_url
import pandas as pd


url = "https://raw.githubusercontent.com/SocialFinanceDigitalLabs/sf-nova/main/examples/network/data.csv"

st.title('network graph creator')

network_df = pd.read_csv(open_url(url))

A = list(network_df["source_ip"].unique())
B = list(network_df["destination_ip"].unique())

node_list = set(A+B)
G = nx.Graph()
for i in node_list:
    G.add_node(i)
for i,j in network_df.iterrows():
    G.add_edges_from([(j["source_ip"],j["destination_ip"])])

pos = nx.spring_layout(G, k=0.5, iterations=50)

for n, p in pos.items():
    G.nodes[n]['pos'] = p

edge_trace = go.Scatter(
x=[],
y=[],
line=dict(width=0.5,color='#888'),
hoverinfo='none',
mode='lines')

for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='RdBu',
        reversescale=True,
        color=[],
        size=15,
        colorbar=dict(
            thickness=10,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)))

for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])


for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color']+=tuple([len(adjacencies[1])])
    print("ADJ", adjacencies[0])
    node_info = adjacencies[0] or "" +' # of connections: '+str(len(adjacencies[1]))
    node_trace['text']+=tuple([node_info])

fig = go.Figure(data=[edge_trace, node_trace],
            layout=go.Layout(
            title='<br>AT&T network connections',
            titlefont=dict(size=16),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="No. of connections",
                showarrow=False,
                xref="paper", yref="paper") ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

st.plotly_chart(fig)
