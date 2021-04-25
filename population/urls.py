from django.urls import path
from population.views.disp_pop import StatusView
from population.views.disp_pop_plot import PlotAsin
from population.views.plot_pop import get_svg



app_name = 'population'
urlpatterns = [
    path('pop_top/', StatusView.as_view(), name="pop_top"),
    path('pop_plot/', StatusView.as_view(), name="pop_top"),
    path('pop_plot/<int:id>', PlotAsin.as_view(),  name="pop_plot"),
    path('plot/<int:id>', get_svg, name='plot'),

]