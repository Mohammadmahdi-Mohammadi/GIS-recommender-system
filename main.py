class object():
    def __init__(self,  category, name,x, y, someInformation, color ):
        self.Category = category
        self.Name = name
        self.X = x 
        self.Y = y
        self.Color = color
        
    def SetCategory(self, category):
        self.Category = Category
    def SetName(self, name):
        self.Name = name
    def SetX(self, x):
        self.X = x
    def SetY(self, y):
        self.Y = y
    def SetColor(self, color):
        self.Color = color
    def GetCategory(self):
        return self.Category
    def GetName(self):
        return self.Name
    def GetX(self):
        return self.X
    def GetY(self):
        return self.Y    
    def GetColor(self):
        return self.Color
  
