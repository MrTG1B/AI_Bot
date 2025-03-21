import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.interpolate import griddata

# Load CSV Data
csv_file = "scan_data.csv"
data = pd.read_csv(csv_file)

# Sensor positions (Vertical offsets)
sensor_offsets = np.linspace(-2.5, 2.5, 6)

# Store 3D points
x_vals, y_vals, z_vals = [], [], []

for _, row in data.iterrows():
    angle = np.radians(row["Angle"])
    for i in range(6):
        distance = row[f"S{i+1}"]
        if 0 < distance < 2000:
            x = distance * np.cos(angle)
            y = distance * np.sin(angle)
            z = sensor_offsets[i]
            x_vals.append(x)
            y_vals.append(y)
            z_vals.append(z)

# Create a grid for smoother visualization
grid_x, grid_y = np.mgrid[min(x_vals):max(x_vals):100j, min(y_vals):max(y_vals):100j]
grid_z = griddata((x_vals, y_vals), z_vals, (grid_x, grid_y), method='cubic')

# **Plotly Interactive 3D Surface Plot**
fig = go.Figure(data=[
    go.Surface(x=grid_x, y=grid_y, z=grid_z, colorscale="jet")
])
fig.update_layout(title="High-Resolution 3D Scan", scene=dict(
    xaxis_title="X Distance (mm)",
    yaxis_title="Y Distance (mm)",
    zaxis_title="Z Height (mm)"
))
fig.show()
