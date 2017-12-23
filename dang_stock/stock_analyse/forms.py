from django import forms

class StockForms(forms.Form):
    Symbol     = forms.CharField(max_length=10)
    start_date = forms.CharField(max_length=10)
    end_date   = forms.CharField(max_length=10)