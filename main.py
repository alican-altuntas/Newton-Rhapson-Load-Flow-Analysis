import numpy as np
from scipy.sparse import lil_matrix


def create_bus_admittance_matrix(bus_data, line_data):
    # Get the number of buses
    num_buses = len(bus_data)
    # Initialize the bus admittance matrix in lil_matrix format
    y_bus = lil_matrix((num_buses, num_buses), dtype=complex)
    # Loop through the line data to populate the Ybus matrix
    for line in line_data:
        from_bus = line['from_bus'] - 1  # Convert to zero-based index
        to_bus = line['to_bus'] - 1  # Convert to zero-based index
        impedance = line['impedance']
        admittance = 1 / impedance  # Y = 1 / Z

        # Add to diagonal for both from_bus and to_bus (self-admittance)
        y_bus[from_bus, from_bus] += admittance
        y_bus[to_bus, to_bus] += admittance

        # Subtract off-diagonal elements (mutual admittance between buses)
        y_bus[from_bus, to_bus] -= admittance
        y_bus[to_bus, from_bus] -= admittance

    return y_bus


# Example usage:
bus_data = {
    1: {'voltage': 1.0, 'angle': 0.0},  # Example bus data
    2: {'voltage': 1.0, 'angle': 0.0},
    3: {'voltage': 1.0, 'angle': 0.0}
}

line_data = [
    {'from_bus': 1, 'to_bus': 2, 'impedance': 0.01 + 0.03j},  # Example line data
    {'from_bus': 2, 'to_bus': 3, 'impedance': 0.02 + 0.04j},
    {'from_bus': 3, 'to_bus': 1, 'impedance': 0.015 + 0.045j}
]

# Create Ybus matrix
y_bus = create_bus_admittance_matrix(bus_data, line_data)

# Convert Ybus to dense matrix for display (optional)
print(y_bus.todense())
