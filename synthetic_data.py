# -*- coding: utf-8 -*-
import random
import pandas as pd

# Define city and transport type pools
cities = ["Delhi", "Mumbai", "Jaipur", "Agra", "Varanasi", "Udaipur",
          "Chennai", "Kolkata", "Hyderabad", "Bengaluru"]
transport_types = ["Bus", "Train", "Flight", "Cab", "Auto"]  # Auto is still included

def generate_booking(i):
    city = random.choice(cities)
    flight = random.randint(4500, 8500)
    transport = random.randint(400, 1800)
    insurance = random.randint(600, 1000)
    guide = random.randint(2200, 3900)

    hotel = random.randint(1800, 5500)
    hotel_tax = round(hotel * random.uniform(0.05, 0.10), 2)
    hotel_service = random.randint(150, 700)

    # Bias toward higher quality
    guide_rating = round(random.uniform(3.5, 5.0), 1)
    hotel_rating = round(random.uniform(3.5, 5.0), 1)

    transport_type = random.choice(transport_types)

    # Lower carbon score for more feasibility
    carbon_score = round((flight + transport) * random.uniform(0.005, 0.03), 2)

    total = flight + transport + insurance + guide
    true_total = total + hotel + hotel_tax + hotel_service

    return {
        "BookingID": i,
        "City": city,
        "FlightCost": flight,
        "TransportCost": transport,
        "InsuranceCost": insurance,
        "GuideCost": guide,
        "TotalCost": total,
        "TransportType": transport_type,
        "GuideRating": guide_rating,
        "CarbonScore": carbon_score,
        "HotelCost": hotel,
        "HotelTax": hotel_tax,
        "HotelServiceFee": hotel_service,
        "HotelRating": hotel_rating,
        "TrueTotalCost": true_total
    }

# Generate 100 rows
synthetic_data = [generate_booking(i + 1) for i in range(100)]

# Convert to DataFrame
df = pd.DataFrame(synthetic_data)

# Save to CSV
df.to_csv("synthetic_data.csv", index=False)

# Show a preview
print(df.head())

