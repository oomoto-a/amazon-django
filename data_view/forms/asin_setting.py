from django import forms
from django.forms.fields import ChoiceField
from django.forms import TextInput
from data_view.models.asin_setting import ASINSettingModel

class ASINSettingForm(forms.ModelForm):
    class Meta():
        model = ASINSettingModel
        fields = ('asin_group_id', 'asin')

        # テキストエリアのサイズ変更
        widgets = {
            'asin': forms.Textarea(attrs={'rows': 20, 'cols': 80}),
        }

