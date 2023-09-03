#author Laurynas Maksvytis
"""
There are street lights placed evenly every 20 meters on a straight road.
Most of the street lights are working and have the same illumination intencity.
Non-working street lights are provided as a list of their indexes.
If a street light is not working - its position can still be illuminated by neighboring lights.
Illumination is decreasing exponentially when the distance increases from a street light.
Please find an index of a street light, which has the lowest illumination. Its light bulb will be replaced.
Notes:
- The road lenght can be from 0 to 2000000m.
- The street lights are indexed from 0 and the first one stands at the begining of the road.
- The intensity of illumination can be calculated using f(x) = 3^(-(x/90)^2) formula, 
  where x is a distance from the street ligth in meters.
- If the street light is very far away and its illumination intencity is less than 0.01 - its illumination has to be ignored.
- In case there are several street lights with the same lowest illumination - provide the one with the lowest index.
Example:
road_length = 200
non_working_street_lights = [4, 5, 6]
The length of the road is 200 meters and it has 11 street lights on it. Lights with indexes 4, 5 and 6 are not working.
The bulb of the street light with index 5 has to be replaced, because the illumination at it is the lowest.
Optional (for extra Karma points):
- Please find the minimal number of light bulbs, which is needed to be replaced
  to make cumulative illumination intencity at every street light non less than 1.
"""
import itertools

DISTANCE_BETWEEN_LIGHTS = 20 #distance between lights in meters
LIGHT_THRESHOLD = 0.01 #illumination to be ignored
NEIGHBORS_RANGE = 1 #how many neighbors influences total illumination (1 is just closest two neighbors)


def count_illumination_influence(distance: int) -> float:
    return pow(3, -(pow((distance/90), 2)))
    
def count_street_lights(road_length: int) -> int:
    return int(road_length / DISTANCE_BETWEEN_LIGHTS) + 1

def find_index_of_darkest_street_light(road_length: int, not_working_street_lights: list[int]) -> int:
    lights_count = count_street_lights(road_length)

    targeted_lights = [0] + not_working_street_lights + [lights_count - 1] #counting only not working lights ilumination plus first and last one
    total_lights_illumination = count_lights_ilumination(targeted_lights, not_working_street_lights, lights_count)
      
    min_illum = min(total_lights_illumination)
    index_min = total_lights_illumination.index(min_illum)
    min_light_ilumination_index = targeted_lights[index_min]

    return min_light_ilumination_index
    
def count_lights_ilumination(targeted_lights, not_working_street_lights, lights_count) -> list[float]:
    count_of_not_working_lights = len(targeted_lights)
    total_lights_illumination = []
    
    for i in range(count_of_not_working_lights):
        current_light_index = targeted_lights[i]
        cumulative_illumination = float(0)
        for j in range(-NEIGHBORS_RANGE, NEIGHBORS_RANGE + 1):
            neighbor_light_index = current_light_index + j
            if(neighbor_light_index not in not_working_street_lights):
                if(0 <= neighbor_light_index < lights_count):
                    distance_between_neighbors = abs(j)*DISTANCE_BETWEEN_LIGHTS
                    cumulative_illumination += count_illumination_influence(distance_between_neighbors)
        rounded_illumination = round(cumulative_illumination, 2)
        total_lights_illumination.append(rounded_illumination)
    
    return total_lights_illumination
    
def are_all_lights_intense(lights_illumination) -> bool:
    for x in lights_illumination:
        if(x < 1):
            return False
            
    return True
    
def find_minimal_number_of_lights_to_replace(road_length: int, not_working_street_lights: list[int]) -> int:
    lights_count = count_street_lights(road_length)
    minimal = 0
    targeted_lights = not_working_street_lights #counting only not working lights ilumination
    count_of_targeted_lights = len(targeted_lights)
        
    for x in range(count_of_targeted_lights + 1):
        for subset in itertools.combinations(targeted_lights, x):
            new_target = targeted_lights.copy()
            for x in subset:
                new_target.remove(x)
            total_lights_illumination = count_lights_ilumination(new_target, new_target, lights_count)
            if(are_all_lights_intense(total_lights_illumination)):
                minimal = len(subset)
                return minimal
        
    return minimal

if __name__ == "__main__":
    # This is an example test. When evaluating the task, more will be added:
    assert find_index_of_darkest_street_light(road_length=200, not_working_street_lights=[4, 5, 6]) == 5
    assert find_minimal_number_of_lights_to_replace(road_length=200, not_working_street_lights=[4, 5, 6]) == 1
    print("ALL TESTS PASSED")
    
