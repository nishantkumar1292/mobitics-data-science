from django import forms

class ParamsForm(forms.Form):
    incoming_calls = forms.IntegerField(label='Incoming', min_value=1)
    outgoing_calls = forms.IntegerField(label='Outgoing', min_value=1)
    missed_calls = forms.IntegerField(label='Missed', min_value=0)
    blank_calls = forms.IntegerField(label='Blank', min_value=0)
