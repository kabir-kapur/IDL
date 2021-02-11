import dash
import dash_cytoscape as cyto
import dash_html_components as html
import networkvis

"""
possible approaches:
- change the way its formatted/ size of nodes
- 

"""
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
    elsList = []
    dem = 0
    rep = 0
    ind = 0
    tnk = 0

    for i in networkvis.currd:
        if networkvis.currd[i] == 'd':
            dem += 1
        elif networkvis.currd[i] == 'r':
            rep += 1
        elif networkvis.currd[i] == 'i':
            ind += 1

    for i in networkvis.currd:
        if networkvis.currd[i] == 't':
            elsList.append({'data' : {'id' : str(i), 'label' : str(i), 'color' : 'green'}})
        elsList.append({'data' : {'id' : 'democrats', 'label' : str(dem) + ' democrats'}})
        elsList.append({'data' : {'id' : 'republicans', 'label' : str(rep) + ' republicans', 'weight' : rep}})
        elsList.append({'data' : {'id' : 'independents', 'label' : str(ind) + ' independents', 'weight' : ind}})

    # for i, j in list(networkvis.makeAdjMatrix(inlist).items()):
    #     for k, l in list(j.items()):
    #         if l != 0 and currd[i] == 'd':
    #             elsList.append({'data' : {'source' : str(dem) + ' democrats', 'target' : str(k)}})

    return elsList



def makeElementsListColored(inlist = networkvis.makeNetworkList()):
    elsList = []
    coloredDict = {'d' : [], 'r' : [], 'i': [], 't' : []}
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
                elsList.append({'data' : {'id' : str(j), 'label' : str(j), 'classes' : 'blue'}})
        elif i == 'r':
            for j in coloredDict[i]:
                elsList.append({'data' : {'id' : str(j), 'label' : str(j), 'classes' : 'red'}})
        elif i == 'i':
            for j in coloredDict[i]:
                elsList.append({'data' : {'id' : str(j), 'label' : str(j), 'classes' : 'purple'}})
        elif i == 't':
            for j in coloredDict[i]:
                elsList.append({'data' : {'id' : str(j), 'label' : str(j), 'classes' : 'green'}})
    
    for i, j in list(networkvis.makeAdjMatrix(inlist).items()):
        for k, l in list(j.items()):
            if l != 0:
                elsList.append({'data' : {'source' : str(i), 'target' : str(k)}})
    return elsList
            
    return coloredDict
    

app = dash.Dash(__name__)
# instantiate Dash object
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape_tweet_network',
        layout={'name': 'random'},
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