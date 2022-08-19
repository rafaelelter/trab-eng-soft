from django.contrib.auth.models import User 

def is_buyer(self):
    if hasattr(self, 'buyer'):
        return True
    return False

def is_offerer(self):
    if hasattr(self, 'offerer'):
        return True
    return False

def is_regulator(self):
    if hasattr(self, 'regulator'):
        return True
    return False
