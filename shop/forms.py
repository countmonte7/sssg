from django import forms
from .models import Order
import json
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text
from django.template.loader import render_to_string
from django.conf import settings
from .mixins import IamportBaseForm


# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ('name', 'amount')
#         widgets = {
#             'name': forms.TextInput(attrs={'readonly':'readonly'}),
#             'amount': forms.TextInput(attrs={'readonly':'readonly'}),
#         }

class PayForm(IamportBaseForm):
    template_name = 'shop/_iamport.html'
    params_names = ['merchant_uid', 'name','amount']
    imp_fn_name = 'request_pay'
    class Meta:
        model = Order
        fields = ['imp_uid',]
        widgets = {
            'imp_uid': forms.HiddenInput,
        }

    def as_iamport(self):
        hidden_fields = mark_safe(''.join(smart_text(field) for field in self.hidden_fields()))
        fields = {
            'merchant_uid': str(self.instance.merchant_uid),
            'name': self.instance.name,
            'amount': self.instance.amount,
        }
        return hidden_fields + render_to_string('shop/_iamport.html', {
            'json_fields': mark_safe(json.dumps(fields, ensure_ascii=False)),
            'iamport_shop_id': settings.IAMPORT_SHOP_ID
        })
    
    def save(self):
        order = super().save(commit=False)
        order.update()
        order.status = 'paid'
        order.save()
        return order
        