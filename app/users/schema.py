from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

#Custom type class, used to define users. Inherits from Django's built in User Model
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

#create mutation to create user
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        #Use the default Django's user model
        user = get_user_model()(
            username = username,
            email = email
        )
        #password needs to be set with set_password function
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()