import Map
import Node
import PRM

# size: list, a list which show max range of map, [min_x, max_x, min_y, max_y]
# n: number of obstacle
size = [0, 20, 0, 20]
n = 1
# generate map
map = Map.Map(size, n)
initial = Node.Node(1, 1)
goal = Node.Node(19, 19)

prm = PRM.PRM(map, 5, 3, initial, goal)
prm.Roadmap_construction()
prm.solve_query()

prm.Plot()
