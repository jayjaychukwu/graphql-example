import graphene
from graphene_django import (
    DjangoObjectType,  # this import is used to change Django objects to F
)

from main_app.models import Contact


class ContactType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = Contact
        field = ("id", "name", "phone_number")


class Query(graphene.ObjectType):
    # query ContactType class to get the list of contacts
    list_contact = graphene.List(ContactType)

    def resolve_list_contact(root, info):
        # can easily optimize query count in the resolve method
        return Contact.objects.all()


schema = graphene.Schema(query=Query)
