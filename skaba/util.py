from skaba.models import UserProfile, Attendance, Guild, Event
from django.shortcuts import render, render_to_response, redirect, get_object_or_404

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
