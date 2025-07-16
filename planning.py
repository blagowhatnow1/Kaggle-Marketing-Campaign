# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from scipy.optimize import linprog

# Load dataset and apply filters
df = pd.read_csv("synthetic_data.csv")
df = df[(df['HotelRating'] >= 3.5) & (df['TransportType'] != 'Auto')].reset_index(drop=True)

# Setup LP variables
n = len(df)
c = df['TrueTotalCost'].values
bounds = [(0, 1) for _ in range(n)]

# Constraints
A_eq = [np.ones(n)]
b_eq = [5.000001]  # Select exactly 5 bookings (relaxed for tolerance)

A_ub = []
b_ub = []

# Budget constraint: ≤ ₹80,000
A_ub.append(df['TrueTotalCost'].values)
b_ub.append(80000.0)

# Guide rating sum ≥ 20 → -sum ≤ -20
A_ub.append(-df['GuideRating'].values)
b_ub.append(-20.0)

# Carbon score constraint (optional): ≤ 600
if 'CarbonScore' in df.columns:
    A_ub.append(df['CarbonScore'].values)
    b_ub.append(600.0)

# Solve using fallback methods
methods_to_try = ['simplex', 'interior-point']
res = None
for method in methods_to_try:
    try:
        res = linprog(c, A_ub=A_ub, b_ub=b_ub,
                      A_eq=A_eq, b_eq=b_eq,
                      bounds=bounds, method=method)
        if res.success:
            break
    except:
        pass

# Extract and show results
if res is not None and res.success:
    x = res.x
    top_indices = np.argsort(-x)[:5]
    itinerary_df = df.loc[top_indices].copy()
    total_cost = itinerary_df['TrueTotalCost'].sum()
    total_carbon = itinerary_df['CarbonScore'].sum() if 'CarbonScore' in itinerary_df.columns else 'N/A'

    print("\n🧭 Final Optimized Itinerary")
    print("Total Cost: ₹%.2f" % total_cost)
    print("Total Carbon Score: %s" % total_carbon)
    print(itinerary_df[['BookingID', 'City', 'TrueTotalCost', 'GuideRating',
                        'HotelRating', 'TransportType', 'CarbonScore']])
else:
    print("❌ No feasible itinerary found after applying all constraints.")

