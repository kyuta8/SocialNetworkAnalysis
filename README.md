# ソーシャルネットワーク分析（Pajek用）
## .pajファイルの読込みとグラフの出力と</br>ネットワークの時系列分析を目的としたノートブック

### 必要なパッケージ（追記：2022/10/17）
networkx == 2.8.7  
matplotlib == 3.5.2  
seaborn == 0.11.2  
pandas == 1.4.3  

``` pip install -r requirement.txt ```

### 実行方法（追記：2022/10/17）
1. rootディレクトリにpajファイルが含まれるフォルダを置く
2. 以下のコマンドを実行する  
``` python main.py ```

### 開発者とバグIDのネットワークを出力
開発者とバグIDのネットワークを出力したいときは，以下のように実行してください．

`
files = ['AnalysisData/2003_1-4/200301.paj']
print_net(files)
`

![ネットワーク例１](.picture/net1.png)

### 開発者のみ，またはバグIDのみのネットワークを出力（1-modeネットワーク）
開発者のみのネットワークを出力したいときは，以下のように実行してください．

`
files = ['AnalysisData/2003_1-4/200301.paj']
print_net(files, target=['dev'])
`

バグIDのみのネットワークを出力したいときは，以下のように実行してください．

`
files = ['AnalysisData/2003_1-4/200301.paj']
print_net(files, target=['bug'])
`

![ネットワーク例２](.picture/net2.png)

### 開発者，またはバグIDのネットワークを時系列に分析
開発者，またはバグIDのネットワークを時系列に分析したい場合は，以下のように実行してください．

`
files = ['AnalysisData/2003_1-4/200301.paj', 'AnalysisData/2003_1-4/200301.paj']
print_net(files, target=['dev'], sequence=True)
`

![ネットワーク例３](.picture/net3.png)

### ネットワークの出力に関係するパラメータ一覧（ print_net() ）

files：.pajの拡張子のファイルリスト（読み込みたいファイルが1つでもリスト形式で）  
target：1-modeネットワークを構築したいときに使う  

- dev：開発者のネットワーク
- bug：バグIDのネットワーク

figure_x：プロットの横幅  
figure_y：プロットの縦幅  
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
