
from data_manager import load_parcels
from sorting import sort_by_priority

# Load parcels test
parcels = load_parcels()

print("----- ORIGINAL PARCELS -----")

for p in parcels:
    print(p)

# Sort parcels test
sorted_parcels = sort_by_priority(parcels)

print("\n----- SORTED PARCELS -----")

for p in sorted_parcels:
    print(p["parcel_id"], "-", p["priority"])
