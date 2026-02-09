def parse_vrp_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    data = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("DIMENSION"):
            data['dimension'] = int(line.split()[-1])
        elif line.startswith("CAPACITY"):
            data['capacity'] = int(line.split()[-1])
        elif line.startswith("VEHICLES"):
            data['vehicles'] = int(line.split()[-1])
        elif line.startswith("EDGE_WEIGHT_SECTION"):
            i += 1
            matrix = []
            for _ in range(data['dimension']):
                row = list(map(int, lines[i].split()))
                matrix.append(row)
                i += 1
            data['distance_matrix'] = matrix
            continue
        elif line.startswith("DEMAND_SECTION"):
            i += 1
            demands = []
            for _ in range(data['dimension']):
                parts = lines[i].split()
                demands.append(int(parts[1]))
                i += 1
            data['demands'] = demands
            continue
        i += 1

    return data
