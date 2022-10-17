import itertools
import pandas as pd


def to_mode_1_net(node: list, edge: list, partition: list, target: list):
    """
        2-modeから1-modeへネットワークの変換
    """

    nodes = node
    edges = pd.DataFrame(edge, columns = ['target', 'source', 'other'])
    edges.drop(columns = ['other'], inplace = True)

    dev = []  # 開発者情報の格納用
    dev_edge = []  # 開発者の繋がり
    dev_net = []  # 開発者のノード，エッジ情報の格納用
    bug_id = []  # バグID情報の格納用
    bug_id_edge = []  # バグIDの繋がり
    bug_id_net = []  # バグIDのノード，エッジ情報の格納用

    #　開発者，バグ報告書にノードを分割
    [dev.append(nodes[i]) if partition[i] == 'yellow' else bug_id.append(nodes[i]) for i in range(len(partition))]

    if 'dev' in target:
        #　開発者ネットワーク構築のためのエッジ抽出
        for i in range(len(bug_id)):
            # 各バグIDに紐づいている開発者を抽出
            b_id = bug_id[i]
            bug_in_edge = edges.query('@b_id == target or @b_id == source')
            bug_in_edge = bug_in_edge['target'].tolist()
            dev_link = set(bug_in_edge) - set(b_id)
            # バグIDに紐づいていた開発者同士でエッジを結ぶ
            dev_edge.extend(itertools.product(dev_link, dev_link))
            # 使用したバグIDは取り除く
            edges = edges.query('@b_id != target or @b_id != source')

    if 'bug' in target:
        #　バグ報告書ネットワーク構築のためのエッジ抽出
        for i in range(len(dev)):
            # 各開発者に紐づいているバグIDを抽出
            d = dev[i]
            dev_in_edge = edges.query('@d == target or @d == source')
            dev_in_edge = dev_in_edge['source'].tolist()
            bug_link = set(dev_in_edge) - set(d)
            # 開発者に紐づいていたバグID同士でエッジを結ぶ
            bug_id_edge.extend(itertools.product(bug_link, bug_link))
            # 使用した開発者は取り除く
            edges = edges.query('@d != target or @d != source')

    if 'dev' in target:
        dev_net = [dev, dev_edge]
        return dev_net

    elif 'bug' in target:
        bug_id_net = [bug_id, bug_id_edge]
        return bug_id_net

    elif 'dev' in target and 'bug' in target:
        dev_net = [dev, dev_edge]
        bug_id_net = [bug_id, bug_id_edge]
        return dev_net, bug_id_net