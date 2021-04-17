import matplotlib
#バックエンドを指定
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
import numpy as np
from . import keepaTime

#グラフ作成
def setPlt():
    x = ["07/01", "07/02", "07/03", "07/04", "07/05", "07/06", "07/07"]
    y = [3, 5, 0, 5, 6, 10, 2]
    plt.bar(x, y, color='#00d5ff')
    plt.title(r"$\bf{Running Trend  -2020/07/07}$", color='#3407ba')
    plt.xlabel("Date")
    plt.ylabel("km")

# SVG化
def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

def ParseCSV(csv, to_datetime = True):
    """

    Parses csv list from keepa into a python dictionary

    csv is organized as the following
        index   item
        0       Amazon Price
        1       Marketplace New
        2       Marketplace Used
        3       Sales Rank
        4       Listing Price
        5       Collectable Price
        11      New Offers
        12      Used Offers
        14      Collectable Offers
        16      Rating


    """

    # index in csv, key name, isfloat (is price)
    indices = [[0, 'AmazonPrice', True],
               [1, 'MarketplaceNew', True],
               [2, 'MarketplaceUsed', True],
               [3, 'SalesRank', False],
               [4, 'ListingPrice', True],
               [5, 'CollectablePrice', True],
               [11, 'NewOffers', False],
               [12, 'UsedOffers', False],
               [14, 'CollectableOffers', False],
               [16, 'Rating', False]]


    product_data = {}

    for index in indices:
        # Check if it exists
        ind = index[0]
        if csv[ind]:
            key = index[1]

            # Data goes [time0, value0, time1, value1, ...]
            product_data[key + '_time'] = keepaTime.KeepaMinutesToTime(csv[ind][::2], to_datetime)

            # Convert to float price if applicable
            if index[2]:
                product_data[key] = np.array(csv[ind][1::2], np.float)/100.0
            else:
                if index[1] == 'Rating':
                    product_data[key] = np.asarray(
                            csv[ind][1::2], np.float)/10.0
                else:
                    product_data[key] = np.asarray(csv[ind][1::2])

    return product_data



def PlotProduct(product, keys=[], rng=None):
    """ Plots a product using matplotlib """
    
    # if not plt_loaded:
    #     raise Exception('Plotting not available.  Check matplotlib install')

    # Use all keys if not specified
    if not keys:
        keys = product['data'].keys()
    
    # Create three figures, one for price data, offers, and sales rank

    pricefig, priceax = plt.subplots()
    pricefig.canvas.set_window_title('Product Price Plot')
    plt.title(product['title'])
    pricelegend = []

    offerfig, offerax = plt.subplots()
    offerfig.canvas.set_window_title('Product Offer Plot')
    plt.title(product['title'])
    offerlegend = []
    
    salesfig, salesax = plt.subplots()
    salesfig.canvas.set_window_title('Product Sales Rank Plot')
    plt.title(product['title'])
    saleslegend = []
    print(product['title'])
    # タイトル日本語化対応
    # https://qiita.com/yniji/items/3fac25c2ffa316990d0c
    # 上記に沿って下記の所を編集
    # Lib\\site-packages\\matplotlib\\mpl-data\\matplotlibrc'
    from matplotlib import rcParams
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
    # Add in last update time
    lstupdate = keepaTime.KeepaMinutesToTime(product['lastUpdate'])
        
    # Attempt to plot each key
    for key in keys:

        # Continue if key does not exist
        if key not in product['data'].keys():

            continue
        
        elif 'SalesRank' in key and not 'time' in key:
            x = np.append(product['data'][key + '_time'], lstupdate)
#            x = ConvertToDateTime(x)
            y = np.append(product['data'][key], product['data'][key][-1]).astype(np.float)
            ReplaceInvalid(y)
            salesax.step(x, y, where='pre')
            saleslegend.append(key)
        
        elif 'Offers' in key and not 'time' in key:
            x = np.append(product['data'][key + '_time'], lstupdate)
#            x = ConvertToDateTime(x)
            y = np.append(product['data'][key], product['data'][key][-1]).astype(np.float)
            ReplaceInvalid(y)
            offerax.step(x, y, where='pre')
            offerlegend.append(key)
            
        elif not 'time' in key:

            x = np.append(product['data'][key + '_time'], lstupdate)
#            x = ConvertToDateTime(x)
            y = np.append(product['data'][key], product['data'][key][-1]).astype(np.float)
            ReplaceInvalid(y)
            priceax.step(x, y, where='pre')
            pricelegend.append(key)
            
            # print(x)
            # print(y)
    

    # Add in legends or close figure
    if pricelegend:
        priceax.legend(pricelegend)
    else:
        plt.close(pricefig)
        
    if offerlegend:
        offerax.legend(offerlegend)
    else:
        plt.close(offerfig)
        
    if not saleslegend:
        plt.close(salesfig)
        
    # plt.show(block=True)
    # plt.draw()
    
def ReplaceInvalid(arr):
    """ Replace invalid data with nan """
#    mask = np.logical_not(np.isnan(arr))
    mask = arr < 0.0
    if mask.any():
        arr[mask] = np.nan

# 実行するビュー関数
def get_svg(request):
    import json

    with open('2021_01_2922_26_12.json') as f:
        df = json.load(f)
    product = df["products"][0]
    product["data"] = ParseCSV(product["csv"], False)
    PlotProduct(product)  
    svg = plt2svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response