from collections import defaultdict

from django import forms
from django.utils.translation import gettext as _

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = "__all__"
        exclude = [
            "updated_at",
            "created_at",
            "is_published",
            "are_the_preparation_steps_html",
            "author",
            'slug',
        ]
        widgets = {
            'cover': forms.FileInput(attrs={'class': "cover"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        self.add_attr({
            "preparation_steps": "preparation_steps",
        })

    def add_attr(self, fields_and_values: dict = {}):
        for field, class_value in fields_and_values.items():
            field_widget = self.fields.get(field).widget
            field_widget.attrs['class'] = class_value

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data: dict = self.cleaned_data
        title = cleaned_data.get("title")
        description = cleaned_data.get('description')

        if len(title) < 5:
            self._my_errors['title'].append(
                _("Title must have more at least 6 chars."))

        if description == title:
            self._my_errors['description'].append(
                _("Description can't be equal to title")
            )

        if self._my_errors:
            raise forms.ValidationError(self._my_errors)

        return super_clean
