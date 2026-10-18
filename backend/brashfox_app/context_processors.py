from brashfox_app.models import AboutMe


def about_me_context(request):
    """
    Adds AboutMe instance to all template contexts.
    This allows footer and other templates to access social links
    without explicitly passing the context in every view.
    """
    try:
        about_me = AboutMe.get_instance()
        return {'about_me': about_me}
    except Exception:
        # Return empty dict if AboutMe doesn't exist yet
        return {'about_me': None}
