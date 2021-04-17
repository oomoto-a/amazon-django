from django.shortcuts import render
from django_tables2 import SingleTableView
from asin.models.keepa_info import KeepaInfo
from . import keepa_info_table
from asin.forms import ResultFilterForm
from django_tables2 import RequestConfig 
import ast
from django.shortcuts import redirect
import sys
import csv
from django.http import HttpResponse
from datetime import datetime
from django.http import StreamingHttpResponse
from asin.const import Const

class Echo:
    """
    ファイル書き込み用のクラス
    """
    def write(self, value):
        return value

class ResultView(SingleTableView):
    model = KeepaInfo
    table_class = keepa_info_table.KeepaInfoTable
    per_page = Const.PAGE_PER_DEFAULT
    template_name = "asin/disp_asin_result.html" 
    form_class = "ResultFilterForm"
    
    def create_keepa_info(self, request, asin_group_id):
        """
        keepaInfo作成
        """
        def createStartEnd(start,end):
            """
            検索条件のスタート・エンドを返す
            """
            resultStart = start
            resultEnd = end
            if start == "" or start is None:
                resultStart = -1
            if end == "" or end is None:
                resultEnd = sys.maxsize
            return [resultStart, resultEnd]

        # 価格
        lowest_condition = createStartEnd(request.GET.get("lowest_price_start"), request.GET.get("lowest_price_end"))
        lowest_price_start = lowest_condition[0]
        lowest_price_end = lowest_condition[1]
        # Fmb
        lowest_condition_fmb = createStartEnd(request.GET.get("lowest_price_fbm_start"), request.GET.get("lowest_price_fbm_end"))
        lowest_price_fbm_start = lowest_condition_fmb[0]
        lowest_price_fbm_end = lowest_condition_fmb[1]
        # Fma
        lowest_condition_fma = createStartEnd(request.GET.get("lowest_price_fba_start"), request.GET.get("lowest_price_fba_end"))
        lowest_price_fba_start = lowest_condition_fma[0]
        lowest_price_fba_end = lowest_condition_fma[1]

        keepaInfo = KeepaInfo.objects.filter(
            account_id = request.user, 
            asin_group_id = asin_group_id,
            lowest_price__gte=lowest_price_start,
            lowest_price__lte=lowest_price_end,
            lowest_price_fbm__gte=lowest_price_fbm_start,
            lowest_price_fbm__lte=lowest_price_fbm_end,
            lowest_price_fba__gte=lowest_price_fba_start,
            lowest_price_fba__lte=lowest_price_fba_end,
            )
        
        return keepaInfo

    def create_params(self, user, request, asin_group_id, keepaInfo):
        """
        params作成
        """
        # select設定
        form = ResultFilterForm(initial = {"hidden_asin_group_id" : asin_group_id})
        keepaInfos = KeepaInfo.objects.values_list("asin_group_id").filter(account_id=user).distinct()
        choice_values = []
        for value in keepaInfos:
            choice_values.append((value[0], value[0]))

        form.fields['asin_group_id'].choices = choice_values

        keepaInfo = self.create_keepa_info(request, asin_group_id)

        table1 = keepa_info_table.KeepaInfoTable(keepaInfo)
        RequestConfig(request, paginate={"per_page": self.per_page}).configure(table1)


        datas = []
        for rowData in keepaInfo:
            if not rowData.variations:
                #variationsが無い場合は次のレコードへ
                continue
    
            variations_json = ast.literal_eval(rowData.variations)
            for variation in variations_json:

                for attribute in variation["attributes"]:
                    datas.append({"id": rowData.id, 
                            "asin":variation["asin"], 
                            "dimension":attribute["dimension"], 
                            "value":attribute["value"], 
                            })

        return {'form': form, 'table' : table1, 
        'table2': keepa_info_table.VariationsTable(datas), 'modal' : 'disp_asin_result',
        'parameter' : '?'+request.GET.urlencode()}

    def get(self, request, *args, **kwargs):

        keepaInfo = None
        asin_group_id = request.GET.get("asin_group_id")
        if asin_group_id is None:
            asin_group_id = kwargs["asin_group_id"] 

        params = self.create_params(request.user, request,asin_group_id, keepaInfo)
        # params['table'] = table1

        return render(request, self.template_name, params)

    # データのダウンロード
    def download(request, asin_group_id):
        # レスポンスの設定
        response = HttpResponse(content_type='text/csv; charset=utf-8_sig')
        dt_now = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = 'data_{}.csv'.format(dt_now)  # ダウンロードするcsvファイル名
        keepaInfo = ResultView().create_keepa_info(request, asin_group_id)
        csvTables=keepa_info_table.KeepaInfoCsv(keepaInfo)

        # response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        # writer = csv.writer(response)
        # # as_valuesでヘッダーも取れるのでそのまま出力
        # for csvTable in csvTables.as_values():
        #         writer.writerow(csvTable)

        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in csvTables.as_values(exclude_columns="plot")),
                                        content_type="text/csv; charset=utf-8_sig")
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        return response