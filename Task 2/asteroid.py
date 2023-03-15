import sys

def calculate_area(data, neighbours):
  for voxel in data:
    neighbours[voxel] = []
    for key in neighbours.keys():
      if key[2] == voxel[2]:
        if (key[1] == voxel[1] and (key[0] == voxel[0] - 1 or key[0] == voxel[0] + 1)) or (key[0] == voxel[0] and (key[1] == voxel[1] - 1 or key[1] == voxel[1] + 1)):  
          neighbours[voxel].append(key)
          neighbours[key].append(voxel)
      else:
        if (key[2] == voxel[2] - 1 or key[2] == voxel[2] + 1) and (key[0] == voxel[0] and key[1] == voxel[1]):
          neighbours[voxel].append(key)
          neighbours[key].append(voxel)
          
  invisible = 0
  for value in neighbours.values():
    invisible += len(value)
  return len(data) * 6 - invisible

def dfs_helper(graph, components, point, axis):

  visited = []
  conn = []
  nodes = list(graph.keys())
  ind = 0
  for i in range(len(nodes)):
    if nodes[i][0] == point and axis == "x":
      ind = i
      break
    elif nodes[i][1] == point and axis == "y":
      ind = i
      break
    elif nodes[i][2] == point and axis == "z":
      ind = i
      break 
  aux = [nodes.pop(ind)]
  while len(aux):
    curr = aux.pop()
    if curr not in visited and curr not in conn:
      visited.append(curr)
      conn.append(curr)
      if axis == "x":
        for v in graph[curr]:
          if v[0] == curr[0]:
            aux.append(v)
      if axis == "y":
        for v in graph[curr]:
          if v[1] == curr[1]:
            aux.append(v)
      if axis == "z":
        for v in graph[curr]:
          if v[2] == curr[2]:
            aux.append(v)
  components.append(conn)
  return

def dfs(graph, points):
  components = []
  index = 0
  while len(components) != 6:
    if index in (0, 1):
      dfs_helper(graph, components, points[index], "x")
    elif index in (2, 3):
      dfs_helper(graph, components, points[index], "y")
    elif index in (4, 5):
      dfs_helper(graph, components, points[index], "z")
    index += 1
  return components

def conn_comp(data, graph):
  xmax = xmin = data[0][0]
  ymax = ymin = data[0][1]
  zmax = zmin = data[0][2]
  for i in range(1, len(data)):
    if data[i][0] > xmax:
      xmax = data[i][0]
    if data[i][0] < xmin:
      xmin = data[i][0]
    if data[i][1] > ymax:
      ymax = data[i][1]
    if data[i][1] < ymin:
      ymin = data[i][1]
    if data[i][2] > zmax:
      zmax = data[i][2]
    if data[i][2] < zmin:
      zmin = data[i][2]
  
  conn = dfs(graph, [xmax, xmin, ymax, ymin, zmax, zmin])
  max_surface = len(conn[0])
  for i in range(1, len(conn)):
    size = len(conn[i])
    if size > max_surface:
      max_surface = size

  return max_surface

def print_output(total_area, max_area):
    print("{} {}".format(total_area, max_area))

def parse_input(data, neighbours):
  total_area = calculate_area(data, neighbours)
  max_area = conn_comp(data, neighbours)
  print_output(total_area, max_area)

if __name__ == "__main__":
    lines = []
    for line in sys.stdin:
        lines.append(line)
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    try:
        lines.remove("")
    except ValueError:
        pass
    
    line = "".join(lines)
    lines = line.split("(")
    try:
        lines.remove("")
    except ValueError:
        pass
    input_line = "".join(lines)
    lines = input_line.split(")")
    try:
        lines.remove("")
    except ValueError:
        pass
    
    data = []
    for line in lines:
        data.append(line.split(", "))
    for i in range(len(data)):
        for j in range(len(data[i])):
          data[i][j] = int(data[i][j])
    for i in range(len(data)):
        data[i] = tuple(data[i])
    parse_input(data, {})
