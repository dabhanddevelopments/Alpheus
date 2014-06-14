from django import forms
from django.forms.widgets import HiddenInput, TextInput

from django.utils.safestring import mark_safe

class PlainTextWidget(forms.Widget):
   def render(self, name, value, attrs=None):
       return mark_safe("%s" %(value))
   
class FundMonthlyReturnForm(forms.Form):
    pk1 = forms.IntegerField(widget=HiddenInput, required=False)
    pk2 = forms.IntegerField(widget=HiddenInput, required=False)
    fund = forms.IntegerField(widget=HiddenInput, required=False)
    name = forms.CharField(widget=PlainTextWidget, required=False)
    return1 = forms.DecimalField(widget=TextInput(attrs={'size':'2'}), decimal_places=2, required=False)
    return2 = forms.DecimalField(widget=TextInput(attrs={'size':'2'}), decimal_places=2, required=False)
    estimation1 = forms.BooleanField(widget=HiddenInput, required=False)
    estimation2 = forms.BooleanField(widget=HiddenInput, required=False)
    group = forms.BooleanField(widget=HiddenInput, required=False)
    
