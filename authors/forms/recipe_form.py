from django import forms
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

    def add_attr(self, fields_and_values: dict = {}):
        for field, class_value in fields_and_values.items():
            field_widget = self.fields.get(field).widget
            field_widget.attrs['class'] = class_value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_attr({
            "preparation_steps": "preparation_steps",
        })
