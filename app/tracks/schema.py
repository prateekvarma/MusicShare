import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Track, Like
# since the Like model uses get_user_model, we will import UserType
from users.schema import UserType

class TrackType(DjangoObjectType):
    #for TrackType to inherit the structure of Track, we define a meta class
    class Meta:
        model = Track

#create a LikeType for getting data from the Like model
class LikeType(DjangoObjectType):
    class Meta:
        model = Like

class Query(graphene.ObjectType):
    #get all tracks query
    tracks = graphene.List(TrackType)
    #get all likes
    likes = graphene.List(LikeType)

    def resolve_tracks(self, info):
        return Track.objects.all()

    def resolve_likes(self, info):
        return Like.objects.all()

class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url):
        #get currently signed in user
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to add a track')

        track = Track(title=title, description=description, url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)

class UpdateTrack(graphene.Mutation):
    #expected retur from this class
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, track_id, title, description, url):
        #get the user associated
        user = info.context.user
        #get the track id
        track = Track.objects.get(id=track_id)

        #check if the posted_by field in track is differen than that's passed from context
        if track.posted_by != user:
            raise GraphQLError('This is not your track, you cannot update it')

        #set the fields in user object that we got from the DB, to ones from the argument
        track.title = title
        track.description = description
        track.url = url
        track.save()

        #return the class, with the field as defined in 1st line of class
        return UpdateTrack(track=track)

class DeleteTrack(graphene.Mutation):
    # In this case, we want only the track's ID to be returned, not the entire track
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        # get the related user, to check if it's his track
        user = info.context.user
        # get the track according to the track_id from arguments
        track = Track.objects.get(id=track_id)
        #check if the track belongs to the user
        if track.posted_by != user:
            raise GraphQLError('This track is not yours, you cannot delete it')

        track.delete()
        return DeleteTrack(track_id=track_id)

class CreateLike(graphene.Mutation):
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        #get the current
        user = info.context.user
        #check if the user is logged in
        if user.is_anonymous:
            raise GraphQLError('Login to like')

        #get the track with it's id    
        track = Track.objects.get(id=track_id)
        #additional check, if track exists (not necessary)
        if not track:
            raise GraphQLError('Cannot find track with that id')

        #create the like
        Like.objects.create(
            user = user,
            track = track
        )
        
        return CreateLike(user=user, track=track)


#The below Mutation class should be now inherited from the base Mutation class
class Mutation(graphene.ObjectType):
    #register your mutations here
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()