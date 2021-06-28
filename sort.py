from numpy import rad2deg, deg2rad
from math import acos, sin, cos

import pandas


visitors = pandas.read_csv('visitor-locations-times.csv')
restaurants = pandas.read_csv('sf-restaurants.csv')


def sort_by_each_visitor():
    """
    best restaurants for given visitor according to his current location and current time.
    """
    for i, visitor in visitors.iterrows():
        print(f'\tvisitor: {i+1}')

        restaurants_for_visitor = restaurants.copy()
        distances = []

        for _, restaurant in restaurants.iterrows():
            # distance between two coordinates
            distance = rad2deg(acos(
                sin(deg2rad(visitor.lat)) * sin(deg2rad(restaurant.lat)) + cos(deg2rad(visitor.lat)) * cos(
                    deg2rad(restaurant.lat)) * cos(deg2rad(visitor.lng - restaurant.lng)))) * 60 * 1.1515

            distances.append(distance)

        restaurants_for_visitor['distance'] = distances

        restaurants_for_visitor = restaurants_for_visitor.loc[(restaurants_for_visitor['distance'] <= 1) & (
                get_timeslot(int(visitor.current_time)) == restaurants_for_visitor['timeslot'])]

        restaurants_for_visitor = restaurants_for_visitor.sort_values(['rating', 'distance'], ascending=(False, True))

        restaurants_for_visitor = restaurants_for_visitor.iloc[:3]

        print(restaurants_for_visitor)


def get_timeslot(time):
    """
    breakfast (8 am - 11 am), lunch (12 pm - 3 pm), or dinner (6:30 pm to 9:30 pm)
    """
    if 800 <= time <= 1100:
        return 'breakfast'
    if 1200 <= time <= 1500:
        return 'lunch'
    if 1830 <= time <= 2130:
        return 'dinner'


if __name__ == "__main__":
    sort_by_each_visitor()
