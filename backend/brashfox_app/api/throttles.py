from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class ContactFormThrottle(AnonRateThrottle):
    """
    Rate limit for contact form submissions.
    Prevents spam from anonymous users.
    """
    rate = 'contact'
    

class RegisterThrottle(AnonRateThrottle):
    """
    Rate limit for user registration.
    Prevents automated account creation.
    """
    rate = 'register'


class LoginThrottle(AnonRateThrottle):
    """
    Rate limit for login attempts.
    Prevents brute force attacks.
    """
    rate = 'login'
