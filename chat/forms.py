from django import forms


class ComposeForm(forms.Form):
	message = forms.CharField(
		widget=forms.TextInput(   # TextInput changed to TextArea
			attrs={
				"class": "form-control",
				"placeholder": "Type your message..."
				}
			)
		)

