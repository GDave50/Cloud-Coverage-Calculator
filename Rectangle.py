# Combines rectangles in a list of rectangles (rects) if
# two rectangles intersect by an area greater than
# or equal to 0 < areaThreshold <= 1
def CombineRects(rects, areaThreshold):
	i = 0
	j = 0
	
	while i < len(rects):
		j = i + 1
		
		while j < len(rects):
			intersectRect = rects[i].GetIntersection(rects[j])
			
			if intersectRect != None:
				area1 = rects[i].GetArea()
				area2 = rects[j].GetArea()
				area = area1 if area1 < area2 else area2
				threshold = area * areaThreshold
				
				intersect_area = intersectRect.GetArea()
				
				if intersect_area > threshold:
					rect1 = rects.pop(j)
					rect2 = rects.pop(i)
					rects.append(rect1.GetIntersection(rect2))
					return CombineRects(rects, areaThreshold)
			
			j += 1
		
		i += 1
	return rects

class Rectangle:
	x = 0
	y = 0
	w = 0
	h = 0
	
	# Initialize the rectangle with x=0, y=0, w=0, h=0
	def __init__(self):
		pass
	
	# Initialize the rectangle with x, y, w, h
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
	
	# Determines if this rectangle contains the given point (x, y)
	def Contains(self, x, y):
		return x >= self.x and y >= self.y and \
			   x < self.x + self.w and y < self.y + self.h
	
	# Determines if rect is entirely contained within this rectangle
	def ContainsRect(self, rect):
		return rect.x >= self.x and \
			   rect.y >= self.y and \
			   rect.x + rect.w < self.x + self.w and \
			   rect.y + rect.h < self.y + self.h
	
	# Determines if rect intersects this rectangle
	def Intersects(self, rect):
		return self.Contains(rect.x, rect.y) or \
			   self.Contains(rect.x + rect.w, rect.y) or \
			   self.Contains(rect.x, rect.y + rect.h) or \
			   self.Contains(rect.x + rect.w, rect.y + rect.h) or \
			   rect.Contains(self.x, self.y) or \
			   rect.Contains(self.x + self.w, self.y) or \
			   rect.Contains(self.x, self.y + self.h) or \
			   rect.Contains(self.x + self.w, self.y + self.h)
	
	# Finds a rectangle that is the intersection rectangle
	# of rect and this rectangle
	def GetIntersection(self, rect):
		if not self.Intersects(rect):
			return None
		
		x1 = self.x if self.x < rect.x else rect.x
		y1 = self.y if self.y < rect.y else rect.y
		
		x_1 = self.x + self.w
		x_2 = rect.x + rect.w
		x2 = x_1 if x_1 > x_2 else x_2
		
		y_1 = self.y + self.h
		y_2 = rect.y + rect.h
		y2 = y_1 if y_1 > y_2 else y_2
		
		w = x2 - x1
		h = y2 - y1
		
		return Rectangle(x1, y1, w, h)
	
	# Returns the tuple (x, y) where x and y are the coordinates
	# of the upper-left corner of this rectangle
	def GetPoint(self):
		return (self.x, self.y)
	
	# Returns the tuple (x, y) where x and y are the coordinates
	# of the lower-right corner of this rectangle
	def GetOppositePoint(self):
		return (self.x + self.w, self.y + self.h)
	
	# Returns the area of this rectangle
	def GetArea(self):
		return self.w * self.h
	
	def __str__(self):
		return "[%d, %d, %d, %d]" % (self.x, self.y, self.w, self.h)