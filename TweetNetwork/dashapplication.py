import dash
import dash_cytoscape as cyto
import dash_html_components as html
import networkvis

"""
possible approaches:
- change the way its formatted/ size of nodes
- 

"""
# def ttList(inList = networkvis.currd):
#     outList = []
#     for i innetworkvis.currd:
#         ifnetworkvis.currd[j] == 't':
#             outList.append

def makeElementsList(inlist = networkvis.makeNetworkList()):
    elsList = []
    for i in inlist:
        elsList.append({'data' : {'id' : str(i), 'label' : str(i)}}) 
    for i, j in list(networkvis.makeAdjMatrix(inlist).items()):
        for k, l in list(j.items()):
            if l != 0:
                elsList.append({'data' : {'source' : str(i), 'target' : str(k)}})
    # print(elslist)
    return elsList

def makeElementsListColoredAndCompressed(inlist = networkvis.makeNetworkList()):
    elsList = [] # outlist for reading by cyto
    ttList = [] # list of notable thinktanks, to be assembled in this function
    dem = 0 # number of democrats
    rep = 0 # ^
    ind = 0 # ^
    tnk = 0 # ^


    for i in networkvis.currd:
        if networkvis.currd[i] == 'democrats':
            dem += 1
        elif networkvis.currd[i] == 'republicans':
            rep += 1
        elif networkvis.currd[i] == 'independents':
            ind += 1

    for i in networkvis.currd:
        if networkvis.currd[i] == 'thinktanks':
            elsList.append({'data' : {'id' : str(i), 'label' : str(i), 'color' : 'green'}})
            elsList.append({'data' : {'id' : 'democrats', 'label' : str(dem) + ' democrats'}})
            elsList.append({'data' : {'id' : 'republicans', 'label' : str(rep) + ' republicans', 'weight' : rep}})
            elsList.append({'data' : {'id' : 'independents', 'label' : str(ind) + ' independents', 'weight' : ind}})

    elsList.append({'data' : {'source' : 'democrats', 'target' : 'democrats'}, 'weight' : 0})
    elsList.append({'data' : {'source' : 'democrats', 'target' : 'republicans'}, 'weight' : 0})
    elsList.append({'data' : {'source' : 'democrats', 'target' : 'independents'}, 'weight' : 0})

    elsList.append({'data' : {'source' : 'republicans', 'target' : 'democrats'}, 'weight' : 0})
    elsList.append({'data' : {'source' : 'republicans', 'target' : 'republicans'}, 'weight' : 0})
    elsList.append({'data' : {'source' : 'republicans', 'target' : 'independents'}, 'weight' : 0})

    elsList.append({'data' : {'source' : 'independents', 'target' : 'democrats'}, 'weight' : 0})
    elsList.append({'data' : {'source' : 'independents', 'target' : 'republicans'}, 'weight' : 0})
    elsList.append({'data' : {'source' : 'independents', 'target' : 'independents'}, 'weight' : 0})

    for i in networkvis.currd:
        if networkvis.currd[i] == 'thinktanks':
            ttList.append(i)

    yuh = 0
    for i, j in list(networkvis.makeAdjMatrix(inlist).items()):
        if i == "@SenA":
            yuh += 1
            print(yuh)
        for k, l in list(j.items()):
            try:
                if networkvis.currd[k] in ttList:
                    elsList.append({'data' : {'source' : networkvis.currd[i], 'target' : k}})
                    ttList.remove(k)
            except KeyError:
                print("Index error at " + k + " while creating DASH ELEMENTS LIST.")


    return elsList



def makeElementsListColored(inlist = networkvis.makeNetworkList()):
    elsList = []
    coloredDict = {'d' : [], 'r' : [], 'i': [], 't' : []}
    counter = 0

    for i in networkvis.currd:
        if networkvis.currd[i] == 'd':
            coloredDict['d'].append(i)
        elif networkvis.currd[i] == 'r':
            coloredDict['r'].append(i)
        elif networkvis.currd[i] == 'i':
            coloredDict['i'].append(i)
        elif networkvis.currd[i] == 't':
            coloredDict['t'].append(i)

    for i in coloredDict:
        if i == 'd':
            for j in coloredDict[i]:
                elsList.append({'data' : {'id' : str(j), 'label' : str(j), 'classes' : 'blue', 'level' : 2}})
        elif i == 'r':
            for j in coloredDict[i]:
                elsList.append({'data' : {'id' : str(j), 'label' : str(j), 'classes' : 'red', 'level' : 2}})
        elif i == 'i':
            for j in coloredDict[i]:
                elsList.append({'data' : {'id' : str(j), 'label' : str(j), 'classes' : 'purple', 'level' : 2}})
        elif i == 't':
            for j in coloredDict[i]:
                elsList.append({'data' : {'id' : str(j), 'label' : str(j), 'classes' : 'green', 'level' : 1}})
            
    return elsList

app = dash.Dash(__name__)
# instantiate Dash object
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape_tweet_network',
        layout={
            'name': 'circle'
        },
        style={'width': '100%', 'height': '800px'},
        elements= makeElementsListColoredAndCompressed(),
        stylesheet = [
            {
                'selector' : 'node',
                'style' : {
                    'background-color': 'green',
                    'label' : 'data(label)' 
                }
            },
            {
                'selector' : '[label = "228 republicans"]', # this number is proprietary to my dataset
                'style' : {
                    'background-color': 'red',
                    'label' : 'data(label)'
                }
            },
            {
                'selector' : '[label = "256 democrats"]', # this number is proprietary to my dataset
                'style' : {
                    'background-color': 'blue',
                    'label' : 'data(label)', 
                }
            },
            {
                'selector' : '[label = "4 independents"]', # this number is proprietary to my dataset
                'style' : {
                    'background-color': 'purple',
                    'label' : 'data(label)' 
                }
            }
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)