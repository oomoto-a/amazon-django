from population.models import Population
import django_tables2 as tables
from django_tables2.utils import A
from population.models import Population
from django.db.models.functions import Abs

class PopulationTable(tables.Table):
    """
    人口画面用テーブル
    Population
    """
    prefectures = tables.Column(verbose_name="都道府県")
    #　リンク用
    plot = tables.LinkColumn("population:pop_plot", args=[A("prefectures_code")], 
                    verbose_name = "",text="人口グラフ", 
                    attrs={"a": {"class": "btn btn-success text-nowrap"}} 
                    )
    population = tables.Column(verbose_name="総人口")
    man = tables.Column(verbose_name="人口(男性)")
    woman = tables.Column(verbose_name="人口(女性)")


    def order_prefectures_code(self, queryset, is_descending):
        queryset = queryset.annotate(
            abs=Abs("prefectures_code")
        ).order_by(("-" if is_descending else "") + "abs")
        return (queryset, True)

    def order_population(self, queryset, is_descending):
        queryset = queryset.annotate(
            abs=Abs("population")
        ).order_by(("-" if is_descending else "") + "abs")
        return (queryset, True)

    def order_man(self, queryset, is_descending):
        queryset = queryset.annotate(
            abs=Abs("man")
        ).order_by(("-" if is_descending else "") + "abs")
        return (queryset, True)

    def order_woman(self, queryset, is_descending):
        queryset = queryset.annotate(
            abs=Abs("woman")
        ).order_by(("-" if is_descending else "") + "abs")
        return (queryset, True)

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
