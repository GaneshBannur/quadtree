import math
import bisect

class node:
    bucket_size = 5

    def __init__(self):
        self.points = set()
        self.children = {}
        self.node_range = [(-1000, 1000), (-1000, 1000)]
    
    def has(self, point):
        if point[0]>=self.node_range[0][0] and point[0]<=self.node_range[0][1] and point[1]>=self.node_range[1][0] and point[1]<=self.node_range[1][1]:
            return True
        else:
            return False

    def make_children(self):
        for i in range(4):
            self.children[i]=node()
        self.children[0].node_range = [((self.node_range[0][0]+self.node_range[0][1])/2,self.node_range[0][1]), ((self.node_range[1][0]+self.node_range[1][1])/2,self.node_range[1][1])]
        self.children[1].node_range = [(self.node_range[0][0], (self.node_range[0][0]+self.node_range[0][1])/2), ((self.node_range[1][0]+self.node_range[1][1])/2,self.node_range[1][1])]
        self.children[2].node_range = [(self.node_range[0][0], (self.node_range[0][0]+self.node_range[0][1])/2), (self.node_range[1][0], (self.node_range[1][0]+self.node_range[1][1])/2)]
        self.children[3].node_range = [((self.node_range[0][0]+self.node_range[0][1])/2,self.node_range[0][1]), (self.node_range[1][0], (self.node_range[1][0]+self.node_range[1][1])/2)]
        for point in  self.points:
            for child in self.children:
                if self.children[child].has(point):
                    self.children[child].points.add(point)
                    break
    
    def insert(self, point):
        for child in self.children:
            if self.children[child].has(point):
                self.children[child].insert(point)
        if not self.children:
            if len(self.points)==node.bucket_size:
                self.points.add(point)
                self.make_children()
            else:
                self.points.add(point)

    def delete(self, point):
        self.points.discard(point)
        if self.children:
            nodes_num = 0
            current_points = set()
            flag = 0
            for child in self.children:
                if self.children[child].has(point):
                    self.children[child].delete(point)
                if self.children[child].children:
                    flag=1
                else:
                    nodes_num = nodes_num + len(self.children[child].points)
                    current_points.update(self.children[child].points)
            if nodes_num<=node.bucket_size and flag==0:
                self.points.update(current_points)
                self.children.clear()

    def get_points_in_range(self, query_range):
        result = set()
        for child in self.children:
            if query_range[0][0]<=self.children[child].node_range[0][1] and query_range[0][1]>=self.children[child].node_range[0][0] and query_range[1][0]<=self.children[child].node_range[1][1] and query_range[1][1]>=self.children[child].node_range[1][0]:
                result.update(self.children[child].get_points_in_range(query_range))
        else:
            for point in self.points:
                if point[0]>=query_range[0][0] and point[0]<=query_range[0][1] and point[1]>=query_range[1][0] and point[1]<=query_range[1][1]:
                    result.add(point)
        return result

    def find_ancestors(self, point, ancestors):
        ancestors.append(self)
        for child in self.children:
            if self.children[child].has(point):
                ancestors = self.children[child].find_ancestors(point, ancestors)
        return ancestors

    def find_closest(self, n, point, current_best_points, current_distances, point_list):
        count = len(current_best_points)
        for neighbour in point_list:
            if neighbour in current_best_points:
                continue
            distance = math.sqrt((neighbour[0]-point[0])**2+(neighbour[1]-point[1])**2)
            if count==0:
                current_best_points.append(neighbour)
                current_distances.append(distance)
                count = 1
            elif count<n:
                index = bisect.bisect_right(current_distances, distance)
                current_best_points.insert(index, neighbour)
                current_distances.insert(index, distance)
                count = count + 1
            else:
                index = bisect.bisect_right(current_distances, distance)
                if index<n:
                    current_best_points.insert(index, neighbour)
                    current_distances.insert(index, distance)
                    current_best_points = current_best_points[:-1]
                    current_distances = current_distances[:-1]
        return (current_best_points, current_distances, count)

    def n_nearest_approx(self, point, n):
        ancestors = self.find_ancestors(point=point, ancestors=[])
        sorted_result = []
        smallest_distances = []
        temp = ancestors.pop()
        count = 0
        sorted_result, smallest_distances, count = self.find_closest(n=n, point=point, current_best_points=sorted_result, current_distances=smallest_distances, point_list=temp.points)
        while count<n:
            if ancestors:
                current = ancestors.pop()
            else:
                return sorted_result
            for child in current.children:
                if current.children[child] is not temp:
                    sorted_result, smallest_distances, count = self.find_closest(n=n, point=point, current_best_points=sorted_result, current_distances=smallest_distances, point_list=current.children[child].points)
            temp = current
        return sorted_result

    def distance_to_node(self, point):
        dx = max(self.node_range[0][0]-point[0], 0, point[0]-self.node_range[0][1])
        dy = max(self.node_range[1][0]-point[1], 0, point[1]-self.node_range[1][1])
        return math.sqrt(dx**2+dy**2)

    def n_nearest(self, point, n):
        nodes_considered = {self}
        prev_nodes_considered = {}
        prev_best = []
        prev_distances = []
        prev_prev_best = []
        prev_prev_distances = []
        count = 0
        prev_prev_best, prev_prev_distances, count = self.find_closest(n=n, point=point, current_best_points=prev_prev_best, current_distances=prev_prev_distances, point_list=self.points)
        prev_nodes_considered = nodes_considered.copy()
        nodes_considered.clear()
        if not self.children:
            return prev_prev_best
        for child in self.children:
            if self.children[child].distance_to_node(point)<=prev_prev_distances[-1]:
                nodes_considered.add(self.children[child])
        while len(nodes_considered)>0:
            prev_nodes_considered = nodes_considered.copy()
            nodes_considered.clear()
            point_list = set()
            point_list.update(prev_prev_best)
            prev_prev_best = prev_best.copy()
            for current in prev_nodes_considered:
                point_list.update(current.points)
            prev_best, prev_distances, count = self.find_closest(n=n, point=point, current_best_points=prev_best, current_distances=prev_distances, point_list=point_list)
            for prev_node in prev_nodes_considered:
                if prev_node.children:
                    for child in prev_node.children:
                        if prev_node.children[child].distance_to_node(point)<=prev_distances[-1]:
                            nodes_considered.add(prev_node.children[child])
        return prev_best