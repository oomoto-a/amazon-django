import matplotlib
#バックエンドを指定
matplotlib.use('agg')
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
import numpy as np
import datetime
import japanize_matplotlib
import seaborn as sns
from cycler import cycler
from population.models import Population
from matplotlib.ticker import ScalarFormatter

# SVG化
def plt_to_svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s




# 実行するビュー関数
def get_svg(request, id):
    # 都道府県コードで絞る
    population_datas = Population.objects.filter(prefectures_code=id)

    years = []
    man_data = []
    woman_data = []
    total_data = []

    for population_data in population_datas:
        years.append(population_data.year)
        man_data.append(population_data.man)
        woman_data.append(population_data.woman)
        total_data.append(population_data.population)


    """ プロット処理 """

    # スタイル設定
    sns.set()
    sns.set('talk', 'whitegrid', 'dark', font_scale=1.5,
    rc={"lines.linewidth": 2, 'grid.linestyle': '--'})
    
    # 日本語化 スタイル設定後にすること
    japanize_matplotlib.japanize()

    # サイズ設定
    fig = plt.figure(dpi=20, figsize=(24,12))
    ax1 = fig.add_subplot(1, 1, 1)
    # カラーサイクルを自作する場合は下記で対応
    # cmap = cycler('color', ['8dd3c7', 'feffb3', 'bfbbd9', 'fa8174', '81b1d2', 'fdb462', 'b3de69', 'bc82bd', 'ccebc4', 'ffed6f'])

    plt.title(population_datas[0].prefectures)
    # plt.xlabel('年', labelpad=30, rotation=0)

    axes = plt.axes()
    
    # plt.xticks(rotation =30)

    # 散布図のedgecolorsに使用 https://matplotlib.org/examples/color/colormaps_reference.html
    cmap = plt.get_cmap("tab20")
    pricelegend = []

    def add_data(years, y_data, marker, color):

        x = [int(s) for s in years]
        y = [int(s) for s in y_data]
        #　散布図
        ax =  plt.scatter(x,  y, facecolor='None',marker=marker,s=150, edgecolors=color, linewidth=3)
        # 折れ線(点入り)
        # plt.plot(x,y, 'rs:', color=color)
        # 折れ線
        # plt.plot(x,y, color=color)
        # ステッププロット 最初のイメージであげたパターン
        # plt.step(x,y,where='pre',color=color)

    #クラス設定  ※ScalarFormatterを継承
    class FixedOrderFormatter(ScalarFormatter):
        def __init__(self, order_of_mag=0, useOffset=True, useMathText=True):
            self._order_of_mag = order_of_mag
            ScalarFormatter.__init__(self, useOffset=useOffset, 
                                    useMathText=useMathText)
        def _set_order_of_magnitude(self):
            self.orderOfMagnitude = self._order_of_mag

    #10^x　表記にする
    # axes.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #
    axes.yaxis.set_major_formatter(FixedOrderFormatter(4 ,useMathText=True))
    axes.set_ylabel('(万人)', rotation=90)
    axes.set_xlabel('(年)', rotation=0)
    axes.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))

 

    add_data(years, total_data, "s", cmap(4) )
    pricelegend.append("全")
    add_data(years, man_data, "v", cmap(0))
    pricelegend.append("男")
    add_data(years, woman_data, "o", cmap(2))
    pricelegend.append("女")

    plt.legend(pricelegend)
    plt.show(block=True)
    plt.draw()

    svg = plt_to_svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response
