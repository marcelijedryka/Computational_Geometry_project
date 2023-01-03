def det_3by3(a, b, c):
    '''calculate where point c is located in accordance to vector a-b
    if det > 0, point is on the left
    if < 0 then point on the right
    if 0 then colineal'''


    return a[0]*b[1]+a[1]*c[0]+b[0]*c[1]-c[0]*b[1]-a[1]*b[0]-a[0]*c[1]

def orient(a, b, c):
    e = 10**(-12)
    '''Orient returns 1 if point c is on the left of the lina a->b, 
    -1 if c is on the right 
    and 0 if the're collineal '''
    d = det_3by3(a, b, c)
    if d > e:
        return 1
    elif d < (-1)*e:
        return -1
    else:
        return 0


class Polygon_line:
    def __init__(self, p1, p2) -> None:
        self.start = p1
        self.end = p2
        self.next = None

    def set_next(self, polygon_line):
        self.next = polygon_line

class Polygon:
    def __init__(self, lines) -> None:
        self.lines = lines
        self.polygon = []
        self.open = False

        for line in self.lines:
            self.polygon.append(line[0])

        if self.lines[len(self.lines) - 1][1] not in self.polygon:
            self.polygon.append(self.lines[len(self.lines) - 1][1])
            self.open = True

        self.left = None
        self.right = None

        self.make_left_right_chains(self.polygon)

    def contains_line(self, line):
        tmp = self.left
        while tmp != None:
            if line == tmp:
                return True
            tmp = tmp.next

        tmp = self.right
        while tmp != None:
            if line == tmp:
                return True
            tmp = tmp.next

        return False

    def is_in_left_chain(self, line):
        tmp = self.left
        while tmp != None:
            if tmp == line:
                return True
            tmp = tmp.next

        return False


    def make_left_right_chains(self, polygon):
        n = len(polygon)
        max_y = -float('inf')
        min_y = float('inf')
        for i, point in enumerate(polygon):
            if point[1] > max_y:
                max_y = point[1]
                max_i = i
            if point[1] < min_y:
                min_y = point[1]
                min_i = i

        left = []
        right = []

        left_i = max_i
        right_i = max_i


        while left_i != min_i:
            if left_i > n:
                left_i = 0
            left.append(polygon[left_i])
            left_i += 1
        if len(left) == 1 and polygon.open:
            left = []
        else:
            left.append(polygon[min_i])

        while right_i != min_i:
            if right_i < 0:
                right_i = n
            right.append(polygon[right_i])
            right_i -= 1
        if len(right) == 1 and polygon.open:
            right = []
        else:
            right.append(polygon[min_i])


        # tu moe się wywalić bo nie zaliczamy najwyzszego i najnizszego punktu do chainow
        # probably juz naprawione ;-;
        if right:
            right_line = Polygon_line(right[0], right[1])
        else:
            right_line = None
        right_ptr = right_line
        if len(right) > 2:
            for i in range(1, len(right) - 1):
                curr_line = Polygon_line(right[i], right[i + 1])
                right_line.set_next(curr_line)
                right_line = right_line.next

        if left:
            left_line = Polygon_line(left[0], left[1])
        else:
            left_line = None
        left_ptr = left_line
        if len(left) > 2:
            for i in range(1, len(left) - 1):
                curr_line = Polygon_line(left[i], left[i + 1])
                left_line.set_next(curr_line)
                left_line = left_line.next


        self.left = left_ptr
        self.right = right_ptr
        

class Intersect:
    '''input polygons as list of edges'''
    def __init__(self, polygon1, polygon2):
        self.polygon1 = Polygon(polygon1)
        self.polygon2 = Polygon(polygon2)

        self.right_edge_c1 = None
        self.right_edge_c2 = None
        self.left_edge_c1 = None
        self.left_edge_c2 = None

        # self.right_edge_c1 = polygon1.right
        # self.right_edge_c2 = polygon2.right
        # self.left_edge_c1 = polygon1.left
        # self.left_edge_c2 = polygon2.left

    def find_max_y(self, polygon):
        max_y = -float('inf')

        for point in polygon:
            if point[1] > max_y:
                max_y = point[1]

        return point[1]

    def find_intersection(self):

        # if len(self.polygon1.lines) == 1 and len(self.polygon2) == 1:
        #     # both polygons are only 1 line
        #     pass

        y_1 = self.find_max_y(self.polygon1.polygon)
        y_2 = self.find_max_y(self.polygon2.polygon)
        y_start = min(y_1, y_2)

        self.init_broom(y_start)

        event = self.find_first_event(y_start)

        while not self.all_pointers_null():
            if self.polygon1.contains_line(event):
                if self.polygon1.is_in_left_chain(event):
                    self.handle_left_event(self.polygon1, self.polygon2, event)
                else:
                    self.handle_right_event(self.polygon1, self.polygon2, event)

            else:
                if self.polygon2.is_in_left_chain(event):
                    self.handle_left_event(self.polygon2, self.polygon1, event)
                else:
                    self.handle_right_event(self.polygon2, self.polygon1, event)



    def handle_left_event(self, polygon1, polygon2, line):
        pass

    def handle_right_event(self, polygon1, polygon2, line):
        pass

    def lines_intersect(self, line_1: Polygon_line, line_2: Polygon_line):
        a, b = line_1.start, line_1.end
        c, d = line_2.start, line_2.end

        orient_1 = orient(a, b, c)
        orient_2 = orient(a, b, d)

        orient_3 = orient(c, d, a)
        orient_4 = orient(c, d, b)

        if orient_1 != orient_2 and orient_3 != orient_4:
            True

        return False


    def init_broom(self, y_start):
        if self.polygon1.left:
            if self.polygon1.left.start >= y_start >= self.polygon1.left.end:
                self.left_edge_c1 = self.polygon1.left
        if self.polygon1.right:
            if self.polygon1.right.start >= y_start >= self.polygon1.right.end:
                self.right_edge_c1 = self.polygon1.right

        if self.polygon2.left:
            if self.polygon2.left.start >= y_start >= self.polygon2.left.end:
                self.left_edge_c2 = self.polygon2.left
        
        if self.polygon2.right:
            if self.polygon2.right.start >= y_start >= self.polygon2.right.end:
                self.right_edge_c2 = self.polygon2.right

    def all_pointers_null(self):
        if self.left_edge_c1:
            return False
        if self.left_edge_c2:
            return False
        if self.right_edge_c1:
            return False
        if self.right_edge_c2:
            return False
        return True

    def find_first_event(self, start_y):
        if start_y == self.polygon1.left.start:
            return self.polygon1.left
        
        if start_y == self.polygon2.left.start:
            return self.polygon2.left

        if start_y == self.polygon1.right.start:
            return self.polygon1.right

        if start_y == self.polygon2.right.start:
            return self.polygon2.right
        



    
