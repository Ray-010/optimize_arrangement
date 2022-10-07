def visualize_map(route_only, sy, sx, gy, gx, height, width):
    map = [["#"]*width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if route_only[y][x] != -1:
                map[y][x] = "."

    map[sy][sx] = "S"
    map[gy][gx] = "G"
    
    return map
