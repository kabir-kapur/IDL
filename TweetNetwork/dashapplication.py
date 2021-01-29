import dash
import dash_cytoscape as cyto
import dash_html_components as html
import networkvis

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

app = dash.Dash(__name__)
# instantiate Dash object
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape_tweet_network',
        layout={'name': 'circle'},
        # style={'width': '100%', 'height': '1000px'},
        # elements=networkvis.makeNetworkList()[:10]
        elements= makeElementsList()
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, port = 8010)


# import dash
# import dash_cytoscape as cyto
# import dash_html_components as html
# import *networkvis

# App = dash.Dash(__name__)

# App.layout = html.Div([
#   cyto.Cytoscape(
#       id = 'cytoscape-two-nodes', 
#       layout = {'name' : 'preset'},
#       style = {'width' : '100%', 'height' : '400px'}
#   )]
'''        elements=[
            {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
            {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'one', 'target': 'two'}}
        ]'''



# ssh -N -f -L localhost:8050:localhost:8050 krkapur@socs-stats.ucsc.edu