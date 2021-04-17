import django_tables2 as tables
from asin.models.asin_group_id import AsinGroupId
from asin.const import Const
from django_tables2.utils import A


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
            
class AsinGroupIdTable(tables.Table):
    """
    ASIN取得状況画面用テーブル
    AsinGroupIdベース
    """
    asin_group_id = tables.LinkColumn("asin:edit_asin",args=[A("asin_group_id")], verbose_name="ASINグループID")
    status = StatusColumn()
    create_date = tables.DateTimeColumn(format="Y/m/d G:i:s")
    complete_date = tables.DateTimeColumn(format="Y/m/d G:i:s")
    #　リンク用
    button = ButtonLinkColumn("asin:disp_asin_result_group", args=[A("asin_group_id")], 
                    verbose_name = "",text="データ表示", 
                    attrs={"a": {"class": "btn btn-success"}} 
                    )
    class Meta:
        model = AsinGroupId
        template_name = 'django_tables2/bootstrap4.html'
        # 表示する列column
        fields = ('asin_group_id',
                'asin_count',
                'create_date',
                'status',
                'complete_date',
        )    
        attrs = {"class": "table table-striped"}
