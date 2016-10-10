from django.db.models import BooleanField as _BooleanField


class BooleanField(_BooleanField):
    def __init__(self, *args, **kwargs):
        super(BooleanField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value in ("0", "false", "False"):
            return False
        elif value in ("1", "true", "True"):
            return True
        else:
            return super(BooleanField, self).get_prep_value(value)