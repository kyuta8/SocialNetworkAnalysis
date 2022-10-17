import os
import glob

import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import re
import itertools

from modules.input import read_pajek_file
from modules.transform import to_mode_1_net
from modules.centrality import *



class UnexpectedParameter(Exception):
    pass


### ネットワーク構築用 ###
    

    
# 時系列分析用関数
def color_add_node(ori: list, pre: list, post: list):

    """
        時間（t）におけるノードの集合をpre，時間（t+1）におけるノードの集合ををpostとしている
        oriはtとt+1それぞれにおけるノードの集合を合わせたもの
        変わらずに存在するノード：yellow
        新しく加わったノード：red
        次の時間でなくなったノード：blue
    """
    node_color = []
    
    for i in range(len(ori)):
        if ori[i] in pre and ori[i] in post:
            node_color.append('yellow')

        elif not(ori[i] in pre) and ori[i] in post:
            node_color.append('red')
            
        elif ori[i] in pre and not(ori[i] in post):
            node_color.append('blue')

    return node_color


# ネットワークグラフの出力
def pajek_to_net(files: list, target=[], figure_x=30, figure_y=30, print_graph=True,
                 anotation=False, node_alpha=0.6, edge_alpha=0.8, label_alpha=0.8,
                 font_size=10, degree=False, close=False, between=False,
                 eigen=False, sequence=False, cluster=False, save=False):

    """
        files：.pajの拡張子のファイルリスト（読み込みたいファイルが1つでもリスト形式で）
        target：1-modeネットワークを構築したいときに使う
                dev：開発者のネットワーク
                bug：バグIDのネットワーク
        figure_x：プロットの横幅
        figure_y：プロットの縦幅
        print_graph：グラフの出力（default：True）
        anotation：ノードのラベルを表示（default：False）
        node_alpha：ノードの濃さ（0 ~ 1）
        edge_alpha：エッジの濃さ（0 ~ 1）
        label_alpha：ラベルの濃さ（0 ~ 1）
        font_size：文字の大きさ
        degree：次数中心性のプロットを行うか（default：False）
        close：近接中心性のプロットを行うか（default：False）
        between:：媒介中心性のプロットを行うか（default：False）
        eigen：固有ベクトル中心性のプロットを行うか（default：False）＊これはいらなさそう
        sequence：時系列分析（default：False）
        cluster：クラスター係数の出力（default：False）
        save：png出力（default：False）
    """
    nodes = []
    edges = []
    _sequence = 'sequence' if sequence else 'unsequence'

    for i in range(len(files)):

        G, partition = read_pajek_file(files[i])

        node = list(G.nodes)
        edge = list(G.edges)

        if target:
            if 'dev' == target[0] and len(target) == 1:
                dev_net = to_mode_1_net(node, edge, partition, target)
                nodes.append(dev_net[0])
                edges.append(dev_net[1])

            elif 'bug' == target[0] and len(target) == 1:
                bug_net = to_mode_1_net(node, edge, partition, target)
                nodes.append(bug_net[0])
                edges.append(bug_net[1])

            else:
                raise UnexpectedParameter("target is expected only using a string, either 'dev' or 'bug'.")

        else:
            if print_graph:
                plt.figure(figsize=(figure_x, figure_y))
                plt.title('Time location: ' + re.sub('.paj', '', os.path.basename(files[i])), fontsize=50)
                pos = nx.kamada_kawai_layout(G)

                nx.draw_networkx_nodes(G, pos, node_color=partition, alpha=node_alpha)
                nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=edge_alpha)

                if anotation:
                    nx.draw_networkx_labels(G, pos, font_size=font_size, alpha=label_alpha)

                if save:
                    os.makedirs('./2-mode', exist_ok=True)
                    plt.savefig('./2-mode/' + re.sub('.paj', '.png', os.path.basename(files[i])))

                else:
                    plt.show()

                plt.close()

    if target:
        for i in range(len(files)-1):
            Graph = nx.Graph()

            Graph.add_edges_from(edges[i])
            Graph.add_edges_from(edges[i+1])

            if print_graph:
                plt.figure(figsize=(figure_x, figure_y))
                plt.title('Time location: ' + re.sub('.paj', '', os.path.basename(files[i]))
                            + ' + ' + re.sub('.paj', '', os.path.basename(files[i+1])),
                            fontsize=50)
                pos = nx.kamada_kawai_layout(Graph)

                nx.draw_networkx_nodes(Graph, pos, node_color=color_add_node(list(Graph.nodes), nodes[i], nodes[i+1]), alpha=node_alpha)
                nx.draw_networkx_edges(Graph, pos, edge_color='gray', alpha=edge_alpha)

                if anotation:
                    nx.draw_networkx_labels(Graph, pos, font_size=font_size, alpha=label_alpha)

                if save:
                    path = f'./1-mode/{target[0]}/{_sequence}'
                    os.makedirs(path, exist_ok=True)
                    plt.savefig(path + target[0] + '_' + re.sub('.paj', '', os.path.basename(files[i])) 
                                + '+' + re.sub('.paj', '.png', os.path.basename(files[i+1])))

                else:
                    plt.show()

                plt.close()
                
            if degree:
                path = f'./degree/{_sequence}/{target[0]}'
                os.makedirs(path, exist_ok=True)
                print('Time location：{} → {}'.format(files[i], files[i+1]))
                degree_centrality(Graph).to_csv(os.path.join(path, 'degree_' + target[0] + '_' + re.sub('.paj', '', os.path.basename(files[i]))
                                                                + '+' + re.sub('.paj', '.csv', os.path.basename(files[i+1]))))

            if close:
                path = f'./close/{_sequence}/{target[0]}'
                os.makedirs(path, exist_ok=True)
                print('Time location：{} → {}'.format(files[i], files[i+1]))
                close_centrality(Graph).to_csv(os.path.join(path, 'close_' + target[0] + '_' + re.sub('.paj', '', os.path.basename(files[i]))
                                                                + '+' + re.sub('.paj', '.csv', os.path.basename(files[i+1]))))

            if between:
                path = f'./between/{_sequence}/{target[0]}'
                os.makedirs(path, exist_ok=True)
                print('Time location：{} → {}'.format(files[i], files[i+1]))
                between_centrality(Graph).to_csv(os.path.join(path, 'between_' + target[0] + '_' + re.sub('.paj', '', os.path.basename(files[i]))
                                                                + '+' + re.sub('.paj', '.csv', os.path.basename(files[i+1]))))

            if eigen:
                path = f'./eigen/{_sequence}/{target[0]}'
                os.makedirs(path, exist_ok=True)
                print('Time location：{} → {}'.format(files[i], files[i+1]))
                eigen_centrality(Graph).to_csv(os.path.join(path, 'eigen_' + target[0] + '_' + re.sub('.paj', '', os.path.basename(files[i]))
                                                                + '+' + re.sub('.paj', '.csv', os.path.basename(files[i+1]))))
            if cluster:
                print('Time location：{} → {}'.format(files[i], files[i+1]))
                print_clustering_value(Graph)

    
# クラスター係数
def print_clustering_value(Graph: object):
    print('クラスター係数：{}'.format(nx.average_clustering(Graph)))



if __name__ == '__main__':
    files = sorted(glob.glob('AnalysisData/**/*.paj'))

    pajek_to_net(files, target=['dev'], figure_x=50, figure_y=50, anotation=True, degree=True, close=True, between=True, print_graph=False)
    pajek_to_net(files, target=['bug'], figure_x=50, figure_y=50, anotation=True, degree=True, close=True, between=True, print_graph=False)
    pajek_to_net(files, target=['dev'], figure_x=50, figure_y=50, anotation=True, degree=True, close=True, between=True, sequence=True, print_graph=False)
    pajek_to_net(files, target=['bug'], figure_x=50, figure_y=50, anotation=True, degree=True, close=True, between=True, sequence=True, print_graph=False)