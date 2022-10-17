import re
import networkx as nx

# ノードの色付け
COLOR = {
    "1" : "yellow",
    "2" : "blue"
}


def read_pajek_file(file: str, encoding='utf8'):
    """
        .pajファイルの読み込み
    """

    paj = ''  # Pajekファイルの読み込み用
    partition = []  # パーティション（開発者かバグIDか）のデータ格納用
    text = True  # 読み込むテキストが存在を判断
    flag = False  # ノード情報，ノードの属性情報の判断用

    with open(file, encoding=encoding, errors='ignore') as f:
        while text:
            l = f.readline()

            if '*Network' in l:
                pass

            elif '*Vertices' in l:
                if flag:
                    continue
                else:
                    num = re.findall(r'[0-9]+', l)
                    if len(num) >= 2:
                        l = re.sub(num[-1], '', l)    

            elif '*Partition' in l:
                flag = True
                continue

            if l:
                if flag:
                    l = re.sub('\n', '', l)
                    if COLOR.get(l):
                        color = COLOR[l]
                    else:
                        color = 'red'

                    partition.append(color)

                else:
                    paj += l
                    
            else:
                text = False

    return nx.parse_pajek(paj), partition