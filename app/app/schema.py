import graphene
import tracks.schema
import users.schema

#main Query class, that will take query classes from all other django apps
class Query(tracks.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation ,tracks.schema.Mutation, graphene.ObjectType):
    pass

#schema is defined here in main schema, instead of every app's schema
schema = graphene.Schema(query=Query, mutation=Mutation)