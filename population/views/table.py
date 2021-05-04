from population.models import Population
import django_tables2 as tables
from asin.models.asin_group_id import AsinGroupId
from asin.const import Const
from django_tables2.utils import A
from population.models import Population

class PoplationColumn(tables.Column):
    """
    人口の表示用カラム
    """
    def render(self, value):
        return int(value)

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
    # prefectures_code = tables.Column(verbose_name="都道府県コード")
    prefectures = tables.Column(verbose_name="都道府県")
    #　リンク用
    plot = tables.LinkColumn("population:pop_plot", args=[A("prefectures_code")], 
                    verbose_name = "",text="詳細グラフ", 
                    attrs={"a": {"class": "btn btn-success text-nowrap"}} 
                    )
    population = PoplationColumn(verbose_name="総人口")
    man = PoplationColumn(verbose_name="人口(男性)")
    woman = PoplationColumn(verbose_name="人口(女性)")



    class Meta:
        model = Population
        template_name = 'django_tables2/bootstrap4.html'
        # 表示する列column
        fields = ('prefectures_code',
                'prefectures',
                'plot',
                'population',
                'man',
                'woman',

        )    
        attrs = {"class": "table table-striped"}
