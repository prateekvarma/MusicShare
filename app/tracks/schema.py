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