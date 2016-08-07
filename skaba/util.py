"""""""""""""""""""""""""""""""""""
"These don't work yet as intended!"
"""""""""""""""""""""""""""""""""""

"""
Check if user has admin status.
"""
def check_admin(user):
    if (user.role == "admin"):
        return True
    return False

"""
Check if user has moderator status.
"""
def check_mod(user):
    if (user.role == "mod"):
        return True
    return False
