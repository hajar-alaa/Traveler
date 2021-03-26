from django.contrib import admin

# Register your models here.
from travler.models import *



admin.site.register(Location)
admin.site.register(Post)
admin.site.register(Activity)
# admin.site.register(PostActivity)
admin.site.register(UserProfile)
admin.site.register(WorkPlace)
admin.site.register(Message)
admin.site.register(Visit)