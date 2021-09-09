 #Import Library
import openrouteservice
from openrouteservice import convert
import json
import folium
import xlrd
map = folium.Map(location=[ 36.676056, 48.493992], zoom_start = 13)

class object():
    def __init__(self,  category, name,x, y, color ):
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
    
    
        
#me = object('bank', 'maskan', 37.296933, -121.9574983 , ' hello')
#print(me.Name)


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
        #map = folium.Map(location=[ 36.676056, 48.493992], zoom_start = 13)
        #print(    sheet.cell_value(10, 0))
        for i in range(1, sheet.nrows):
            
            place = object(sheet.cell_value(i, 0), sheet.cell_value(i, 3) , sheet.cell_value(i, 2), sheet.cell_value(i, 1), sheet.cell_value(i, 4))
            
            list.append(place)
            #folium.Marker(location=[float(_y),float(_x)], popup = _name , icon=folium.Icon(color = _color )).add_to(map) 
            folium.Marker(location=[place.GetY(),place.GetX()], popup = place.GetName() , icon=folium.Icon(color = place.GetColor() )).add_to(map) 
        #Save the map
        map.save("map3.html")
        _user = User(sheet)
        destinationX = sheet.cell_value(2, 15)
        destinationY = sheet.cell_value(2, 14)
        _user.goal(destinationX, destinationY)
        
    def main(self):
        sheet = self.ReadFile()
        x = self.CreateMap(sheet)
        

class User(): 
    def __init__(self , sheet):
       # print(sheet.cell_value(2, 13))
        self.X= sheet.cell_value(2, 13)
        self.Y= sheet.cell_value(2, 12  )
        self.Name = sheet.cell_value(2, 6)
        self.Color = sheet.cell_value(2, 11)
        folium.Marker(location=[ self.Y,self.X], popup =  self.Name , icon=folium.Icon(color = self.Color )).add_to(map) 
        map.save("map3.html")
        
    def goal(self, destinationX, destinationY):
        client = openrouteservice.Client(key='5b3ce3597851110001cf62486d7b45f0c7424ffd9be3404ac5894fe1')
        coords = ((self.X,self.Y),(destinationX,destinationY))
        res = client.directions(coords)
        geometry = client.directions(coords)['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)

        distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
        duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"

        #map = folium.Map(location=[ 36.676056, 48.493992],zoom_start=13, control_scale=True,tiles="cartodbpositron")
        folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(map)

        folium.Marker(location=list(coords[0][::-1]),popup="Galle fort",icon=folium.Icon(color="green"),).add_to(map)

        folium.Marker(location=list(coords[1][::-1]),popup="Jungle beach",icon=folium.Icon(color="red"),).add_to(map)
        map.save('map3.html')


x = recommenderSystem()
x.main()
        
