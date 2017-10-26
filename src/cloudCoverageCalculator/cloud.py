def trim_cloud_list(clouds):
    i = 0
    j = 0
    while i < len(clouds):
        j = i + 1
        while j < len(clouds):
            if clouds[i].contains_cloud(clouds[j]):
                clouds.remove(clouds[j])
                return trim_cloud_list(clouds)
            elif clouds[j].contains_cloud(clouds[i]):
                clouds.remove(clouds[i])
                return trim_cloud_list(clouds)
            j += 1
        i += 1
    return clouds

def combine_clouds(clouds):
    i = 0
    j = 0
    while i < len(clouds):
        j = i + 1
        while j < len(clouds):
            intersect_area = clouds[i].get_intersection_area(clouds[j])
            if intersect_area > 0:
                avg_area = (clouds[i].get_area() + clouds[j].get_area()) / 2
                area_threshold = avg_area * 2
                if intersect_area > area_threshold:
                    clouds.append(get_cloud_combination(clouds[i], clouds[j]))
                    clouds.remove(clouds[i])
                    clouds.remove(clouds[j])
                    return combine_clouds(clouds)
            j += 1
        i += 1
    return clouds

def get_cloud_combination(cloud1, cloud2):
    x = cloud1.x if cloud1.x < cloud2.x else cloud2.x
    y = cloud1.y if cloud1.y < cloud2.y else cloud2.y
    
    x1 = cloud1.x + cloud1.w
    x2 = cloud2.x + cloud2.w
    y1 = cloud1.y + cloud1.h
    y2 = cloud2.y + cloud2.h
    w = x1 - x if x1 > x2 else x2 - x
    h = y1 - y if y1 > y2 else y2 - y
    
    return Cloud(x, y, w, h)

class Cloud:
    x = 0
    y = 0
    w = 0
    h = 0
    
    def __init__(self):
        pass
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def contains(self, x, y):
        return x >= self.x and y >= self.y and \
                x < self.x + self.w and y < self.y + self.h
    
    def contains_cloud(self, cloud):
        return self.x <= cloud.x and \
                self.y <= cloud.y and \
                self.x + self.w >= cloud.x + cloud.w and \
                self.y + self.h >= cloud.y + cloud.h
    
    def intersects(self, cloud):
        return self.contains(cloud.x, cloud.y) or \
                self.contains(cloud.x + cloud.w, cloud.y) or \
                self.contains(cloud.x, cloud.y + cloud.h) or \
                self.contains(cloud.x + cloud.h, cloud.y + cloud.h) or \
                cloud.contains(self.x, self.y) or \
                cloud.contains(self.x + self.w, self.y) or \
                cloud.contains(self.x, self.y + self.h) or \
                cloud.contains(self.x + self.h, self.y + self.h)
    
    def get_intersection_area(self, cloud):
        if not self.intersects(cloud):
            return 0
        
        xmin = self.x if self.x < cloud.x else cloud.x
        xmax1 = self.x + self.w
        xmax2 = cloud.x + cloud.w
        xmax = xmax1 if xmax1 > xmax2 else xmax2
        
        ymin = self.y if self.y < cloud.y else cloud.y
        ymax1 = self.y + self.h
        ymax2 = cloud.y + cloud.h
        ymax = ymax1 if ymax1 > ymax2 else ymax2
        
        w = xmax - xmin
        h = ymax - ymin
        
        return w * h
    
    def get_point(self):
        return (self.x, self.y)
    
    def get_opposite_point(self):
        return (self.x + self.w, self.y + self.h)
    
    def get_area(self):
        return self.w * self.h