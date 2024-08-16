from django import forms


class SearchDishForm(forms.Form):
    search_string = forms.CharField(widget=forms.TextInput(attrs={
        "id": "search-input-id",
        "class": "i1ypu1yl",
        "value": "",
        "aria-label": "Поиск",
        "autocomplete": "off",
        "placeholder": "Найти блюдо"
    }))
