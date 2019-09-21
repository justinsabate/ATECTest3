### As we have been creating separate folders for models, we have to import the here, for more information, read methods at "https://www.webforefront.com/django/modelsoutsidemodels.html"
### All the models will be accessible as if the were in a model.py file

#from .product import ...

from .product_classes import Product,AttributeProduct,Location,PriceProduct,ImageProduct,StockProduct,Rate
from .general import General, Action, Task
from .person_classes import LanguagePerson,Person,Mail,Phone,TypePerson
from .reservation_classes import TypePayment, PaymentReservation, Reservation,LineReservation
