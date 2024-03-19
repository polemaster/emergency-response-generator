import csv
import os
import shutil

from utils.constants import CODES_FILEPATH


class Exporter:
    def __init__(self, generator, directory, include_headers=True):
        self.directory = directory
        # create a directory if it doesn't already exist
        os.makedirs(directory, exist_ok=True)
        self.generator = generator
        self.include_headers = include_headers

    def export_all(self):
        self.export_incidents("incidents.csv")
        self.export_vehicles_sql("vehicles_sql.csv")
        self.export_vehicles_csv("vehicles_csv.csv")
        self.export_vehicle_positions("vehicle_positions.csv")
        self.export_teams("teams.csv")
        self.export_victims_sql("victims_sql.csv")
        self.export_victims_csv("victims_csv.csv")
        self.export_officers_sql("officers_sql.csv")
        self.export_officers_csv("officers_csv.csv")
        self.copy_incident_types("incident_types.csv")
        self.export_victim_groups("victim_groups.csv")
        self.export_incident_team_assignments("incident_team_assignments.csv")
        self.export_team_officer_assignments_sql("team_officer_assignments_sql.csv")

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

        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            if self.include_headers:
                writer.writerow(headers)

            for incident in self.generator.incidents:
                row_data = [
                    incident.incident_id,
                    incident.city,
                    incident.district,
                    incident.position.lat,
                    incident.position.lng,
                    incident.report_datetime,
                    incident.arrival_datetime,
                    incident.victim_satisfaction,
                    incident.type_code,
                ]
                writer.writerow(row_data)

    def write_objects_to_csv(self, objects_list, headers, csv_filename):
        # Open the CSV file in write mode
        with open(csv_filename, "w", newline="") as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write headers if specified
            if self.include_headers:
                writer.writerow(headers)

            # Iterate over each object in the list and write its data to the CSV file
            for obj in objects_list:
                # Extract values for the specified columns
                row_data = [getattr(obj, column) for column in headers]
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

    def export_vehicle_positions(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = [
            "vehicle_position_id",
            "license_plate_number",
            "latitude",
            "longitude",
            "at_time",
        ]

        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            if self.include_headers:
                writer.writerow(headers)

            for vehicle_pos in self.generator.vehicle_positions:
                row_data = [
                    vehicle_pos.vehicle_position_id,
                    vehicle_pos.license_plate_number,
                    vehicle_pos.latitude,
                    vehicle_pos.longitude,
                    vehicle_pos.at_time,
                ]
                writer.writerow(row_data)

        # self.write_objects_to_csv(self.generator.vehicle_positions, headers, filepath)

    def export_teams(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = ["team_id", "start_datetime", "end_datetime", "license_plate_number"]

        self.write_objects_to_csv(self.generator.teams, headers, filepath)
        
    def export_team_officer_assignments_sql(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = ["team_id", "officer_id"]

        self.write_objects_to_csv(self.generator.team_officer_assignments, headers, filepath)
  
    def export_victims_sql(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = ["victim_id", "first_name", "last_name"]

        self.write_objects_to_csv(self.generator.victims, headers, filepath)

    def export_victims_csv(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = ["victim_id", "first_name", "last_name", "gender", "date_of_birth"]

        self.write_objects_to_csv(self.generator.victims, headers, filepath)

    def export_officers_sql(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = ["officer_id", "first_name", "last_name", "team"]

        self.write_objects_to_csv(self.generator.officers, headers, filepath)

    def export_officers_csv(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = [
            "officer_id",
            "first_name",
            "last_name",
            "rank",
            "gender",
            "date_of_birth",
            "hire_date",
            "email",
            "phone_number",
        ]

        self.write_objects_to_csv(self.generator.officers, headers, filepath)

    def copy_incident_types(self, filename):
        filepath = os.path.join(self.directory, filename)
        shutil.copy(CODES_FILEPATH, filepath)

    def export_victim_groups(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = ["victim_id", "incident_id"]

        self.write_objects_to_csv(self.generator.victim_groups, headers, filepath)

    def export_incident_team_assignments(self, filename):
        filepath = os.path.join(self.directory, filename)
        headers = ["incident_id", "team_id"]

        self.write_objects_to_csv(
            self.generator.incident_team_assignments, headers, filepath
        )
