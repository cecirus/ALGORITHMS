import pandas as pd
from math import fabs


input_file = "parking_spots.csv"
data = pd.read_csv(input_file)


data['Latitude'] = data['Latitude'].astype(str).str.replace(r'[^\d.-]', '', regex=True).astype(float)
data['Longitude'] = data['Longitude'].astype(str).str.replace(r'[^\d.-]', '', regex=True).astype(float)
data['Cost per minute'] = data['Cost per minute'].astype(str).str.replace(r'[^\d.-]', '', regex=True).astype(float)
data['Available time'] = data['Available time'].astype(str).str.replace(r'[^\d.-]', '', regex=True).astype(int)


coordinates = [
   {
       'Name': row['Name'],
       'Latitude': float(row['Latitude']),
       'Longitude': float(row['Longitude']),
       'Cost per minute': float(row['Cost per minute']),
       'Available time': int(row['Available time']) * 60,  
       'Zone': row['Zone']
   }
   for _, row in data.iterrows()
]


def approx_distance(coord1, coord2):
   return fabs(coord1[0] - coord2[0]) + fabs(coord1[1] - coord2[1])


def quicksort(coords, ref_point):
   if len(coords) <= 1:
       return coords
   else:
       pivot = coords[0]
       pivot_distance = approx_distance(ref_point, (pivot['Latitude'], pivot['Longitude']))
       less = [x for x in coords if approx_distance(ref_point, (x['Latitude'], x['Longitude'])) < pivot_distance]
       equal = [x for x in coords if approx_distance(ref_point, (x['Latitude'], x['Longitude'])) == pivot_distance]
       greater = [x for x in coords if approx_distance(ref_point, (x['Latitude'], x['Longitude'])) > pivot_distance]
       return quicksort(less, ref_point) + equal + quicksort(greater, ref_point)


def greedy_best_spot(sorted_spots, user_time, cost_weight, distance_weight):
   best_spot = None
   best_score = float('-inf')  


   for spot in sorted_spots:
       distance = approx_distance((user_latitude, user_longitude), (spot['Latitude'], spot['Longitude']))
       cost_per_minute = spot['Cost per minute']
       available_time = spot['Available time']


       print(f"Checking spot {spot['Name']} with available time {available_time}")


       if user_time > available_time:
           print(f"Skipping spot {spot['Name']} (User time {user_time} > Available time {available_time})")
           continue


       total_cost = user_time * cost_per_minute


       score = -total_cost * cost_weight + -distance * distance_weight


       print(f"Spot: {spot['Name']}, Score: {score}, Cost: ${total_cost:.2f}, Distance: {distance:.2f}")


       if score > best_score:
           best_score = score
           best_spot = spot


   return best_spot


print("\nDataset:")
print(data[['Name', 'Available time', 'Cost per minute', 'Zone']])


try:
   user_latitude = float(input("Enter your latitude: "))
   user_longitude = float(input("Enter your longitude: "))
   user_time = int(input("How long do you plan to park (in minutes)? "))
   cost_weight = float(input("How important is cost? (Enter 1 for equal importance and 2 its a priority) "))
   distance_weight = float(input("How important is distance? (Enter 1 for equal importance and 2 its a priority) "))
except ValueError:
   print("Invalid input! Please enter numeric values.")
   exit()


current_location = (user_latitude, user_longitude)
sorted_coords = quicksort(coordinates, current_location)


best_spot = greedy_best_spot(sorted_coords, user_time, cost_weight, distance_weight)


if best_spot:
   print("\nThe best parking spot for you is:")
   print(f"Name: {best_spot['Name']}")
   print(f"Cost per minute: ${best_spot['Cost per minute']:.2f}")
   print(f"Total cost for {user_time} minutes: ${best_spot['Cost per minute'] * user_time:.2f}")
   print(f"Available time: {best_spot['Available time']} minutes")
   print(f"Zone: {best_spot['Zone']}")
else:
   print("No suitable parking spot found based on your preferences.")
