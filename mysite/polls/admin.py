from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Poll)
admin.site.register(User)
admin.site.register(Invitation)
admin.site.register(PollOptionAssociation)
admin.site.register(Choice)
admin.site.register(Option)