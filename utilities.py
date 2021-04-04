import pandas as pd
import networkx as nx
import math
import matplotlib.pyplot as plt

# Generate an endgelist for a given DataFrame
# And create a DiGraph using the edgelist
# Also filters tweets from a given hashtag or country if specified 
def get_network(df, from_hashtag="", from_country=""):
    ''' returns a dataframe with the edges and timestamp from tweets feed (df)'''
    
    if from_hashtag != "":
        mask = df["hashtags"].apply(lambda x: from_hashtag.lower() in x)
        filteredDf = df[mask]
    else: 
        filteredDf = df

    if from_country != "":
        mask = filteredDf["country_code"] == from_country
        filteredDf = filteredDf[mask]


    filteredColumns = ['screen_name', 'to', 'created_at', 'text', 'followers_count', 'friends_count', 'favourites_count', 'retweet_count']
    edgelistColumns = ["followers_count", "friends_count", "favourites_count", "retweet_count", "created_at", "text"]

    if("toxicity" in list(filteredDf.columns)):
        filteredColumns += "toxicity"
        edgelistColumns += "toxicity"

    edges_df = filteredDf[filteredColumns]

    edges_df = edges_df.rename(columns={'screen_name': 'from'})
    edges_df = edges_df.explode('to')
    edges_df = edges_df.explode('to').reset_index(drop=True)
    
    edges_df["from"] = edges_df["from"].apply(lambda x: str("@" + x) if len(x) != 0 and x[0] != "@" else x)
    edges_df["to"] = edges_df["to"].apply(lambda x: str("@" + x) if len(x) != 0 and x[0] != "@" else x)
    
    G = nx.from_pandas_edgelist(edges_df, 'from', 'to', edgelistColumns, create_using=nx.DiGraph())

    return G

# Takes our main dataset and combines `reply_to_screen_name` and `mentions` from tweets
# into a single `to` column
# this should ALWAYS be used to get our primary data for the dataset
def transform_df(df):
    edges_df = df[['screen_name', 'reply_to_screen_name', 'created_at', 'hashtags', 'mentions', 'followers_count', 'friends_count', 'text', 'is_quote', 'is_retweet', 'favourites_count', 'retweet_count', 'country_code', 'verified', 'lang']]

    edges_df["hashtags"] = edges_df["hashtags"].apply(lambda x: ",".join(x))
    edges_df["mentions"] = edges_df["mentions"].apply(lambda x: ",".join(x))
    
    edges_df["reply_to_screen_name"] = edges_df["reply_to_screen_name"].fillna("")
    edges_df["reply_to_screen_name"] = edges_df["reply_to_screen_name"].apply(lambda x: "@" + x if x != "" else "")

    edges_df["to"] = edges_df["reply_to_screen_name"] + "," + edges_df["mentions"]
    edges_df["to"] = edges_df["to"].fillna("")

    edges_df["to"] = edges_df["to"].apply(lambda x: ",".join(list(set(x.split(",")))))
    edges_df["to"] = edges_df["to"].apply(lambda x: x[1:] if len(x)>0 and x[0]=="," else x)

    edges_df = edges_df.drop(["reply_to_screen_name", "mentions"], axis=1)
    edges_df["country_code"] = edges_df["country_code"].fillna("")

    noReplyFilter = edges_df["to"] != ""
    edges_df = edges_df[noReplyFilter]

    noRTFilter = edges_df["is_retweet"] != True
    edges_df = edges_df[noRTFilter]

    onlyEnglishFilter = edges_df["lang"] == "en"
    edges_df = edges_df[onlyEnglishFilter]

    rTfilters = edges_df["retweet_count"] >= 50
    edges_df = edges_df[rTfilters]

    likefilters = edges_df["favourites_count"] >= 50
    edges_df = edges_df[likefilters]

    edges_df = edges_df.drop_duplicates().reset_index(drop=True)

    return edges_df

# Given a network, creates a gexf file for Gephi
def create_gephi_from_network(network, name):
    nx.write_gexf(network, "./gephis/" + name + "-network.gexf")

# Get the giant strongly connected component of G
def get_strongly_gcc(G):
    SGcc = max(nx.strongly_connected_components(G), key=len)
    SGcc = G.subgraph(SGcc)
    return SGcc

# Get the giant weakly connected component of G
def get_weakly_gcc(G):
    WGcc = max(nx.weakly_connected_components(G), key=len)
    WGcc = G.subgraph(WGcc)
    return WGcc
   
# Plot the graph with varying nodesize
def plot_network(G, G_degree=None, outputname="default", color="turquoise", n_color="blue"):    
    fig = plt.figure(num=None, figsize=(15, 15), dpi=60, facecolor='b', edgecolor='k')
    pos = nx.spring_layout(G)
    
    if G_degree:
        node_size=[v * 10 for v in dict(G_degree).values()]
    else:
        node_size = 1
        
    nx.draw(G, pos, nodelist=dict(G_degree).keys(), node_size=node_size, width=0.5, alpha=0.5, edge_color=color, node_color=n_color)
    plt.axis('off')
    plt.show()
    fig.savefig("./viz/" +outputname + "-network.svg", transparent=True)