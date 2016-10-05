from skaba.models import User, Event
import csv
from io import StringIO

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

def csv_user_import(csv_file, guild):
    # assume columns to be First name, Last name, e-mail, is_KV, is_TF, Password
    csvf = StringIO(csv_file.read().decode())
    csvreader = csv.DictReader(csvf, delimiter=';',
    	fieldnames=['firstname', 'lastname', 'email', 'is_kv', 'is_tf', 'password'])

    for row in csvreader:
        if row['password']:
            pw = row['password']
        else:
            pw = 'ISO2016'
        user = User.objects.create_user(username = generate_username(row['firstname'], row['lastname']),
            first_name = row['firstname'],
            last_name = row['lastname'],
            email = row['email'],
            password = pw
            )
        user.save()
        profile = user.profile
        profile.is_kv = row['is_kv'] == '1'
        profile.is_tf = row['is_tf'] == '1'
        profile.guild_id = guild
        profile.save()

    return True

def csv_event_import(csv_file, guild):
    # assume columns to be Event name, desc(fi), desc(en), desc(swe), Points, url, repeats, date
    csvf = StringIO(csv_file.read().decode())
    csvreader = csv.DictReader(csvf, delimiter=';',
    	fieldnames=['eventname', 'descfi', 'descen', 'descswe', 'points', 'url', 'repeats', 'date'])

    for row in csvreader:
        event = Event.objects.create(
            name = row['eventname'],
            description = str(row['descfi']) + "<br /><br />" + str(row['descen']) + "<br /><br />" + str(row['descswe']),
            points = row['points'],
            guild_id = guild,
            slug = row['url'],
            repeats = row['repeats'],
            date = row['date']
            )
        event.save()

    return True

    
def generate_username(first, last):
    name = first + '.' + last
    name = name.lower()
    if User.objects.filter(username=name).exists():
        name = generate_username(first, last + '1')
    return name


