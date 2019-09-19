
### USED TO GET A REQUESTED FOREIGN KEY FIELD

from django.forms.models import BaseInlineFormSet
from .models import LanguagePerson,Person,Mail,Phone

class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        q = self.get_queryset()
        try:
            q.get()
            ### we look if at least one mail/phone does exists for the person that is being modified/created
            ###not sure of the get() but it works
        except:
            form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
            form.empty_permitted = False
        else:
            form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
            form.empty_permitted = True
        return form