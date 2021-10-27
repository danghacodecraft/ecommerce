from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from .models import *
from django.views.generic import ListView, CreateView, DeleteView, TemplateView
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def create_checkout_session(request, id):
    pass


class PaymentSuccessViews(TemplateView):
    pass


class PaymentFailView(TemplateView):
    pass


class OrderHistoryListView(ListView):
    pass


