import csv
import numpy
import collections

if __name__ =='__main__':
    file="final_project_data/final_project_point_cloud.fuse"
    '''
        Create 4 Arrays, LAT, LONG, ALTITUDE, INTENSITY
    '''
    latitude_array=[]
    longitude_array=[]
    altitude_array=[]
    intensity_array=[]

    '''
        Open the file and attach each column to respective array
    '''
    with open(file) as csv_file:
        lines=csv.reader(csv_file,delimiter=' ')
        for line in lines:
            latitude_array.append(float(line[0]))
            longitude_array.append(float(line[1]))
            altitude_array.append(float(line[2]))
            intensity_array.append(float(line[3]))

    '''
        Get size of any array and use it to create an array shape which can be used when converting 
        lat long to xyz axis
    '''

    no_of_rows=len(latitude_array)
    points_array=numpy.ones((no_of_rows, 4))

    for i in range(0, no_of_rows):
        lat=latitude_array[i]
        long=longitude_array[i]
        pi_value=numpy.pi
        long_cos=numpy.cos(long*pi_value/180)
        long_sin=numpy.sin(long*pi_value/180)
        lat_cos=numpy.cos(lat*pi_value/180)
        lat_sin=numpy.sin(lat*pi_value/180)
        radius_earth=6378137.0

        extra=1.0/numpy.sqrt((lat_cos**2 + ((1-(1.0/298.26))**2)*(lat_sin**2)))
        x=radius_earth*lat_cos*long_cos*extra
        y=radius_earth*lat_cos*long_sin*extra
        z=altitude_array[i]
        intensity=intensity_array[i]

        points_array[i]=x,y,z,intensity

    ''' Add the downsampling code here '''

    ''' Planar plane removal 
        Use the planar removeal on raw point cloud data 
        We filter out points in z axis which do not match the filtering criteria
    '''


    grid_z_list=collections.defaultdict(list)
    x_attach_point=numpy.round(points_array[:,0]*2)
    y_attach_point=numpy.round(points_array[:,1]*2)

    for i in range(len(points_array)):
        grid_z_list[(x_attach_point[i],y_attach_point[i])].append((i, points_array[i, 2]))

    result=[]
    for xy, iz in grid_z_list.items():
        index_list, z_list=zip(*iz)
        if max(z_list) - min(z_list) >= 0.6:
            result.extend(index_list)

    result_planar=points_array[result,:]
    '''
        New values are stored in the ressult
        Planar values are stored in result_planar
    '''

    print(result_planar)








