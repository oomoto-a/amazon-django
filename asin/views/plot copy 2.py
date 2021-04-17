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

def keepaMinutesToTime(minutes, to_datetime=True):

    # Convert to timedelta64 and shift
    dt = np.array(minutes, dtype='timedelta64[m]')
    dt = dt + keepa_st_ordinal # shift from ordinal

    # Convert to datetime if requested
    if to_datetime:
        return dt.astype(datetime.datetime)
    else:
        return dt

# SVG化
def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

def ParseCSV(csv, index,to_datetime = True):
    # index in csv, key name, isfloat (日本円なのでfloat無し), isContainShipping
    indices = [[0, 'AmazonPrice', False, False],
               [1, 'MarketplaceNew', False, False],
               [2, 'MarketplaceUsed', False, False],
               [3, 'SalesRank', False, False],
               [4, 'ListingPrice', False, False],
               [5, 'CollectablePrice', False, False],
               [6, '', False, False],
               [7, 'FBM', False, True],#NewFbmShipping
               [8, '', False, False],
               [9, '', False, False],
               [10, 'FBA', False, False],#NewFba
               [11, 'NewOffers', False, False],
               [12, 'UsedOffers', False, False],
               [14, 'CollectableOffers', False, False],
               [16, 'Rating', False, False]]
    index = indices[index]
    step_num = 2
    if index[3]:
        # 送料込みである場合
        step_num = 3

    product_data = {}
    if csv:
        key = index[1]

        # Data goes [time0, value0, time1, value1, ...]
        product_data[key + '_time'] = keepaMinutesToTime(csv[::step_num], to_datetime)

        # Convert to float price if applicable
        if index[2]:
            product_data[key] = np.array(csv[1::step_num], np.float)/100.0
            print( product_data[key][0:10])
        else:
            if index[1] == 'Rating':
                product_data[key] = np.asarray(
                        csv[1::step_num], np.float)/10.0
            else:
                product_data[key] = np.asarray(csv[1::step_num])
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
    plt.title(product['asin'])
    pricelegend = []

    offerfig, offerax = plt.subplots()
    offerfig.canvas.set_window_title('Product Offer Plot')
    plt.title(product['asin'])
    offerlegend = []
    
    salesfig, salesax = plt.subplots()
    salesfig.canvas.set_window_title('Product Sales Rank Plot')
    plt.title(product['asin'])
    saleslegend = []
    # Add in last update time
    lstupdate = keepaMinutesToTime(product['lastUpdate'])
        
    # Attempt to plot each key
    for key in keys:

        # Continue if key does not exist
        if key not in product['data'].keys():

            continue
        
#         elif 'SalesRank' in key and not 'time' in key:
#             x = np.append(product['data'][key + '_time'], lstupdate)
# #            x = ConvertToDateTime(x)
#             y = np.append(product['data'][key], product['data'][key][-1]).astype(np.float)
#             ReplaceInvalid(y)
#             salesax.step(x, y, where='pre')
#             saleslegend.append(key)
        
#         elif 'Offers' in key and not 'time' in key:
#             x = np.append(product['data'][key + '_time'], lstupdate)
# #            x = ConvertToDateTime(x)
#             y = np.append(product['data'][key], product['data'][key][-1]).astype(np.float)
#             ReplaceInvalid(y)
#             offerax.step(x, y, where='pre')
#             offerlegend.append(key)
            
        elif not 'time' in key:

            x = np.append(product['data'][key + '_time'], lstupdate)
#            x = ConvertToDateTime(x)
            y = np.append(product['data'][key], product['data'][key][-1]).astype(np.float)
            ReplaceInvalid(y)
            priceax.step(x, y, where='pre')
            pricelegend.append(key)

    

    # Add in legends or close figure
    if pricelegend:
        print("XXXXXXXXXXXXXXX")
        priceax.legend(pricelegend)
    else:
        plt.close(pricefig)
        
    if offerlegend:
        print("YYYYYYYYYYYYYYYY")
        offerax.legend(offerlegend)
    else:
        plt.close(offerfig)
        
    if not saleslegend:
        print("ZZZZZZZZZZZZZZZ")
        plt.close(salesfig)
        
    plt.show(block=True)
    plt.draw()

def ReplaceInvalid(arr):
    """ Replace invalid data with nan """
#    mask = np.logical_not(np.isnan(arr))
    mask = arr < 0.0
    if mask.any():
        arr[mask] = np.nan

# 実行するビュー関数
def get_svg(request, id):
    keepaInfo = KeepaInfo.objects.filter(
        id = id, account_id = request.user).first()
    
    lastUpdate = 0
    product_data = {}
    # if keepaInfo.new_price_history:
    #     csv = str(keepaInfo.new_price_history).split(",")
    #     product_data = ParseCSV(csv, 1, False)
    #     lastUpdate = csv[-2]
    
    # if keepaInfo.used_price_history:
    #     csv = str(keepaInfo.used_price_history).split(",")
    #     product_data.update(ParseCSV(csv, 2, False))
    #     lastUpdate = csv[-2]
    
    if keepaInfo.lowest_history_fbm:
        csv = str(keepaInfo.lowest_history_fbm).split(",")
        product_data.update(ParseCSV(csv, 7, False))
        lastUpdate = csv[-2]
    
    if keepaInfo.lowest_history_fba:
        csv = str(keepaInfo.lowest_history_fba).split(",")
        product_data.update(ParseCSV(csv, 10, False))
        lastUpdate = csv[-2]
    
    product = {}
    product["data"] = product_data
    product["asin"] = keepaInfo.asin
    product["lastUpdate"] = lastUpdate
    PlotProduct(product)  
    # setPlt()
    svg = plt2svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response