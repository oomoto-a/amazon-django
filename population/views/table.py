from population.models import Population
import django_tables2 as tables
from asin.models.asin_group_id import AsinGroupId
from asin.const import Const
from django_tables2.utils import A
from population.models import Population

class StatusColumn(tables.Column):
    """
    ステータスの表示用カラム
    """
    def render(self, value):
        if value in Const.kEEPA_STATUS:
            return Const.kEEPA_STATUS[value]
        return value

class ButtonLinkColumn(tables.LinkColumn):
    """
    リンク表示用カラム(ボタン)
    """
    def render(self, record, value):
        if record.count > 0:
            # ステータス：完了
            return "データ表示"
        else:
            # ステータス：完了以外
            return ""
            
class PopulationTable(tables.Table):
    """
    人口画面用テーブル
    Population
    """
    prefectures = tables.Column(verbose_name="都道府県")
    #　リンク用
    plot = tables.LinkColumn("population:pop_plot", args=[A("prefectures_code")], 
                    verbose_name = "",text="詳細グラフ", 
                    attrs={"a": {"class": "btn btn-success text-nowrap"}} 
                    )



    class Meta:
        model = Population
        template_name = 'django_tables2/bootstrap4.html'
        # 表示する列column
        fields = ('prefectures',
                'plot',

        )    
        attrs = {"class": "table table-striped"}
