# from django.http import HttpResponse
#
#
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


from django.views.generic import TemplateView
from pygal.style import DarkStyle

from .charts import BrowserUsageHorizontalChart


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        # Instantiate our chart. We'll keep the size/style/etc.
        # config here in the view instead of `charts.py`.
        # cht_fruits = FruitPieChart(
        #     height=600,
        #     width=800,
        #     explicit_size=True,
        #     style=DarkStyle
        # )

        cht_browsers = BrowserUsageHorizontalChart(
            height=600,
            width=800,
            explicit_size=True,
            # style=DarkStyle
        )
        # Call the `.generate()` method on our chart object
        # and pass it to template context.
        # context['cht_fruits'] = cht_fruits.generate()
        context['cht_browsers'] = cht_browsers.generate()
        return context


class SingleView(TemplateView):
    template_name = 'ui-template/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(SingleView, self).get_context_data(**kwargs)
        context['sprint_completion'] = '89%'
        return context;

