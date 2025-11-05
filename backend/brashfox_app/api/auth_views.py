from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


# Simplified versions without throttling (can be added later with proper cache setup)
class ThrottledTokenObtainPairView(TokenObtainPairView):
    """
    JWT Token obtain view.
    Note: Throttling disabled - requires cache backend for production use.
    """
    pass


class ThrottledTokenRefreshView(TokenRefreshView):
    """
    JWT Token refresh view.
    Note: Throttling disabled - requires cache backend for production use.
    """
    pass
