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

def get_all_logged_in_users(): ###comment on 1st launch beacuse sessions does not exist
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


    def save(self, *args, **kwargs):
        self.last_modification = timezone.now()

        ### Get the user
        users=get_all_logged_in_users()
        user=''
        for e in users:
            user += str(e)

        ### Get the Class
        classes = self.get_cname()
        print('detected classe ' + classes)
        # auto = '' #='' if the action has been made by the user and 'automatic action' if it is an automatic saving in another function
        if classes == 'Task':
            self.assigner_auto = user
            print(user+' registered as assigner of task')


        ### Save the object
        super(General, self).save(*args, **kwargs) ### to create the other classes

        if classes == 'LineReservation':

            # auto = \
            self.updt_payment_state()

            ###we have to save the reservation now

            #super(General, self).save(*args, **kwargs)
            #this_reservation.save(*args, **kwargs)
        elif classes == 'PaymentReservation':
            # auto = \
            self.updt_payment_state()

            ###we have to save the reservation now

            #super(General, self).save(*args, **kwargs)
            #this_reservation.save(*args, **kwargs)
        elif classes == 'Reservation':

            self.updt_payment_state()
            print('update of totals and payment state')
            print(str(self.total_to_pay)+str(self.total_payments))

        ### Create the action
        if classes != 'Action': #because we create an action and don't want an action to register that we created an action
            s = str(self.last_modification) + ' ' + user + ' modified or created element ' + str(self.id) + ' of class ' + self.get_cname()
            print('Registered Action' +s)
            #Action.objects.create(act=auto + s)
            Action.objects.create(act=s)

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


class Action(General):
    act = models.TextField(default='')

    def get_cname(self):
        class_name = 'Action'
        return class_name

    def __str__(self):
        return str(self.act)

class Task(General):
    STATE = [
        ('D', 'DONE'),
        ('TD', 'TODO'),
        ('SB', 'STANDBY'),
    ]

    description = models.TextField(default='')
    assigned_date = models.DateField(default=timezone.now) #readonly
    delivery_date = models.DateField(blank=True, null=True)
    cause = models.TextField(blank=True, null=True)
    assigner_auto = models.CharField(max_length=100, null=True, blank=True)
    task_state = models.TextField(choices=STATE, default='TD')

    ### KEYS
    assigned_user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True
        )

    def get_cname(self):
        class_name = 'Task'
        return class_name

    def __str__(self):
        return str(self.description)

class ATEC(General):
    def get_cname(self):
        class_name = 'ATEC'
        return class_name

    def __str__(self):
        return str(self.field_name)

    field_name = models.TextField(default='Tours ONG ATEC',null=True,blank=True)
    field_cedjuri = models.TextField(default='Céd.Juri: 3-002-118055',null=True,blank=True)
    field_tel_cellular = models.TextField(default='+(506) 8706-4758.',null=True,blank=True)
    field_localisation = models.TextField(default='Frente a Farmacia Caribe, bajo Mopri, Puerto Viejo Limon',null=True,blank=True)
    field_tel_officina = models.TextField(default='Teléfono: +(506) 2750-0398', null=True, blank=True)
    field_mail = models.TextField(default='Email: ongatec@gmail.com', null=True, blank=True)

    logo = models.ImageField(upload_to='app/static/img',default='ATEC_LOGO.png',null=True,blank=True)
    size_logo = models.TextField(default="120", null=True, blank=True)

    field_thanks = models.TextField(default='Thank you for booking and supporting our NGO ATEC!', null=True, blank=True)
    field_recommandations = models.TextField(default='Recommendations: apply repellent and sun block, closed shoes, bottle of water, camera, snacks, cash and in cases apply swimming suit, towel, jaket',blank=True,null=True)

    ###IMAGES###
    image_1 = models.ImageField(upload_to='app/static/img',default='tripadvisor.jpeg',null=True,blank=True)
    image_2 = models.ImageField(upload_to='app/static/img',default='fb.jpeg',null=True,blank=True)
    image_3 = models.ImageField(upload_to='app/static/img',default='codeofconduct.jpeg',null=True,blank=True)
    image_4 = models.ImageField(upload_to='app/static/img',default='ict.jpeg',null=True,blank=True)
    image_5 = models.ImageField(upload_to='app/static/img',default='turismosostenible.jpeg',null=True,blank=True)

    ###LINKS###
    link_1 = models.TextField(default='https://www.tripadvisor.com.mx/Attraction_Review-g309265-d2209012-Reviews-ATEC_Talamancan_Association_of_Ecotourism_and_Conservation_Day_Tours-Puerto_Viejo.html', null=True, blank=True)
    link_2 = models.TextField(default='https://www.facebook.com/ongatec/', null=True, blank=True)
    link_3 = models.TextField(default='', null=True, blank=True)
    link_4 = models.TextField(default='', null=True, blank=True)
    link_5 = models.TextField(default='', null=True, blank=True)

    ###SIZES###
    size_1 = models.TextField(default="90", null=True, blank=True)
    size_2 = models.TextField(default="90", null=True, blank=True)
    size_3 = models.TextField(default="60", null=True, blank=True)
    size_4 = models.TextField(default="30", null=True, blank=True)
    size_5 = models.TextField(default="44", null=True, blank=True)

class COUPON(General):
    def get_cname(self):
        class_name = 'COUPON'
        return class_name

    def __str__(self):
        return str(self.numero)

    numero = models.IntegerField(default=0)
    image = models.ImageField(upload_to='app/static/img',null=True,blank=True)
    size = models.TextField(default="44", null=True, blank=True)