import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata

# Load scan data from SD card
file_path = "E:\scan_data.csv" # Ensure correct path
data = pd.read_csv(file_path)

# Stepper motor full rotation = 360°
total_steps = len(data)  # Total recorded steps
angle_per_step = 360 / total_steps  # Step resolution

# Sensor positions (relative to stepper rotation)
sensor_offsets = np.array([-2.5, -1.5, -0.5, 0.5, 1.5, 2.5])  # Adjusted positions in cm

# Empty lists for 3D points
x_points, y_points, z_points = [], [], []

for index, row in data.iterrows():
    step_angle = index * angle_per_step  # Convert step count to angle

    for i, distance in enumerate(row[1:]):  # Skip first column (step count)
        if distance > 0 and distance < 2000:  # Ignore invalid readings
            angle_rad = np.radians(step_angle)
            x = (distance / 10) * np.cos(angle_rad)  # Convert mm to cm
            y = (distance / 10) * np.sin(angle_rad)
            z = sensor_offsets[i]

            x_points.append(x)
            y_points.append(y)
            z_points.append(z)

# Convert lists to numpy arrays
x_points, y_points, z_points = np.array(x_points), np.array(y_points), np.array(z_points)

# Densify using interpolation
grid_x, grid_y = np.meshgrid(
    np.linspace(min(x_points), max(x_points), 100),
    np.linspace(min(y_points), max(y_points), 100)
)

grid_z = griddata((x_points, y_points), z_points, (grid_x, grid_y), method='cubic')

# Create an interactive 3D plot
fig = go.Figure(data=[
    go.Scatter3d(x=x_points, y=y_points, z=z_points, mode='markers',
                 marker=dict(size=2, color=z_points, colorscale='Viridis', opacity=0.8))
])

fig.update_layout(title="3D Scan Visualization", scene=dict(
    xaxis_title="X (cm)", yaxis_title="Y (cm)", zaxis_title="Z (cm)"
))

fig.show()
