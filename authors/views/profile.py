from django.views.generic.base import TemplateView
from authors.models import Profile
from django.shortcuts import get_object_or_404


class ProfileView(TemplateView):
    template_name = "authors/pages/profile.html"

    def get(self, request, *args, **kwargs):
        profile_id = kwargs.get('id')
        profile = get_object_or_404(
            Profile.objects.filter(id=profile_id).select_related("author"),
            id=profile_id
        )

        return self.render_to_response({
            "profile": profile
        })
