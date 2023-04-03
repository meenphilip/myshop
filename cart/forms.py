from django import forms

# Allow for selection from 1 to 20
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


# Add product to cart form
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)

    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
