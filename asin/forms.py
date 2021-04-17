from django import forms
import re
from asin.const import Const

class AlphNumericField(forms.CharField):
    def clean(self, value):
        m = re.fullmatch(r'^[0-9a-zA-Z]*$', value)
        if m is None:
            raise forms.ValidationError('半角英数のみで入力して下さい')
        return super().clean(value)

class AsinsField(forms.CharField):
    def clean(self, value):
        if len(value) == 0:
            # 除外画面で0文字の場合、true
            # 入力必須の画面ではrequiredのため、0文字はあり得ない
            return super().clean(value)

        asin_list = value.split("\r\n")
        try:
            asin_list = list(filter(lambda a: a != '', asin_list))
        except:
            pass
        #件数チェック
        if len(asin_list) > Const.ASIN_MAX_LIMIT:
            raise forms.ValidationError('{}件以内で入力して下さい（入力件数{}）'.format(Const.ASIN_MAX_LIMIT, len(asin_list)) )

        #形式チェック
        type_message_array = []

        for asin in asin_list:
            # asin = asin.strip('\t').strip()
            m = re.fullmatch(r'^[0-9a-zA-Z]{10}', asin)
            if m is None:
                # 件数が多すぎると表示がおかしくなるのを考慮して10件
                if len(type_message_array) < 10:
                    type_message_array.append(asin)
                    continue
                    
            # if len(asin) != 10:
            #     if len(type_message_array) < 10:
            #         type_message_array.append(asin)

        if len(type_message_array) > 0:
            message = "ASINは半角英数10桁で入力して下さい（10件まで表示します）。{}".format(",".join(type_message_array))
            raise forms.ValidationError(message)
            
        return super().clean(value)


class AsinsForm(forms.Form):
    asin_group_id = forms.CharField(label='ASINグループID',  max_length=100)
    asins = AsinsField(label='ASIN一覧', widget=forms.Textarea(attrs={'cols': '80', 'rows': '10'}))
    # submitボタンの表示制御
    submit = "submit"

class AsinsDisableForm(forms.Form):
    asin_group_id = forms.CharField(label='ASINグループID',  max_length=100, disabled='disabled')
    asins = AsinsField(label='ASIN一覧', disabled='disabled', widget=forms.Textarea(attrs={'cols': '80', 'rows': '10'}))
    # submitボタンの表示制御
    submit = ""

class ExclusionAsinsForm(forms.Form):
    asins = AsinsField(label='除外ASIN一覧', required=False, 
            widget=forms.Textarea(attrs={
                'class': 'textarea-wide form-control'
                }))

class ExclusionWordForm(forms.Form):
    word = forms.CharField(label='除外ワード', required=False, 
            widget=forms.Textarea(attrs={
                'class': 'textarea-wide form-control'
                }))

class ResultFilterForm(forms.Form):
    asin_group_id = forms.fields.ChoiceField(
        label='ASINグループID',
        required=True,
        widget=forms.widgets.Select(
            attrs={'class':'form-control','style':'width: fit-content;'}
        )
    )
    hidden_asin_group_id = forms.CharField()
    lowest_price_start = forms.CharField()
    lowest_price_end = forms.CharField()
    lowest_price_fbm_start = forms.CharField()
    lowest_price_fbm_end = forms.CharField()
    lowest_price_fba_start = forms.CharField()
    lowest_price_fba_end = forms.CharField()

class PlotForm(forms.Form):
    fbm = forms.BooleanField(
        label='FBM',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'check form-check-input','id':'fbm_checkbox'}),
    )
    fba = forms.BooleanField(
        label='FBA',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'check form-check-input','id':'fba_checkbox'}),
    )
    cart = forms.BooleanField(
        label='カート',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'check form-check-input','id':'cart_checkbox'}),
    )
