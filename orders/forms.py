from django import forms
from .models import ShippingAddress


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9)

class CouponForm(forms.Form):
    code = forms.CharField(max_length=30)

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'postalCode']

    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
