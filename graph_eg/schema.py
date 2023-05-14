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


class ContactMutation(graphene.Mutation):
    class Arguments:
        # add fields you would like to create.
        # this will corelate with the ContactType fields above
        name = graphene.String()
        phone_number = graphene.String()

    contact = graphene.Field(ContactType)  # define the class we are the fields from

    @classmethod
    def mutate(cls, root, info, name, phone_number):
        # function that will save the data to the db
        contact = Contact(
            name=name,
            phone_number=phone_number,
        )  # accepts all fields
        contact.save()  # save the contact to the database


class Query(graphene.ObjectType):
    # query ContactType class to get the list of contacts
    list_contact = graphene.List(ContactType)
    read_contact = graphene.Field(ContactType, id=graphene.Int())  # id = graphene.Int

    def resolve_list_contact(root, info):
        # can easily optimize query count in the resolve method
        return Contact.objects.all()

    def resolve_read_contact(root, info, id):
        # get data where id in the database is equal to the id queried from the frontend
        return Contact.objects.get(id=id)


class Mutation(graphene.ObjectType):
    # keywords that will be used to do the mutation in the frontend
    create_contact = ContactMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
