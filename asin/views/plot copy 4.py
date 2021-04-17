import matplotlib
#バックエンドを指定
matplotlib.use('agg')
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
import numpy as np
from asin.models.keepa_info import KeepaInfo
import datetime

keepa_st_ordinal = np.datetime64('2011-01-01')

def keepainutes_to_time(minutes, to_datetime=True):

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

def plt2png():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=200)
    s = buf.getvalue()
    buf.close()
    return s

def parse_csv(csv, key,step_num, to_datetime = True):

    product_data = {}
    if csv:
        # 時間を設定する
        product_data[key + '_time'] = keepainutes_to_time(csv[::step_num], to_datetime)

        # 金額を設定する
        product_data[key] = np.asarray(csv[1::step_num])
    return product_data

def plot_product(product):
    """ Plots a product using matplotlib """

    # キー作成
    keys = product['data'].keys()
    
    # Create three figures, one for price data, offers, and sales rank

    pricefig, priceax = plt.subplots()
    pricefig.canvas.set_window_title('Product Price Plot')
    plt.title(product['asin'])
    pricelegend = []

    lstupdate = keepainutes_to_time(product['lastUpdate'])
        
    # キーの数だけ出力
    for key in keys:

        # キー値のチェック
        if key not in product['data'].keys():
            continue
        elif not 'time' in key:

            x = np.append(product['data'][key + '_time'], lstupdate)
            y = np.append(product['data'][key], product['data'][key][-1]).astype(np.float)
            replace_invalid(y)
            priceax.step(x, y, where='pre')
            pricelegend.append(key)
    
    # Add in legends or close figure
    if pricelegend:
        priceax.legend(pricelegend)
    else:
        plt.close(pricefig)


    plt.show(block=True)
    plt.draw()

def replace_invalid(arr):
    """ Replace invalid data with nan """

    mask = arr < 0.0
    if mask.any():
        arr[mask] = np.nan

# 実行するビュー関数
def get_svg(request, id):
    keepaInfo = KeepaInfo.objects.filter(
        id = id, account_id = request.user).first()
    
    lastUpdate = 0
    product_data = {}

    if keepaInfo.lowest_history_fbm:
        csv = str(keepaInfo.lowest_history_fbm).split(",")
        product_data.update(parse_csv(csv, 'FBM', 3))
        lastUpdate = csv[-2]
    
    if keepaInfo.lowest_history_fba:
        csv = str(keepaInfo.lowest_history_fba).split(",")
        product_data.update(parse_csv(csv, 'FBA', 2))
        lastUpdate = csv[-2]
    
    product = {}
    product["data"] = product_data
    product["asin"] = keepaInfo.asin
    product["lastUpdate"] = lastUpdate
    plot_product(product)  
    # svg = plt_to_svg()  #SVG化
    # plt.cla()  # グラフをリセット
    # response = HttpResponse(svg, content_type='image/svg+xml')
    # return response

    png = plt2png()
    plt.cla()
    response = HttpResponse(png, content_type='image/png')
    return response