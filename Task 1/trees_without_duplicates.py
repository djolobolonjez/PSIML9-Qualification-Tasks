import sys

def cd(wd, arg, parents, visited, dir_tree):
  if arg == "..":
      wd = parents[wd]
  else:
    if arg == "/":
      path = arg
    else:
      path = "/" + arg
      if wd != "/":
        path = wd + path
    if path not in visited:
      parents[path] = wd
    wd = path
    if path not in visited and arg != "..":
      visited.append(path)
  
  if parents[wd] not in dir_tree:
    dir_tree[parents[wd]] = [[wd], [], False]
  else:
    if arg != ".." and wd != parents[wd] and wd not in dir_tree[parents[wd]][0]:
      dir_tree[parents[wd]][0].append(wd)
  return wd

def ls(wd, arg, parents, visited, dir_tree):
  files = arg.split(" ")
  try:
    files.remove("")
  except ValueError:
    pass
  if wd not in dir_tree:
    dir_tree[wd] = [[], [], True]

  if len(files) == 1 and files[0] == "":
      return
  for f in files:
    filename = f[3:]
    path = "/"+filename
    if wd != "/":
      path = wd + path
    
    parents[path] = wd
    if path not in visited:
        visited.append(path)
      
    if f[1] == "d" and path not in dir_tree[wd][0]:
      dir_tree[wd][0].append(path)
    elif f[1] == "f" and path not in dir_tree[wd][1]:
        dir_tree[wd][1].append(path)
    dir_tree[wd][2] = True

def sort_tree(tree):
  for key in tree.keys():
    tree[key][0].sort()
    tree[key][1].sort()

def traverse(tree, node, is_dir, depth, dups, order):
  print("|-" * depth, end='')
  if node == "/":
    depth = 0
    print(node)
  else:
    path = node.split("/")
    if is_dir:
      print("{}/".format(path[-1]))
    else:
      parent_path = "/".join(path[:-1])
      if parent_path == "":
        parent_path = "/"
      if path[-1] not in dups:
        dups[path[-1]] = [parent_path]
      else:
        order.append(path[-1])
        dups[path[-1]].append(parent_path)
      print(path[-1])
  if is_dir:
    if node in tree:
      dirs, files, listed = tree[node]
      for i in range(len(dirs)):
        traverse(tree, dirs[i], True, depth + 1, dups, order)
      for i in range(len(files)):
        traverse(tree, files[i], False, depth + 1, dups, order)
      if not listed:
        print("|-" * (depth + 1), end='')
        print("?")
    else:
      print("|-" * (depth + 1), end='')
      print("?")
  return dups, order
      
def print_stats(tree):
    num_dirs = 0
    num_files = 0
    for values in tree.values():
        num_dirs += len(values[0])
        num_files += len(values[1])
    print("{}\n{}".format(num_dirs, num_files))

def path_chk(curr, new, file):
  if curr == new:
    return ""
  curr_list = curr.split("/")
  new_list = new.split("/")
  pth = "/"
  
  if len(curr) > len(new):
    ind = 0
    for i in range(len(new_list)):
      if curr_list[i] == new_list[i]:
        ind = i
      else:
        break
    
    if ind > 0:
      for i in range(1, ind + 1):
        pth += new_list[i]
        pth += "/"
  else:
    ind = 0
    for i in range(len(curr_list)):
      if curr_list[i] == new_list[i]:
        ind = i
      else:
        break
    if ind > 0:
      for i in range(1, ind + 1):
        pth += curr_list[i]
        pth += "/"
  if pth != "/":
    pth = pth[:-1]  
  return pth
    
def len_chk(dest, wd, parents):
  a = dest.count("/")
  b = 0
  while wd != dest:
    b += 1
    wd = parents[wd]
  if a >= b:
    return 0
  return 1

def remove_dups(dups, order, parents):
  cmd = ["$ cd /"]
  wd = "/"
  while len(order):
    next = order.pop(0)
    path = dups[next].pop(1)
    res = path_chk(wd, path, next)
    if res != "":
      if len_chk(res, wd, parents) != 0:
        stack = []
        aux = res
        while aux != "/":
          stack.append("$ cd " + aux.split("/")[-1])
          aux = parents[aux]
        cmd.append("$ cd /")
        while len(stack):
          cmd.append(stack.pop())
      else:
        while wd != res:
          cmd.append("$ cd ..")
          wd = parents[wd]
      wd = res
      stack = []
      aux = path
      while aux != wd:
        stack.append("$ cd " + aux.split("/")[-1])
        aux = parents[aux]
      while len(stack):
        cmd.append(stack.pop())
   
      wd = path
    cmd.append("$ rm " + next)
  return cmd
    
def print_commands(cmd):
  if len(cmd) > 1:
    for c in cmd:
      print(c)
    
def count_data(commands, dir_tree, parents):
  wd = "/"
  visited = []
  for i in range(len(commands)):
    cmd = commands[i][:2]
    index = len(commands[i])
    arg = commands[i][3:index]
    if arg != "":
      if arg[-1] == " ":
        arg = arg[:len(arg)-1]
    if cmd == "cd":
      wd = cd(wd, arg, parents, visited, dir_tree)
    elif cmd == "ls":
      ls(wd, arg, parents, visited, dir_tree)

def parse_input(commands, dir_tree, parents):
  count_data(commands, dir_tree, parents) 
  sort_tree(dir_tree)
  print_stats(dir_tree)
  dups, order = traverse(dir_tree, "/", True, 0, {}, [])
  cmd = remove_dups(dups, order, parents)
  print_commands(cmd)

dir_tree = {"/":[[], [], False]}
parents = {"/":"/"}
if __name__ == "__main__":
    line = sys.stdin.read()
    input_lines = line.split("\n")
    lines = [line for line in input_lines if line != ""]
    line = " ".join(lines)
    line = " " + line
    commands = line.split('$ ')
    try:
        commands.remove(" ")
    except ValueError:
        pass
    parse_input(commands, dir_tree, parents)