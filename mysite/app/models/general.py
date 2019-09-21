from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
#from .reservation_classes import Reservation,PaymentReservation,LineReservation

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

        ### Get the Class
        classes = self.get_cname()
        print('detected classe' + classes)
        # auto = '' #='' if the action has been made by the user and 'automatic action' if it is an automatic saving in another function
        if classes == 'Task':
            self.assigner_auto = user
            print(user+' registered as assigner of task')

        ### Update the PaymentState
        if classes == 'LineReservation':
            this_reservation = self.line_reservation
            # auto = \
            self.updt_payment_state(this_reservation)

        elif classes == 'PaymentReservation':
            this_reservation = self.payment_reservation
            # auto = \
            self.updt_payment_state(this_reservation)

        ### Save the object
        super(General, self).save(*args, **kwargs)


        ### Create the action
        if classes != 'Action': #because we create an action and don't want an action to register that we created an action
            s = str(self.last_modification) + ' ' + user + ' modified or created element ' + str(self.id) + ' of class ' + self.get_cname()
            print('Registered Action' +s)
            #Action.objects.create(act=auto + s)
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

class Task(General):
    description = models.TextField(default='')
    assigned_date = models.DateField(default=timezone.now) #readonly
    delivery_date = models.DateField(blank=True, null=True)
    cause = models.TextField(blank=True, null=True)
    assigner_auto = models.CharField(max_length=100, null=True, blank=True)

    ### KEYS
    assigned_user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            null=True
        )

    def get_cname(self):
        class_name = 'Task'
        return class_name

    def __str__(self):
        return str(self.description)





