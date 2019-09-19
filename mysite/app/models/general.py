from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

### To get the authenticated user https://stackoverflow.com/questions/2723052/how-to-get-the-list-of-the-authenticated-users
def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)

class General(models.Model):
    def get_cname(self):
        class_name = 'General'
        return class_name

    id = models.AutoField(primary_key=True) # Auto incrementation, unique

    DISABLED = '0'
    ENABLED = '1'
    STATE = [
        (DISABLED, 'DISABLED'),
        (ENABLED, 'ENABLED'),
    ]
    state = models.TextField(choices=STATE, default=ENABLED)
    creation = models.DateTimeField(default=timezone.now)
    last_modification = models.DateTimeField(default=timezone.now)
    #modifier = User.get_username

    def save(self, *args, **kwargs):
        self.last_modification = timezone.now()

        ### Get the user
        users=get_all_logged_in_users()
        user=''
        for e in users:
            user += str(e)

        ### Save the object
        super(General, self).save(*args, **kwargs)

        ### Create the action
        classes = self.get_cname()
        if classes != 'Action': #because we create an action and don't want an action to register that we created an action
            s = str(self.last_modification) + ' ' + user + ' modified or created element ' + str(self.id) + ' of class ' + self.get_cname()
            print(s)
            Action.objects.create(act=s)


#### ajouter eliminar et les get_name dans chaque classe
#
# def delete(self):
#     ### Get the user
#     users = get_all_logged_in_users()
#     user = ''
#     for e in users:
#         user += str(e)
#
#     ### Delete the object
#     super(self).delete()
#
#     ### Create the action
#     classes = self.get_cname()
#     if classes != 'Action':
#         s = str(self.last_modification) + user + ' deleted element ' + str(
#             self.id) + ' of class ' + self.get_cname()
#         print(s)
#         Action.objects.create(act=s)

class Action(General):
    act = models.TextField(default='')

    def get_cname(self):
        class_name = 'Action'
        return class_name

    def __str__(self):
        return str(self.act)




