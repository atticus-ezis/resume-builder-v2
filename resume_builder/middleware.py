from django.utils.deprecation import MiddlewareMixin


class CSRFExemptAPILoginMiddleware(MiddlewareMixin):
    """
    Middleware to exempt the login API endpoint from CSRF checks.
    This allows login without CSRF tokens while keeping CSRF protection for other endpoints.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Exempt login endpoint from CSRF
        # Check both with and without trailing slash, and check view class name as backup
        login_paths = ["/api/accounts/login/", "/api/accounts/login"]
        if request.path in login_paths or (
            hasattr(view_func, "view_class")
            and view_func.view_class.__name__ == "CSRFExemptLoginView"
        ):
            setattr(request, "_dont_enforce_csrf_checks", True)
        return None
