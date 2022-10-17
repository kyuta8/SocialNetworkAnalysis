import pandas as pd
import networkx as nx


def degree_centrality(Graph: object, top=5):
    """
        次数中心性

        Graph：グラフオブジェクト
        top：上位何件を抽出するのか
    """
    degree_centers = nx.degree_centrality(Graph)
    degree_centers_sorted =  sorted(degree_centers.items(), key=lambda x: x[1], reverse=True)[:top]
    degree_centers_df = pd.DataFrame(degree_centers_sorted, columns = ['Nodes', 'Degree_Centrality'])
    return degree_centers_df


def close_centrality(Graph: object, top=5):
    """
        近接中心性

        Graph：グラフオブジェクト
        top：上位何件を抽出するのか
    """
    close_centers = nx.closeness_centrality(Graph)
    close_centers_sorted = sorted(close_centers.items(), key=lambda x: x[1], reverse=True)[:top]
    close_centers_df = pd.DataFrame(close_centers_sorted, columns = ['Nodes', 'Close_Centrality'])
    return close_centers_df

    
def between_centrality(Graph: object, top=5):
    """
        媒介中心性

        Graph：グラフオブジェクト
        top：上位何件を抽出するのか
    """
    between_centers = nx.betweenness_centrality(Graph)
    between_centers_sorted = sorted(between_centers.items(), key=lambda x: x[1], reverse=True)[:top]
    between_centers_df = pd.DataFrame(between_centers_sorted, columns = ['Nodes', 'Between_Centrality'])
    return between_centers_df


def eigen_centrality(Graph: object, top=5):
    """
        固有ベクトル中心性

        Graph：グラフオブジェクト
        top：上位何件を抽出するのか
    """
    eigen_centers = nx.eigenvector_centrality_numpy(Graph)
    eigen_centers_sorted = sorted(eigen_centers.items(), key=lambda x: x[1], reverse=True)[:top]
    eigen_centers_df = pd.DataFrame(eigen_centers_sorted, columns = ['Nodes', 'Eigen_Centrality'])
    return eigen_centers_df