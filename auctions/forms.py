from django import forms
from .models import User, Categories, Bids, Listings, Comments
from django.utils.translation import gettext_lazy as _

# Include a form here to create a new listing
class CreateListingForm(forms.ModelForm):
    """A form for creating a new auction listing with options for:
    - Title
    - Description
    - Image (optional)
    - Starting bid
    - Category (optional)
    """
    title = forms.CharField(label="Title", max_length=64, required=True, widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control form-group'}))
    description = forms.CharField(label="Description", required=True, widget=forms.Textarea(attrs={'placeholder':'Item details', 'rows':'3', 'class':'form-control form-group'}))
    photo = forms.URLField(label="Image URL", required=False, widget=forms.TextInput(attrs={'placeholder': 'Photo URL', 'class': 'form-control form-group'}))
    starting_bid = forms.DecimalField(decimal_places=2, max_digits=8, widget=forms.NumberInput(attrs={'placeholder':'Initial Price', 'min':'0.01', 'step': '0.01', 'class': 'form-control form-group'}))
    category = forms.ChoiceField(choices=[(category.id, category.category_name) for category in Categories.objects.all()], required=False, label="Category", widget=forms.Select(attrs={'class': 'form-control form-group'})
    )

    class Meta:
        model = Listings
        fields = ["title", "description", "photo", "starting_bid", "category"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["content"]
        labels = {"content": _("")}
        widgets = {"content": forms.Textarea(attrs={"placeholder": "Add your comments", "rows":'1', "class":"form-control form-group"})}

