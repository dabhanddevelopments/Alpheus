from django import forms
from django.forms.widgets import HiddenInput

from django.utils.safestring import mark_safe

class PlainTextWidget(forms.Widget):
   def render(self, name, value, attrs=None):
       return mark_safe("%s" %(value))
   
class FundMonthlyReturnForm(forms.Form):
    pk = forms.IntegerField(widget=HiddenInput, required=False)
    name = forms.CharField(widget=PlainTextWidget, required=False)
    nav1 = forms.DecimalField(widget=PlainTextWidget, decimal_places=2, required=False)
    weight = forms.DecimalField(widget=PlainTextWidget, decimal_places=2, required=False)
    nav2 = forms.DecimalField(decimal_places=2, required=False)
    return2 = forms.DecimalField(decimal_places=2, required=False)
    nav3 = forms.DecimalField(decimal_places=2, required=False)
    return3 = forms.DecimalField(decimal_places=2, required=False)
    ytd = forms.DecimalField(widget=PlainTextWidget, decimal_places=2, required=False)
    estimation2 = forms.CharField(widget=HiddenInput, required=False)
    estimation3 = forms.CharField(widget=HiddenInput, required=False)
    #flag = forms.BooleanField(widget=HiddenInput)
    total = forms.BooleanField(widget=HiddenInput, required=False)
    
