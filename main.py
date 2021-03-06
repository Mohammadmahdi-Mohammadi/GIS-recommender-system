 #Import Library
 #The openrouteservice library gives you painless access to the openrouteservice (ORS) routing API's. It performs requests against our API's for
import openrouteservice
from openrouteservice import convert
#Folium is a Python library used for visualizing geospatial data. It is easy to use and yet a powerful library. Folium is a Python wrapper for Leaflet. 
#js which is a leading open-source JavaScript library for plotting interactive maps. ... js and the simplicity of Python, which makes it an excellent tool for plotting maps.
from folium.plugins import MarkerCluster
import folium
import xlrd

#create map with coordiante 36.676056, 48.493992 for Zanjan
map = folium.Map(location=[ 36.676056, 48.493992], zoom_start = 13)


#this class is for locations there are in dataset 
class object():
    def __init__(self,  category, name,x, y, color,  status ):
        self.Category = category # band or gas_station or market
        self.Name = name 
        self.X = x 
        self.Y = y
        self.Color = color #color of icons
        #status is some thing for measerment suitable of that road
        self.Status = status
     
  

  #some function for object
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
    def SetStatus(self, status):
        self.Status = status
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
    def GetStatus(self):
        return self.Status

class recommenderSystem:
    #read exel file and puts them in list
    def ReadFile(self):
        # Give the location of the file
        loc = ("F:\python files\informations.xlsx")
        # To open Workbook
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        return sheet
    
    #create map and after that add some marker to it
    def CreateMap(self, sheet):
        #Create base map
        list = []
        #map = folium.Map(location=[ 36.676056, 48.493992], zoom_start = 13)
        
        for i in range(1, sheet.nrows):
            
            place = object(sheet.cell_value(i, 0), sheet.cell_value(i, 3) , sheet.cell_value(i, 2), sheet.cell_value(i, 1), sheet.cell_value(i, 4),  sheet.cell_value(i, 5))
            
            list.append(place)
            #folium.Marker(location=[float(_y),float(_x)], popup = _name , icon=folium.Icon(color = _color )).add_to(map) 
            folium.Marker(location=[place.GetY(),place.GetX()], popup = place.GetName() , icon=folium.Icon(color = place.GetColor() )).add_to(map) 
        #Save the map
        map.save("map3.html")
        _user = User(sheet)
        #whichCategory = input("enter What place do you want to go?")
       # _user.SelectBest(list,whichCategory )
        if sheet.cell_value(2, 15) != 0:
            destinationX = sheet.cell_value(2, 15)
            destinationY = sheet.cell_value(2, 14)
            _user.goal(destinationX, destinationY)
        
        
        
            
        
        
    def main(self):
        sheet = self.ReadFile()
        self.CreateMap(sheet)
        

class User(): 
    #def __init__(self ):
    def __init__(self , sheet):
        self.BestX=0
        self.BestY=0
        self.BestD=0
        self.BestName = ''
        self.X= sheet.cell_value(2, 13)
        self.Y= sheet.cell_value(2, 12  )
        self.Name = sheet.cell_value(2, 6)
        self.Color = sheet.cell_value(2, 11)
        folium.CircleMarker(location=[self.Y, self.X], radius = 9, popup=self.Name, fill_color='black', color=self.Color, fill_opacity = 0.9).add_to(map)
        #folium.Marker(location=[ self.Y,self.X], popup =  self.Name , icon=folium.Icon(color = self.Color )).add_to(map) 
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

        folium.Marker(location=list(coords[0][::-1]),popup=self.Name,icon=folium.Icon(color="black"),).add_to(map)

        folium.Marker(location=list(coords[1][::-1]),popup="Goal",icon=folium.Icon(color="white"),).add_to(map)
        map.save('map3.html')
    def SelectBest(self ,  list ,  _category ):
       
        for i in list:
            if i.Category ==_category :
                client = openrouteservice.Client(key='5b3ce3597851110001cf62486d7b45f0c7424ffd9be3404ac5894fe1')
                coords = ((self.X,self.Y),(i.X, i.Y))
                res = client.directions(coords)
                tempD = round(res['routes'][0]['summary']['distance']/1000,1) * i.Status            
                if  self.BestD==0:
                    self.BestD =tempD
                else:
                    if self.BestD>=tempD:
                        
                        self.BestD = tempD
                        self.BestX = i.X
                        self.BestY = i.Y
                        self.BestName = i.Name
             
        print(self.BestName)
        self.goal(self.BestX, self.BestY)
        

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


# Function that computes the weighted rating of each movie
def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)
    
    
    
    
    # Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return metadata['title'].iloc[movie_indices]
    
    def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan
    
    def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []
    
    def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''
            
            # Import CountVectorizer and create the count matrix
from sklearn.feature_extraction.text import CountVectorizer

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(metadata['soup'])