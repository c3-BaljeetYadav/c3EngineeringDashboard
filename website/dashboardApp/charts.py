import pygal

from .models import Fruit


# class FruitPieChart():
#
#     def __init__(self, **kwargs):
#         self.chart = pygal.Pie(**kwargs)
#         self.chart.title = 'Amount of Fruits'
#
#     def get_data(self):
#         '''
#         Query the db for chart data, pack them into a dict and return it.
#         '''
#         data = {}
#         for fruit in Fruit.objects.all():
#             data[fruit.name] = fruit.amt
#         return data
#
#     def generate(self):
#         # Get chart data
#         chart_data = self.get_data()
#
#         # Add data to chart
#         for key, value in chart_data.items():
#             self.chart.add(key, value)
#
#         # Return the rendered SVG
#         return self.chart.render(is_unicode=True)


class BrowserUsageHorizontalChart():
    def __init__(self, **kwargs):
        self.chart = pygal.Line(**kwargs)
        self.chart.title = 'Browser Usage Evolution'
        self.chart.x_labels = map(str, range(2002, 2013))

    def generate(self):
        self.chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
        self.chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
        self.chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
        self.chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
        self.chart.range = [0, 100]
        return self.chart.render(is_unicode=True)
