from django.shortcuts import render
import pandas as pd
from analysis.utils import *
import os
from django.conf import settings


def work_with_chart(request):
    data_seconds = pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'analysis/dataset.xlsx'), sheet_name='Wait_times')
    hist = get_hist(data_seconds, 'seconds', 'Customer Wait Time')
    context = {'hist': hist}
    return render(request, 'analysis/work_with_chart.html', context)
