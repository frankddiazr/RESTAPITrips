import codecs
import pandas as pd
import dateutil.parser
from datetime import datetime
from rest_framework import viewsets,status
from .serializer import AverageSerializer,TripSerializerVieOnly
from .models import Datasources, Regions, Trips
from rest_framework.response import Response


SQL_AVERAGE_BY_REGION=""" SELECT 1 as id,ROUND(trips_per_week.count_trips :: numeric) / 
                        ROUND(apirest_trips.total_trips_per_week :: numeric) average,  
                        apirest_trips.num_week num_week
                    FROM ( SELECT  COUNT(*) count_trips, 
                                    EXTRACT('week' FROM datetime) num_week, 
                                    region_id 
                            FROM apirest_trips t,
                                 apirest_regions r
                            WHERE t.region_id = r.id
                            AND region = %(reg)s
                        GROUP BY region_id, EXTRACT('week' FROM datetime)
                            ) trips_per_week 
                        JOIN (
                        SELECT COUNT(*) total_trips_per_week, 
                            EXTRACT('week' FROM datetime) num_week 
                        FROM apirest_trips 
                        GROUP BY EXTRACT('week' FROM datetime)
                        ) apirest_trips 
                        ON trips_per_week.num_week = apirest_trips.num_week """
                        
SQL_AVERAGE_BY_COORDENATES=""" SELECT 1 as id,ROUND(trips_per_week.count_trips :: numeric) / 
                                    ROUND(apirest_trips.total_trips_per_week :: numeric) average,  
                                    apirest_trips.num_week num_week
                                FROM ( SELECT  COUNT(*) count_trips, 
                                                EXTRACT('week' FROM datetime) num_week
                                        FROM apirest_trips
                                        WHERE ((origin_longitud_round >= %(long)s AND destination_longitud_round <= %(long)s )
                                            AND (origin_latitud_round >= %(lat)s  AND destination_latitud_round <= %(lat)s ))
                                        GROUP BY region_id, EXTRACT('week' FROM datetime)
                                        ) trips_per_week 
                                    JOIN (
                                    SELECT COUNT(*) total_trips_per_week, 
                                        EXTRACT('week' FROM datetime) num_week 
                                    FROM apirest_trips 
                                    GROUP BY EXTRACT('week' FROM datetime)
                                    ) apirest_trips 
                                    ON trips_per_week.num_week = apirest_trips.num_week
                                """



"""
This View contains the methods to query and insert the data accondingly the method called
list: This methos will return all trips stored in the DB
insert: This methos will load,process and insert into the DB the file sent on the request.
queryByRegion: This method will return a json file format with the weekly average number of trips by region, noted that this method 
               will return the average which is a float and the number of week in the year.
               Parameters:
                -region(Char):Name of the region
queryByCoordinates: This method will return a json file format with the weekly average number of trips by region and the coordinates given, noted that this method 
               will return the average which is a float and the number of week in the year.
               Parameters:
                -
                
"""

class TripViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Trips.objects.all()
        serializer = TripSerializerVieOnly(queryset, many=True)
        return Response(serializer.data)
    
    
    def insert(self, request):
        #print("Process started:",str(datetime.now()))
        file=codecs.EncodedFile(request.FILES.get("file").open(),"utf-8")
        reader = pd.read_csv(file, delimiter=";")
        
        reader['origin_coord_longitud']=reader.origin_coord.str.split(pat=' ',expand=True)[1]
        reader['origin_coord_latitud']=reader.origin_coord.str.split(pat=' ',expand=True)[2]
        
        reader['origin_coord_longitud']=reader['origin_coord_longitud'].str[1:]
        reader['origin_coord_latitud']=reader['origin_coord_latitud'].str[:-1]
        
        reader['origin_longitud_round']=pd.to_numeric(reader['origin_coord_longitud'], downcast='float').map('{0:10.2f}'.format)
        reader['origin_latitud_round']=pd.to_numeric(reader['origin_coord_latitud'].str[:-1], downcast='float').map('{0:10.2f}'.format)
        #print("origin Coordenates done:",reader.shape) 
        
        #destination Coordenates
        reader['destination_coord_longitud']=reader.destination_coord.str.split(pat=' ',expand=True)[1]
        reader['destination_coord_latitud']=reader.destination_coord.str.split(pat=' ',expand=True)[2]
        reader['destination_coord_longitud']=reader['destination_coord_longitud'].str[1:]
        reader['destination_coord_latitud']=reader['destination_coord_latitud'].str[:-1]
        
        reader['destination_longitud_round']=pd.to_numeric(reader['destination_coord_longitud'], downcast='float').map('{0:10.2f}'.format)
        reader['destination_latitud_round']=pd.to_numeric(reader['destination_coord_latitud'].str[:-1], downcast='float').map('{0:10.2f}'.format)
        print("destination Coordenates done:",reader.shape) 
        reader['time']= pd.to_datetime(reader['datetime']).dt.time
        reader.sort_values(['region','origin_coord_longitud','origin_coord_longitud','destination_coord_longitud','destination_coord_latitud','time'],inplace=True)
        
        #Dropping columns not needed
        reader.drop(columns=['destination_coord','time','origin_coord'],axis=1,inplace=True)
        #print("Finished transforming file:",str(datetime.now()))   
        
        #print("Shape DataFrame processed:",reader.shape) 
        reader=reader.to_dict(orient = 'records')
        #print("Termino de convertir a diccionario:",str(datetime.now()))   
        

        trips = []
        batch_size=100000
        #print("Start batch:",str(datetime.now()))
        for i, row in enumerate(reader):
            
            datasource,created = Datasources.objects.get_or_create(datasource=row['datasource'])
            region,created=Regions.objects.get_or_create(region=row['region'])

            trip=Trips(datasource=datasource, 
                          region=region,
                          origin_coord_longitud=row['origin_coord_longitud'],
                          origin_coord_latitud=row['origin_coord_latitud'],
                          destination_coord_longitud=row['destination_coord_longitud'],
                          destination_coord_latitud=row['destination_coord_latitud'],
                          datetime= dateutil.parser.parse(row['datetime']),
                          origin_longitud_round=row['origin_longitud_round'],
                          origin_latitud_round=row['origin_latitud_round'],
                          destination_longitud_round=row['destination_longitud_round'],
                          destination_latitud_round=row['destination_latitud_round'])
            trips.append(trip)
            
            if i % batch_size == 0:
                Trips.objects.bulk_create(trips)
                trips = []
                print("Termina batch:",i,":",str(datetime.now()))
        if trips:
            Trips.objects.bulk_create(trips)

        return Response({"status":"Data inserted succesfully"}, status=status.HTTP_200_OK)
       
        
    def queryByRegion(self, request, region):
        
        param= {'reg': region}
        average_week = Trips.objects.raw(SQL_AVERAGE_BY_REGION,param)
        serializer=AverageSerializer(average_week, many=True)

        if average_week:
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"No data found"}, status=status.HTTP_200_OK) 
        
    
    def queryByCoordinates(self, request, longitud,latitud):
        
        longitud=float(longitud)
        longitud='{0:10.2f}'.format(longitud)
        latitud=float(latitud)
        latitud='{0:10.2f}'.format(latitud)
        
        param= {'long': longitud,'lat':latitud}
        average_week = Trips.objects.raw(SQL_AVERAGE_BY_COORDENATES,params=param)
        serializer=AverageSerializer(average_week, many=True)

        if average_week:
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"No data found"}, status=status.HTTP_200_OK) 

   
   