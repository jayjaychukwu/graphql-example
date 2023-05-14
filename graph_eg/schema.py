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
        id = graphene.ID()  # this is for updating purpose
        name = graphene.String()
        phone_number = graphene.String()

    contact = graphene.Field(ContactType)  # define the class we are the fields from

    ######INITIAL CODE########
    # @classmethod
    # def mutate(cls, root, info, name, phone_number, id):
    #     # function that will save the data to the db
    #     #######CREATE###########
    #     contact = Contact(
    #         name=name,
    #         phone_number=phone_number,
    #     )  # accepts all fields
    #     contact.save()  # save the contact to the database

    #     ##########UPDATE########################
    #     get_contact = Contact.objects.get(id=id)
    #     get_contact.name = name  # assign a new name
    #     get_contact.phone_number = phone_number  # assign a new phone_number
    #     get_contact.save()
    #     return ContactMutation(contact=get_contact)

    #######UPDATED CODE##############
    def mutate(self, info, name, phone_number, id=None):
        # this is for update case
        if id:
            contact = Contact.objects.get(id=id)
            if name:
                contact.name = name
            if phone_number:
                contact.phone_number = phone_number
            contact.save()

        # this is for create case
        else:
            contact = Contact(name=name, phone_number=phone_number)
            contact.save()

        return ContactMutation(contact=contact)


class Query(graphene.ObjectType):
    # query ContactType class to get the list of contacts
    list_contact = graphene.List(ContactType)  # list all the Contact objects
    read_contact = graphene.Field(
        ContactType,
        id=graphene.Int(),
    )  # id = graphene.Int, retrieve a particular contact object

    def resolve_list_contact(root, info):
        # can easily optimize query count in the resolve method
        return Contact.objects.all()

    def resolve_read_contact(root, info, id):
        # get data where id in the database is equal to the id queried from the frontend
        return Contact.objects.get(id=id)


class Mutation(graphene.ObjectType):
    # keywords that will be used to do the mutation in the frontend
    create_contact = ContactMutation.Field()
    update_contact = ContactMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
