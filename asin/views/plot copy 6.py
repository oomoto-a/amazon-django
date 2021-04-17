import matplotlib
#バックエンドを指定
matplotlib.use('agg')
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
import numpy as np
from asin.models.keepa_info import KeepaInfo
import datetime
import japanize_matplotlib
import seaborn as sns
from cycler import cycler

keepa_st_ordinal = np.datetime64('2011-01-01')

def keepainutes_to_time(minutes):

    # timedelta64に変換。2011-01-01をベースにセット
    dt = np.array(minutes, dtype='timedelta64[m]')
    dt = dt + keepa_st_ordinal 

    # datetime
    return dt.astype(datetime.datetime)

# SVG化
def plt_to_svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

def parse_csv(csv, key, step_num, type="s", color="red"):

    product_data = {}
    if csv:
        # 時間を設定する
        product_data[key + '_time'] = keepainutes_to_time(csv[::step_num])

        # 金額を設定する
        product_data[key] = np.asarray(csv[1::step_num])

        # マーカーの形を設定する
        product_data[key + '_type'] = type

        # マーカーの色を設定する
        product_data[key + '_color'] = color

    return product_data

def plot_product(product, keys):
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
    # 散布図のedgecolorsに使用 https://matplotlib.org/examples/color/colormaps_reference.html
    i = 0
    cmap = plt.get_cmap("tab20")
    # カラーサイクルを自作する場合は下記で対応
    # cmap = cycler('color', ['8dd3c7', 'feffb3', 'bfbbd9', 'fa8174', '81b1d2', 'fdb462', 'b3de69', 'bc82bd', 'ccebc4', 'ffed6f'])
    plt.title(product['asin'])
    pricelegend = []
    plt.ylabel('円', labelpad=30, rotation=0)



    axes = plt.axes()
    
    # import matplotlib.dates as mdates
    # x軸の日付の表示形式設定
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
    # x軸の間隔（月単位）
    # plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    # x軸の日付の範囲設定
    # axes.set_xlim([startD, midD])
    plt.xticks(rotation =30)

    # キーの数だけ出力
    for key in keys:
        x = np.append(product['data'][key + '_time'], product['data'][key + '_time'][-1])
        y = np.append(product['data'][key], product['data'][key][-1]).astype(np.float)
        replace_invalid(y)
        #　散布図
        marker = product['data'][key+'_type']
        color = product['data'][key+'_color']
        ax =  plt.scatter(x,  y, facecolor='None',marker=marker,s=150, edgecolors=color, linewidth=3)
        # 折れ線
        # plt.plot(x,y, 'rs:', color=cmap(i))
        # plt.plot(x,y, color=cmap(i))

        # ステッププロット 最初のイメージであげたパターン
        # plt.step(x,y,where='pre',color=cmap(i))
        i = i + 1
        i = i + 1

        pricelegend.append(key)

    # 凡例追加 　ない場合はクローズ
    if pricelegend:
        # 凡例の表示(FBM等の表示)
        plt.legend(pricelegend)
    else:
        # 0件の場合
        plt.close()

    plt.show(block=True)
    plt.draw()

def replace_invalid(arr):
    """ Replace invalid data with nan """

    mask = arr < 0.0
    if mask.any():
        arr[mask] = np.nan

# 実行するビュー関数
def get_svg(request, id,fbm, fba, cart):
    keepaInfo = KeepaInfo.objects.filter(
        id = id, account_id = request.user).first()
    
    product_data = {}
    keys = []
    cmap = plt.get_cmap("tab20")
    fbm_bool = fbm=="True"
    if keepaInfo.lowest_history_fbm and fbm_bool:
        csv = str(keepaInfo.lowest_history_fbm).split(",")
        product_data.update(parse_csv(csv, "FBM", 3, "v", cmap(0)))
        keys.append("FBM")

    fba_bool = fba=="True"
    if keepaInfo.lowest_history_fba and fba_bool:
        csv = str(keepaInfo.lowest_history_fba).split(",")
        product_data.update(parse_csv(csv, "FBA", 2, "s", cmap(2)))
        keys.append("FBA")

    cart_bool = cart=="True"
    if keepaInfo.buy_box_history and cart_bool:
        csv = str(keepaInfo.buy_box_history).split(",")
        product_data.update(parse_csv(csv, "カート", 3, "o", cmap(4)))
        keys.append("カート")

    product = {}
    product["data"] = product_data
    product["asin"] = keepaInfo.asin
    plot_product(product, keys)  
    svg = plt_to_svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response
