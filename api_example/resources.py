# myapp/api/resources.py
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from api_example.models import Entry
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }
        allowed_methods = ['get', 'post', 'put', 'delete']


class EntryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        #authentication = SessionAuthentication()
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        detail_allowed_methods = ['delete', 'patch', 'post']
