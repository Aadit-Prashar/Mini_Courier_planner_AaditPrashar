
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARCEL_FILE = os.path.join(BASE_DIR, "datasets", "parcels.csv")
LOCATION_FILE = os.path.join(BASE_DIR, "datasets", "locations.csv")


def load_parcels():

    parcels = []

    with open(PARCEL_FILE, "r", newline="", encoding="utf-8-sig") as file:

        reader = csv.DictReader(file)

        for row in reader:

            row["weight"] = float(row["weight"])
            row["delivery_cost"] = float(row["delivery_cost"])

            parcels.append(row)

    return parcels


def save_parcels(parcels):

    fields = [
        "parcel_id",
        "destination",
        "weight",
        "priority",
        "delivery_cost",
        "status"
    ]

    with open(PARCEL_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
        writer.writerows(parcels)


def add_parcel(parcel):

    parcels = load_parcels()

    for p in parcels:

        if p["parcel_id"] == parcel["parcel_id"]:
            return False

    parcels.append(parcel)

    save_parcels(parcels)

    return True


def delete_parcel(parcel_id):

    parcels = load_parcels()
    updated = []

    for p in parcels:

        if p["parcel_id"] != parcel_id:
            updated.append(p)

    if len(updated) == len(parcels):
        return False

    save_parcels(updated)

    return True


def update_status(parcel_id, status):

    parcels = load_parcels()

    for p in parcels:

        if p["parcel_id"] == parcel_id:

            p["status"] = status

            save_parcels(parcels)

            return True

    return False


def load_graph():

    graph = {}

    with open(LOCATION_FILE, "r", newline="", encoding="utf-8-sig") as file:

        reader = csv.DictReader(file)

        for row in reader:

            source = row["source"].strip()
            destination = row["destination"].strip()
            distance = float(row["distance"])

            if source not in graph:
                graph[source] = {}

            if destination not in graph:
                graph[destination] = {}

            graph[source][destination] = distance
            graph[destination][source] = distance

    return graph
