import folium
import xlrd


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
  

class recommenderSystem:
    
    def ReadFile(self):
        # Give the location of the file
        loc = ("F:\python files\informations.xlsx")
        # To open Workbook
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        return sheet
    
    def CreateMap(self, sheet):
        #Create base map
        list = []
        map = folium.Map(location=[ 36.676056, 48.493992], zoom_start = 13)
        #print(    sheet.cell_value(10, 0))
        for i in range(1, sheet.nrows):
            
            place = object(sheet.cell_value(i, 0), sheet.cell_value(i, 3) , sheet.cell_value(i, 2), sheet.cell_value(i, 1), sheet.cell_value(i, 4))
            
            list.append(place)
            #folium.Marker(location=[float(_y),float(_x)], popup = _name , icon=folium.Icon(color = _color )).add_to(map) 
            folium.Marker(location=[place.GetY(),place.GetX()], popup = place.GetName() , icon=folium.Icon(color = place.GetColor() )).add_to(map) 
        
        #Save the map
        map.save("map3.html")
        
    def main(self):
        sheet = self.ReadFile()
        x = self.CreateMap(sheet)
        
        
x = recommenderSystem()
x.main()
        
        
data = Dataset.load_builtin("ml-100k")
sim_options = {
    "name": ["msd", "cosine"],
    "min_support": [3, 4, 5],
    "user_based": [False, True],
}

param_grid = {"sim_options": sim_options}

gs = GridSearchCV(KNNWithMeans, param_grid, measures=["rmse", "mae"], cv=3)
gs.fit(data)

print(gs.best_score["rmse"])
print(gs.best_params["rmse"])
