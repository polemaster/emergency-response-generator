import csv
import os


class Exporter:
    def __init__(self, generator, directory, include_headers=True):
        self.directory = directory
        self.generator = generator
        self.include_headers = include_headers  # TODO: add this functionality

    def export_all(self):
        self.export_incidents("incidents.csv")
        self.export_vehicles_sql("vehicles_sql.csv")
        self.export_vehicles_csv("vehicles_csv.csv")
        # self.export_vehicle_positions()
        # self.export_teams()
        # self.export_victims_sql()
        # self.export_victims_csv()
        # self.export_officers_sql()
        # self.export_officers_csv()
        # self.export_incident_types()
        # self.export_victim_groups()
        # self.export_incident_team_assignments()

    def export_incidents(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = [
            "incident_id",
            "city",
            "district",
            "latitude",
            "longitude",
            "report_datetime",
            "arrival_datetime",
            "victim_satisfaction",
            "type_code",
        ]

        attribute_functions = {
            "latitude": lambda inc: inc.position.lat,
            "longitude": lambda inc: inc.position.lng,
        }

        self.write_objects_to_csv(
            self.generator.incidents, headers, filepath, attribute_functions
        )
        # with open(filepath, "w", newline="") as csvfile:
        #     writer = csv.writer(csvfile)

        #     if self.include_headers:
        #         writer.writerow(headers)

        #     for incident in self.generator.vehicles:
        #         row_data = [
        #             incident.incident_id,
        #         ]
        #         writer.writerow(row_data)

    def write_objects_to_csv(
        self, objects_list, headers, csv_filename, attribute_functions=[]
    ):
        # Open the CSV file in write mode
        with open(csv_filename, "w", newline="") as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write headers if specified
            if headers and self.include_headers:
                writer.writerow(headers)

            # Iterate over each object in the list and write its data to the CSV file
            row_data = []
            for obj in objects_list:
                for attribute in headers:
                    if attribute in attribute_functions:
                        value = attribute_functions[attribute](obj)
                    else:
                        value = getattr(obj, attribute)
                    row_data.append(value)
                # Extract values for the specified columns
                # row_data = [getattr(obj, column) for column in headers]
                writer.writerow(row_data)

    def export_vehicles_sql(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = ["license_plate_number", "type", "last_inspection"]

        # Open the CSV file in write mode
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            if self.include_headers:
                writer.writerow(headers)

            for vehicle in self.generator.vehicles:
                row_data = [
                    vehicle.license_plate_number,
                    vehicle.__class__.__name__,
                    vehicle.last_inspection,
                ]
                writer.writerow(row_data)

    def export_vehicles_csv(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = [
            "license_plate_number",
            "type",
            "brand",
            "model",
            "manufacturing_year",
        ]

        # Open the CSV file in write mode
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            if self.include_headers:
                writer.writerow(headers)

            for vehicle in self.generator.vehicles:
                row_data = [
                    vehicle.license_plate_number,
                    vehicle.__class__.__name__,
                    vehicle.brand,
                    vehicle.model,
                    vehicle.manufacturing_year,
                ]
                writer.writerow(row_data)
