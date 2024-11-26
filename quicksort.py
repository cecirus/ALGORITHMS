import pandas as pd
from math import fabs
input_file = "parking spots 2.csv"  
data = pd.read_csv(input_file)


coordinates = [(float(row['Latitude']), float(row['Longitude'])) for _, row in data.iterrows()]


def approx_distance(coord1, coord2):
   return fabs(coord1[0] - coord2[0]) + fabs(coord1[1] - coord2[1])
def quicksort(coords, ref_point):
   if len(coords) <= 1:
       return coords
   else:
       pivot = coords[0]
       pivot_distance = approx_distance(ref_point, pivot)
       less = [x for x in coords if approx_distance(ref_point, x) < pivot_distance]
       equal = [x for x in coords if approx_distance(ref_point, x) == pivot_distance]
       greater = [x for x in coords if approx_distance(ref_point, x) > pivot_distance]
       return quicksort(less, ref_point) + equal + quicksort(greater, ref_point)


try:
   user_longitude = float(input("Enter your longitude: "))
   user_latitude = float(input("Enter your latitude: "))
   current_location = (user_longitude, user_latitude)
except ValueError:
   print("Invalid input! Please enter numeric values for latitude and longitude.")
   exit()


sorted_coords = quicksort(coordinates, current_location)


print("Sorted coordinates by distance to your location:")
print(sorted_coords)


