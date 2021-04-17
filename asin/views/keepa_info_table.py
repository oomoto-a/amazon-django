from django.forms.fields import ImageField
import django_tables2 as tables
from django_tables2 import columns
from django_tables2.columns.base import Column
from asin.models.asin_group_id import AsinGroupId
from asin.models.keepa_info import KeepaInfo
from asin.const import Const
from django_tables2.utils import A
from django.utils.html import mark_safe
import ast
import datetime

            
class PriceColumn(tables.Column):
    """
    金額表示用カラム
    """
    def render(self, record, value):
        result = value
        if value == -1:
            result = "—"

        return result

class ReleaseDateColumn(tables.Column):
    """
    発売日表示用カラム
    """
    def render(self, record, value):
        result = ""
        if value == "-1":
            result = "—"
        else:
            result = datetime.datetime.strptime(value, '%Y%m%d').strftime("%Y/%m/%d")
        return result

class TitleColumn(tables.Column):
    """
    タイトル表示用カラム(リンク)
    """
    def render(self, record, value):
        href = "http://www.amazon.co.jp/dp/{}".format(record.asin)
        html = '<div style="width: 300px;"><a href="{}" target="_blank" rel="noopener noreferrer">{}</a></div>'
        html = html.format(href, value)

        return mark_safe(html)
            
class ImageColumn(tables.Column):
    """
    イメージ表示用カラム(リンク)
    """
    def render(self, record, value):
        href = "http://www.amazon.co.jp/dp/{}".format(record.asin)
        html = '<a href="{}" target="_blank" rel="noopener noreferrer">'
        html = html+'<img src="https://images-na.ssl-images-amazon.com/images/I/{}" style="max-height: 150px;"/></a>'
        html = html.format(href, value)

        return mark_safe(html)

class VariationsColumn(tables.Column):
    """
    バリエーション表示用カラム(メインテーブル)
    """
    def render(self, record, value):
        result = ""
        if value:
            val_json = ast.literal_eval(value)
            count = 0
            for val in val_json:
                count = count + len(val["attributes"])
            html = "バリエーション{}個".format(count)
            html = '<a href="#" onclick="dispVariationModal({});">{}</a>'.format(record.id, html)
            result = mark_safe(html) 

        return result


class ImageCsvColumn(tables.Column):
    """
    イメージカラム(CSV用)
    """
    def render(self, record, value):
        href = "https://images-na.ssl-images-amazon.com/images/I/{}".format(value)
        return href

class ItemCsvColumn(tables.Column):
    """
    商品リンクカラム(CSV用)
    """
    def render(self, record, value):
        href = "http://www.amazon.co.jp/dp/{}".format(value)
        return href

class VariationsCsvColumn(tables.Column):
    """
    バリエーションカラム(CSV用)
    """
    def render(self, record, value):
        result = ""
        if value:
            val_json = ast.literal_eval(value)
            for val in val_json:
                result = result + val["asin"] + "/"

        return result.rstrip("/")

class DivWrappedColumn(tables.Column):
    """
    幅指定用カラム
    """
    def __init__(self, width=None, *args, **kwargs):
        self.width=width
        super(DivWrappedColumn, self).__init__(*args, **kwargs)

     
    def render(self, value):
        return mark_safe('<div style="width: {}px;">'.format(self.width) +value+'</div>')

class KeepaInfoTable(tables.Table):
    """
    ASIN取得結果画面用テーブル
    KeepaInfoベース
    """
    title = TitleColumn(attrs={"td":{"style":"word-break: keep-all;"}})
    image = ImageColumn(attrs={"td": {"align": "center"}} )
    is_adult_product = columns.BooleanColumn(yesno="対象,対象外")
    variations = VariationsColumn( )
    lowest_price = PriceColumn()
    lowest_shipping = PriceColumn()
    lowest_price_fbm = PriceColumn()
    lowest_shipping_fbm = PriceColumn()
    lowest_price_fba = PriceColumn()
    buy_box_price = PriceColumn()
    buy_box_shipping = PriceColumn()
    top_category_name = DivWrappedColumn(width="150",attrs={"td":{"style":"word-break: keep-all;"}})
    sub_category_name = DivWrappedColumn(width="150",attrs={"td":{"style":"word-break: keep-all;"}})
    manufacturer = DivWrappedColumn(width="150",attrs={"td":{"style":"word-break: keep-all;"}})
    brand = DivWrappedColumn(width="150",attrs={"td":{"style":"word-break: keep-all;"}})
    list_price = PriceColumn()
    packageWeight = tables.Column(verbose_name="パッケージ重量(g)")
    packageHeight = tables.Column(verbose_name="パッケージ高さ(mm)")
    packageLength = tables.Column(verbose_name="パッケージ長さ(mm)")
    packageWidth = tables.Column(verbose_name="パッケージ幅(mm)")
    releaseDate = ReleaseDateColumn()
    plot = tables.LinkColumn("asin:plot_asin", args=[A("id")], 
                    verbose_name = "",text="価格グラフ", 
                    attrs={"a": {"class": "btn btn-success text-nowrap"}} 
                    )
    #plot = tables.TemplateColumn("<a href='/asin/disp_plot/{{ record.id }}' target='_blank'><input type='button' class='btn btn-success text-nowrap' value='価格グラフ' /></a>")
    
    class Meta:
        name = "keepaInfo"
        title = "keepaInfo"
        model = KeepaInfo
        template_name = 'django_tables2/bootstrap4.html'
        # 表示する列column
        fields = ('plot',
                'asin',
                'title',
                'image',
                'lowest_price',
                'lowest_shipping',
                'lowest_price_fbm',
                'lowest_shipping_fbm',
                'lowest_price_fba',
                'buy_box_price',
                'buy_box_shipping',
                'count_new',
                'top_category_id',
                'top_category_name',
                'sub_category_id',
                'sub_category_name',
                'sub_category_rank',
                'product_group',
                'manufacturer',
                'model',
                'brand',
                'packageWeight',
                'packageHeight',
                'packageLength',
                'packageWidth',
                'releaseDate',
                'list_price',
                'is_adult_product',
                'variations',
                )
        attrs = {"class": "table table-striped","th":{"class":"text-nowrap"}}

class VariationsTable(tables.Table):
    """
    ASIN取得結果画面用テーブル
    variationsベース
    """
    id = tables.Column(visible=True, 
            attrs={"td":{"class":"variations_id"},"th":{"class":"variations_id"}})
    asin = tables.Column(orderable=False, verbose_name="ASIN")
    dimension = tables.Column(orderable=False, verbose_name="型")
    value = tables.Column(orderable=False, verbose_name="値")
    class Meta:
        name = "VariationsTable"
        title = "VariationsTable"
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {"class": "table table-striped"}

class KeepaInfoCsv(KeepaInfoTable):
    """
    CSV用
    KeepaInfoTableを継承
    """
    title = tables.Column()
    image = ImageCsvColumn()
    variations = VariationsCsvColumn()
    item_link = ItemCsvColumn(accessor="asin" ,verbose_name="商品リンク")
    top_category_name = tables.Column()
    sub_category_name = tables.Column()
    manufacturer = tables.Column()
    brand = tables.Column()

