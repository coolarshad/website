from django import template
from django.shortcuts import render
from home.models import *

t=None
t2=None
t3=None
t4=None
register=template.Library()

@register.simple_tag
def ObjectData(obj):
    global t
    t=TradeApproval()
    t=obj

    return t

@register.simple_tag
def temp():
    global t
    return t

@register.simple_tag
def SP(obj):
    global t2
    global t3
    global t4
    t2=SalesAndPurchase.objects.get(trn=obj)
    t3=PrePayments.objects.get(trn=obj)
    t4=obj
    return t2,t3,t4

@register.simple_tag
def tempsp():
    global t2
 
    return t2

@register.simple_tag
def temppre():
    global t3
 
    return t3

@register.simple_tag
def tempobj():
    global t4
 
    return t4

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)