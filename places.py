import csv
import random
import time


class Rectangle:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.area = abs(
            (self.bottom_right[0] - self.top_left[0])
            * (self.bottom_right[1] - self.top_left[1])
        )

    def __str__(self):
        return f"Rectangle({self.area}, {self.top_left}, {self.bottom_right})"

    def __repr__(self):
        return f"Rectangle({self.area}, {self.top_left}, {self.bottom_right})"


class District:
    def __init__(self, name):
        self.name = name
        self.rectangles = []
        self.total_area = 0

    def add_rectangle(self, rectangle):
        self.rectangles.append(rectangle)
        self.total_area += rectangle.area

    def __str__(self):
        return f"District({self.name}, {self.total_area}, {self.rectangles})"

    def __repr__(self):
        return f"District({self.name}, {self.total_area}, {self.rectangles})\n"


class City:
    def __init__(self, name):
        self.name = name
        self.districts = []
        self.total_area = 0

    def add_district(self, district):
        self.districts.append(district)
        self.total_area += district.total_area

    def update_area(self):
        self.total_area = 0
        for district in self.districts:
            self.total_area += district.total_area

    def __str__(self):
        return f"City({self.name}, {self.total_area},\n {self.districts})"

    def __repr__(self):
        return f"City({self.name}, {self.total_area},\n {self.districts})"


def generate_random_point(rectangle):
    x = random.uniform(rectangle.top_left[0], rectangle.bottom_right[0])
    y = random.uniform(rectangle.top_left[1], rectangle.bottom_right[1])
    return x, y


def create_cities_with_districts(my_list):
    cities = []

    # create all cities
    unique_city_names = list(set(city[0] for city in my_list))
    for city_name in unique_city_names:
        cities.append(City(city_name))

    # create all districts
    for city_name, district_name, top_left, bottom_right in my_list:
        # if the district is not already added to a city, add it
        city = list(filter(lambda x: x.name == city_name, cities))[0]
        if district_name not in map(lambda x: x.name, city.districts):
            city.add_district(District(district_name))

        # add a rectangle to the the district
        district = list(filter(lambda x: x.name == district_name, city.districts))[0]
        district.add_rectangle(Rectangle(top_left, bottom_right))

    # update areas of the cities
    for city in cities:
        city.update_area()

    return cities


def assign_weights(cities):
    city_weights = [city.total_area for city in cities]  # to-do: standardize?
    district_weights = {}
    for city in cities:
        for district in city.districts:
            district_weights[(city.name, district.name)] = (
                district.total_area / city.total_area
            )

    return city_weights, district_weights


def load_data_from_csv(file_path):
    data = []
    with open(file_path, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city = row["city"]
            district = row["district"]
            top_left_latitude = float(row["top_left_latitude"])
            top_left_longitude = float(row["top_left_longitude"])
            bottom_right_latitude = float(row["bottom_right_latitude"])
            bottom_right_longitude = float(row["bottom_right_longitude"])
            data.append(
                (
                    city,
                    district,
                    (top_left_latitude, top_left_longitude),
                    (bottom_right_latitude, bottom_right_longitude),
                )
            )
    return data


class RandomPlaceGenerator:
    def __init__(self, districts_path="data/districts.csv") -> None:
        self.my_list = load_data_from_csv(districts_path)

        self.cities = create_cities_with_districts(self.my_list)

        # Assign weights to cities and districts based on area
        self.city_weights, self.district_weights = assign_weights(self.cities)

    def select_random_place(self):
        selected_city = random.choices(self.cities, weights=self.city_weights)[0]
        selected_district = random.choices(
            selected_city.districts,
            weights=[
                self.district_weights[(selected_city.name, district.name)]
                for district in selected_city.districts
            ],
        )[0]
        selected_rectangle = random.choice(selected_district.rectangles)
        selected_point = generate_random_point(selected_rectangle)

        return (selected_city.name, selected_district.name, selected_point)


def main():
    g = RandomPlaceGenerator()

    # print("city weights:", city_weights)
    # print("district_weights:", district_weights)

    final_list = []

    start = time.time()
    # Random selection
    n = 100_000
    for _ in range(n):
        selected_place = g.select_random_place()
        final_list.append(selected_place)
    end = time.time()
    print(f"Time of {n} selections: ", end - start)

    selected_place = g.select_random_place()
    print("Selected City:", selected_place[0])
    print("Selected District:", selected_place[1])
    print("Selected Point within Rectangle:", selected_place[2])


if __name__ == "__main__":
    main()
