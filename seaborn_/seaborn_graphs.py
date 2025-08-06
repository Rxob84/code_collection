"""

2019/4/12

author  @hik0107

https://qiita.com/hik0107/items/3dc541158fceb3156ee0

"""

import seaborn as sns
import numpy as np
import pandas as pd
from urllib import request
import matplotlib.pyplot as plt

x = np.random.normal(size=100)

# 社内用プロキシの設定。seabornが内部でurllibを使っていたので、下記で設定。
# https://qiita.com/gazami/items/4b42371ed831c159fb04
proxy = "XXX"
opener = request.build_opener(proxy)
request.install_opener(opener)


# seabornにはいくつかデータセットがあるらしい。
titanic = sns.load_dataset("titanic")  # kaggleのタイタニック　生存者データ
tips = sns.load_dataset("tips")         # お店の食事時間、会計総額、チップのデータ
iris = sns.load_dataset("iris")         # アヤメの統計データ

# いい感じの設定
sns.set()
sns.set_style("whitegrid", {'grid.linestyle': '--'})
sns.set_context("paper", 1.5, {"lines.linewidth": 4})
sns.set_palette("winter_r", 8, 1)
sns.set('talk', 'whitegrid', 'dark',
        rc={"lines.linewidth": 2, 'grid.linestyle': '--'})

# histogram
plt.savefig("histogram.png")
plt.show()  # グラフ表示のために追加

# joint plot
sns.jointplot("sepal_width", "petal_length", data=iris)
plt.savefig("joint_plot.png")
plt.show()

# pair plot
sns.pairplot(data=iris)
plt.savefig("pair_plt.png")
plt.show()

# pair plot 2
sns.pairplot(data=iris, hue="species")
plt.savefig("pair_plot2.png")
plt.show()
