from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class LogoutRequiredMixin(AccessMixin):
    """Verify that the current user is not authenticated"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:profile')
        return super().dispatch(request, *args, **kwargs)
