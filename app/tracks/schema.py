import graphene
from graphene_django import DjangoObjectType

from .models import Track

class TrackType(DjangoObjectType):
    #for TrackType to inherit the structure of Track, we define a meta class
    class Meta:
        model = Track

class Query(graphene.ObjectType):
    #get all tracks query
    tracks = graphene.List(TrackType)

    def resolve_tracks(self, info):
        return Track.objects.all()

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
            raise Exception('Login to add a track')

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
            raise Exception('This is not your track, you cannot update it')

        #set the fields in user object that we got from the DB, to ones from the argument
        track.title = title
        track.description = description
        track.url = url
        track.save()

        #return the class, with the field as defined in 1st line of class
        return UpdateTrack(track=track)


#The below Mutation class should be now inherited from the base Mutation class
class Mutation(graphene.ObjectType):
    #register your mutations here
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()