from django.contrib import admin
from electorates.models import House, Electorate, Party, Member, AddressType, Address, Email

admin.site.register(House)
admin.site.register(Electorate)
admin.site.register(Party)
admin.site.register(Member)
admin.site.register(AddressType)
admin.site.register(Address)
admin.site.register(Email)