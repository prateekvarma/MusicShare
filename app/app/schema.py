import graphene
import tracks.schema
import users.schema
import graphql_jwt

#main Query class, that will take query classes from all other django apps
class Query(users.schema.Query, tracks.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, tracks.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

#schema is defined here in main schema, instead of every app's schema
schema = graphene.Schema(query=Query, mutation=Mutation)