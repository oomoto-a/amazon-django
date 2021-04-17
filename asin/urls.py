from django.urls import path
from asin.views.add_asin import ASINSettingView
from asin.views.exclude_asin import ExcludeASINView
from asin.views.exclude_word import ExcludeWordView
from asin.views.disp_asin_status import StatusView
from asin.views.disp_asin_result import ResultView
from asin.views.plot_asin import PlotAsin
from asin.views.plot import get_svg



app_name = 'asin'
urlpatterns = [
    path('add_asin/', ASINSettingView.as_view(), name="add_asin"),
    path('add_asin/<str:asin_group_id>', ASINSettingView.as_view(), name="edit_asin"),
    path('exclude_asin/', ExcludeASINView.as_view(), name="exclude_asin"),
    path('exclude_word/', ExcludeWordView.as_view(),  name="exclude_word"),
    path('disp_asin_status/', StatusView.as_view(),  name="disp_asin_status"),
    path('disp_asin_result/', ResultView.as_view(),  name="disp_asin_result"),
    path('disp_asin_result/<str:asin_group_id>', ResultView.as_view(),  name="disp_asin_result_group"),
    path('disp_asin_result/<str:asin_group_id>/download/', ResultView.download, name='download'),
    path('disp_plot/<int:id>', PlotAsin.as_view(),  name="plot_asin"),
    path('plot/<int:id>', get_svg, name='plot'),
    path('plot_select/<int:id>/<str:fbm>/<str:fba>/<str:cart>/', get_svg, name='plot_select')

]