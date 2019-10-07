### As we have been creating separate folders for models, we have to import the here, for more information, read methods at "https://www.webforefront.com/django/modelsoutsidemodels.html"
### All the models will be accessible as if the were in a model.py file

#from .product import ...

from .product_classes import Product,AttributeProduct,Location,ImageProduct,StockProduct,Tax
from .general import General, Action, Task,ATEC,COUPON
from .person_classes import LanguagePerson,TypePerson
from .reservation_classes import TypePayment,Mail,Phone,Person, PaymentReservation, Reservation,LineReservation,PriceProduct, Rate,AgeDiscount,RateDiscount,get_user_type



