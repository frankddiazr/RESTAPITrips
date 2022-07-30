from rest_framework import serializers


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    
    def to_internal_value(self, data):
        return self.get_queryset().get_or_create(**{self.slug_field: data})[0]


class AverageSerializer(serializers.Serializer):
    average = serializers.FloatField()
    num_week= serializers.IntegerField()


class TripSerializerVieOnly(serializers.Serializer):
    
    region                     = CreatableSlugRelatedField(slug_field='region',read_only=True)
    datasource                 = CreatableSlugRelatedField(slug_field='datasource',read_only=True)
    origin_coord_longitud      = serializers.CharField(read_only=True)
    origin_coord_latitud       = serializers.CharField(read_only=True)
    destination_coord_longitud = serializers.CharField(read_only=True)
    destination_coord_latitud  = serializers.CharField(read_only=True)
    datetime                   = serializers.DateTimeField(read_only=True)
    origin_longitud_round      = serializers.FloatField(read_only=True) 
    origin_latitud_round       = serializers.FloatField(read_only=True)
    destination_longitud_round = serializers.FloatField(read_only=True)
    destination_latitud_round  = serializers.FloatField(read_only=True)
    