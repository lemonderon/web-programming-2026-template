from django import forms


class NewTaskForm(forms.Form):
    task = forms.CharField(label='New Task')
    priority = forms.IntegerField(min_value=1, max_value=10)

