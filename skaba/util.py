from skaba.models import User

"""
Check if user has admin status.
"""
def check_admin(user):
    if (user.is_authenticated() and (user.profile.role == "admin") or (user.is_superuser)):
        return True
    return False

"""
Check if user has moderator status.
"""
def check_moderator(user):
    if (user.is_authenticated() and (user.profile.role == "moderator" \
    	or user.profile.role == 'admin' \
    	or user.is_superuser)):
        return True
    return False

