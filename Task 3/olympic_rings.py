from PIL import Image
import numpy as np
import math
import sys

def count_pixels(image):
  yellow = np.array([255, 255, 0])
  blue = np.array([0, 0, 255])
  black = np.array([0, 0, 0])
  green = np.array([0, 255, 0])
  red = np.array([255, 0, 0])
  
  print("Y {}".format(np.sum(np.all(image == yellow, axis=2))))
  print("B {}".format(np.sum(np.all(image == blue, axis=2))))
  print("K {}".format(np.sum(np.all(image == black, axis=2))))
  print("G {}".format(np.sum(np.all(image == green, axis=2))))
  print("R {}".format(np.sum(np.all(image == red, axis=2))))

def pixel_DFS(graph):
  cc = []
  visited = []
  data = list(graph.keys())
  while len(data):
    tmp = {}
    stack = [data.pop()]
    while len(stack):
      node = stack.pop()
      if node not in visited:
        visited.append(node)
        conn_entry = graph[node]
        if conn_entry[0] not in tmp:
          tmp[conn_entry[0]] = [node]
        else:
          tmp[conn_entry[0]].append(node)
        try:
          data.remove(node)
        except ValueError:
          pass
      for v in graph[node][1]:
        if v not in visited:
          stack.append(v)

    cc.append(tmp)
  return cc

def is_circle(a, b):
  ERR = 2 * math.sqrt(2)
  if abs(a - b) < ERR:
    return True

  return False

def are_intersected(intersections, circle, ring):
  for key in ring.keys():
    if key != circle:
      d = np.linalg.norm(np.asarray(ring[key][0]) - np.asarray(ring[circle][0]))
      r1, r2 = ring[key][1], ring[circle][1]
      if d > (abs(r1 - r2)) and d < (abs(r1+r2)):
        if key not in intersections:
          intersections[key] = {circle}
        else:
          intersections[key].add(circle)
        if circle not in intersections:
          intersections[circle] = {key}
        else:
          intersections[circle].add(key)

def intersection_chk(rings):
  result = []
  for ring in rings:
    is_circle = []
    for key in ring:
      is_circle.append(ring[key][2])
    if all(is_circle):
      intersections = {}
      for key in ring.keys():
        are_intersected(intersections, key, ring)
      is_ring = True

      if (intersections[1] == {2, 3} and intersections[2] == {1}
          and intersections[3] == {1, 4} and intersections[4] == {3, 5}
          and intersections[5] == {4}
          ):
        is_ring = True
      else:
        is_ring = False
      
      if is_ring:
        result.append(ring)
  return result

def circle_chk(cc):
  valid = 0
  rings = []
  for comp in cc:
    ring = {}
    for key in comp.keys():
      min_x = max_x = comp[key][0][0]
      min_y = max_y = comp[key][0][1]
      
      for pixel in comp[key]:
        if pixel[0] > max_x:
          max_x = pixel[0]
        if pixel[0] < min_x:
          min_x = pixel[0]
        if pixel[1] > max_y:
          max_y = pixel[1]
        if pixel[1] < min_y:
          min_y = pixel[1]

      radius = 0
      center = (int((min_x + max_x) / 2), int((min_y + max_y) / 2))
      for pixel in comp[key]:
        radius += np.linalg.norm(np.asarray(center) - np.asarray(pixel))
      
      ring[key] = [center, radius / len(comp[key]), False]

    if len(ring) == 5:
      rings.append(ring)
      for key in comp.keys():
        dists = []
        for pixel in comp[key]:
          dists.append(np.linalg.norm(np.asarray(pixel) - np.asarray(ring[key][0])))

        min_dist = min(dists)
        max_dist = max(dists)

        if is_circle(max_dist, min_dist):
          ring[key][2] = True

  return rings

def find_neighbours(graph, data):
  for pixel in data:
    px = tuple(pixel)
    entry = (px[0], px[1])
    if entry not in graph:
      graph[entry] = [px[2], []]
    adj = [(entry[0], entry[1] - 1), (entry[0], entry[1] + 1),
           (entry[0] - 1, entry[1]), (entry[0] + 1, entry[1]),
           (entry[0] - 1, entry[1] + 1), (entry[0] + 1, entry[1] + 1),
           (entry[0] - 1, entry[1] - 1), (entry[0] + 1, entry[1] - 1)
    ]
    for v in adj:
      if v in graph:
        graph[v][1].append(entry)
        graph[entry][1].append(v)

def print_results(result):
  colormap = {
      1: "Y",
      2: "B",
      3: "K",
      4: "G",
      5: "R"
  }

  print(len(result))
  for ring in result:
    keys = list(ring.keys())
    keys.sort()
    sorted_ring = {i: ring[i] for i in keys}
    for key in sorted_ring.keys():
      print("{} {} {}".format(colormap[key], sorted_ring[key][0][1], sorted_ring[key][0][0]))

def find_pixels(image):
  yellow = np.array([255, 255, 0])
  blue = np.array([0, 0, 255])
  black = np.array([0, 0, 0])
  green = np.array([0, 255, 0])
  red = np.array([255, 0, 0])

  yellow_pixels = np.where(np.all(image == yellow, axis=-1))
  blue_pixels = np.where(np.all(image == blue, axis=-1))
  black_pixels = np.where(np.all(image == black, axis=-1))
  green_pixels = np.where(np.all(image == green, axis=-1))
  red_pixels = np.where(np.all(image == red, axis=-1))

  yellow_coords = np.stack((yellow_pixels[0], yellow_pixels[1]), axis=-1)
  y = np.full((yellow_coords.shape[0], 1),1)
  yellow_coords = np.column_stack((yellow_coords, y))
  
  blue_coords = np.stack((blue_pixels[0], blue_pixels[1]), axis=-1)
  b = np.full((blue_coords.shape[0], 1),2)
  blue_coords = np.column_stack((blue_coords, b))

  black_coords = np.stack((black_pixels[0], black_pixels[1]), axis=-1)
  k = np.full((black_coords.shape[0], 1),3)
  black_coords = np.column_stack((black_coords, k))
  
  green_coords = np.stack((green_pixels[0], green_pixels[1]), axis=-1)
  g = np.full((green_coords.shape[0], 1),4)
  green_coords = np.column_stack((green_coords, g))
  
  red_coords = np.stack((red_pixels[0], red_pixels[1]), axis=-1)
  r = np.full((red_coords.shape[0], 1),5)
  red_coords = np.column_stack((red_coords, r))

  total = np.vstack((yellow_coords, blue_coords))
  total = np.vstack((total, black_coords))
  total = np.vstack((total, green_coords))
  total = np.vstack((total, red_coords))

  graph = {}

  find_neighbours(graph, total)
  components = pixel_DFS(graph)
  rings = circle_chk(components)
  result = intersection_chk(rings)
  print_results(result)

def process_image(imagepath):
  rgba_img = Image.open(imagepath)
  rgba_img.load()
  img = rgba_img.convert('RGB')
  image = np.array(img)
  count_pixels(image)
  find_pixels(image)

if __name__ == "__main__":
    imagepath = sys.stdin.read()
    imagepath = imagepath.strip()
    process_image(imagepath)
