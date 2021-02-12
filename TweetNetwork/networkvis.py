import os, csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

'''
filepath = '/Users/kabirkapur/Desktop/TweetTracker/Untruncated With RTs'  <--- wd for my machine
filepath = '/afs/cats.ucsc.edu/users/y/krkapur/IDL/TweetNetwork/CongressionalTweetsData' <--- wd for socs stats server
'''

""" use nested lists (n lists with n elements to represent rows and columns) as a way of representing the adjacency matrix used to put out network.
n should be probably around 500-ish and 'hits' only account for in-network accounts"""

currd = {'@RepFinkenauer': 'democrats', '@RepLindaSanchez': 'democrats', '@RepKatieHill': 'democrats', '@RepTimBurchett': 'republicans', '@SenBooker': 'democrats', '@RepSylviaGarcia': 'democrats', '@RepDelBene': 'democrats', '@amprog': 'thinktanks', '@RepMcNerney': 'democrats', '@RepJuanVargas': 'democrats', '@RepJeffries': 'democrats', '@TXRandy14': 'republicans', '@RepCartwright': 'democrats', '@RepRooney': 'republicans', '@RepSpanberger': 'democrats', '@RobWittman': 'republicans', '@CongressmanHice': 'republicans', '@RepJackBergman': 'republicans', '@MarioDB': 'republicans', '@SenatorEnzi': 'republicans', '@RepDebHaaland': 'democrats', '@RepAdrianSmith': 'republicans', '@RepMullin': 'republicans', '@brookingsinst': 'thinktanks', '@RepUnderwood': 'democrats', '@RepRashida': 'democrats', '@RepBeatty': 'democrats', '@BettyMcCollum04': 'democrats', '@RepAdamSmith': 'democrats', '@maziehirono': 'democrats', '@SenatorHassan': 'democrats', '@HurdOnTheHill': 'republicans', '@SenJohnKennedy': 'republicans', '@RepDeanPhillips': 'democrats', '@AEIfdp': 'thinktanks', '@RepBrianFitz': 'republicans', '@DonaldNorcross': 'democrats', '@RepJahanaHayes': 'democrats', '@DrNealDunnFL2': 'republicans', '@CAPTalksRace': 'thinktanks', '@SenatorShaheen': 'democrats', '@SenJackReed': 'democrats', '@Heritage': 'thinktanks', '@BrookingsEcon': 'thinktanks', '@RepDonBeyer': 'democrats', '@virginiafoxx': 'republicans', '@CatoInstitute': 'thinktanks', '@repdavidscott': 'democrats', '@SenJoniErnst': 'republicans', '@RepRoKhanna': 'democrats', '@CongressmanGT': 'republicans', '@RepDLamborn': 'republicans', '@chelliepingree': 'democrats', '@RepTomEmmer': 'republicans', '@BobbyScott': 'democrats', '@RepPaulMitchell': 'independents', '@MikeCrapo': 'republicans', '@SenatorCantwell': 'democrats', '@RepBenCline': 'republicans', '@RepDean': 'democrats', '@WarrenDavidson': 'republicans', '@michaelcburgess': 'republicans', '@SenatorTester': 'democrats', '@SenRickScott': 'republicans', '@RepWebster': 'republicans', '@RepTedBudd': 'republicans', '@SenateMajLdr': 'republicans', '@RepMGS': 'democrats', '@RepAlexMooney': 'republicans', '@RepTrey': 'republicans', '@RepRonWright': 'republicans', '@RepAlGreen': 'democrats', '@RepSherrill': 'democrats', '@RepGarretGraves': 'republicans', '@RepPeteAguilar': 'democrats', '@RepEscobar': 'democrats', '@RepKatiePorter': 'democrats', '@SenTedCruz': 'republicans', '@SenatorBraun': 'republicans', '@SenKamalaHarris': 'democrats', '@RepDanKildee': 'democrats', '@RepLowenthal': 'democrats', '@BennieGThompson': 'democrats', '@SenMcSallyAZ': 'republicans', '@SenatorCarper': 'democrats', '@DesJarlaisTN04': 'republicans', '@MikeKellyPA': 'republicans', '@ChrisCoons': 'democrats', '@RepJerryNadler': 'democrats', '@RepClayHiggins': 'republicans', '@RepChuck': 'republicans', '@RepCarolMiller': 'republicans', '@RepDavid': 'republicans', '@RepKirkpatrick': 'democrats', '@NewAmerica': 'thinktanks', '@SenBlumenthal': 'democrats', '@RepPeteKing': 'republicans', '@RepJoseSerrano': 'democrats', '@NewAmericaEd': 'thinktanks', '@RepLawrence': 'democrats', '@JoaquinCastrotx': 'democrats', '@CongPalazzo': 'republicans', '@SenCapito': 'republicans', '@lisamurkowski': 'republicans', '@NEDemocracy': 'thinktanks', '@RepCarbajal': 'democrats', '@repgregwalden': 'republicans', '@RepTipton': 'republicans', '@RepJasonSmith': 'republicans', '@justinamash': 'independents', '@RepGusBilirakis': 'republicans', '@RepRaulGrijalva': 'democrats', '@RepDLesko': 'republicans', '@RepTomSuozzi': 'democrats', '@RepDavidKustoff': 'republicans', '@RepJoeNeguse': 'democrats', '@RepSusanWild': 'democrats', '@RepKevinBrady': 'republicans', '@SenCoryGardner': 'republicans', '@BrookingsMetro': 'thinktanks', '@RepDaveJoyce': 'republicans', '@RepJohnJoyce': 'republicans', '@RepShalala': 'democrats', '@JudgeCarter': 'republicans', '@SenatorMenendez': 'democrats', '@ChrisVanHollen': 'democrats', '@SenSchumer': 'democrats', '@RepBarbaraLee': 'democrats', '@RepMikeTurner': 'republicans', '@JimInhofe': 'republicans', '@SenatorWicker': 'republicans', '@SteveScalise': 'republicans', '@SenatorBennet': 'democrats', '@SenMikeLee': 'republicans', '@GKButterfield': 'democrats', '@RepPerlmutter': 'democrats', '@RepByrne': 'republicans', '@RepWexton': 'democrats', '@RepTedDeutch': 'democrats', '@RepBonamici': 'democrats', '@CongBoyle': 'democrats', '@JerryMoran': 'republicans', '@CAPenergypolicy': 'thinktanks', '@AIPAC': 'thinktanks', '@SenatorDurbin': 'democrats', '@RepHolding': 'republicans', '@SenatorRomney': 'republicans', '@RepSusanDavis': 'democrats', '@RepKClark': 'democrats', '@RepMarthaRoby': 'republicans', '@SenCortezMasto': 'democrats', '@RepDebDingell': 'democrats', '@RepCharlieCrist': 'democrats', '@RepRichmond': 'democrats', '@SenSherrodBrown': 'democrats', '@RepJasonCrow': 'democrats', '@CongressmanJVD': 'republicans', '@RepChuyGarcia': 'democrats', '@RepConorLamb': 'democrats', '@RepDerekKilmer': 'democrats', '@USRepLong': 'republicans', '@RepBillJohnson': 'republicans', '@RepBrianMast': 'republicans', '@MacTXPress': 'republicans', '@SenatorIsakson': 'republicans', '@RepDianaDeGette': 'democrats', '@RepMikeRogersAL': 'republicans', '@ChuckGrassley': 'republicans', '@JeffFortenberry': 'republicans', '@RepDavidEPrice': 'democrats', '@RepVeasey': 'democrats', '@RepMarkGreen': 'republicans', '@RepRubenGallego': 'democrats', '@RepTomGraves': 'republicans', '@MarshaBlackburn': 'republicans', '@RepAndyKimNJ': 'democrats', '@SenKevinCramer': 'republicans', '@SenSanders': 'independents', '@RepRussFulcher': 'republicans', '@RepGaramendi': 'democrats', '@SenFeinstein': 'democrats', '@SenDanSullivan': 'republicans', '@RepRichHudson': 'republicans', '@ConawayTX11': 'republicans', '@SpeakerPelosi': 'democrats', '@RepChrisStewart': 'republicans', '@CIS_org': 'thinktanks', '@RepWilson': 'democrats', '@boblatta': 'republicans', '@RepKenBuck': 'republicans', '@RepChipRoy': 'republicans', '@SteveDaines': 'republicans', '@SenatorLankford': 'republicans', '@SenatorCollins': 'republicans', '@RepAndyBarr': 'republicans', '@DrPhilRoe': 'republicans', '@RepFilemonVela': 'democrats', '@RepHuffman': 'democrats', '@RepLoisFrankel': 'democrats', '@SenShelby': 'republicans', '@RepSusieLee': 'democrats', '@RepGregSteube': 'republicans', '@SenWhitehouse': 'democrats', '@RepRichardNeal': 'democrats', '@RepGosar': 'republicans', '@RepKendraHorn': 'democrats', '@RepThompson': 'democrats', '@RepEliotEngel': 'democrats', '@RepCloudTX': 'republicans', '@RepSamGraves': 'republicans', '@RepAndyLevin': 'democrats', '@SanfordBishop': 'democrats', '@SenBrianSchatz': 'democrats', '@RepHastingsFL': 'democrats', '@Call_Me_Dutch': 'democrats', '@RepJoeWilson': 'republicans', '@RepTomReed': 'republicans', '@RepJimmyGomez': 'democrats', '@RepWesterman': 'republicans', '@RepSarbanes': 'democrats', '@SenRonJohnson': 'republicans', '@CongMikeSimpson': 'republicans', '@PattyMurray': 'democrats', '@LacyClayMO1': 'democrats', '@SenTomCotton': 'republicans', '@RepBillFoster': 'democrats', '@SenJohnBarrasso': 'republicans', '@reptimmons': 'republicans', '@SenatorFischer': 'republicans', '@SenAngusKing': 'independents', '@RepLoudermilk': 'republicans', '@RepBost': 'republicans', '@RepFrenchHill': 'republicans', '@SenJohnThune': 'republicans', '@USRepMikeDoyle': 'democrats', '@TulsiPress': 'democrats', '@MarkWarner': 'democrats', '@RepJoeMorelle': 'democrats', '@RepGrothman': 'republicans', '@RepDwightEvans': 'democrats', '@CongressmanRaja': 'democrats', '@RepHuizenga': 'republicans', '@RepScottPerry': 'republicans', '@SenatorTimScott': 'republicans', '@jahimes': 'democrats', '@SenatorBurr': 'republicans', '@RepJayapal': 'democrats', '@RepWalorski': 'republicans', '@SenToddYoung': 'republicans', '@repdelgado': 'democrats', '@RepStefanik': 'republicans', '@RepGregoryMeeks': 'democrats', '@RepHoulahan': 'democrats', '@RepRoybalAllard': 'democrats', '@sendavidperdue': 'republicans', '@RepBradWenstrup': 'republicans', '@AustinScottGA08': 'republicans', '@SenHydeSmith': 'republicans', '@RepAdams': 'democrats', '@RepJohnCurtis': 'republicans', '@RepLipinski': 'democrats', '@RepMikeLevin': 'democrats', '@RepArrington': 'republicans', '@RepTerriSewell': 'democrats', '@SenStabenow': 'democrats', '@RepDarrenSoto': 'democrats', '@RepBuddyCarter': 'republicans', '@RepRalphNorman': 'republicans', '@RepCasten': 'democrats', '@SenatorRounds': 'republicans', '@RepAndreCarson': 'democrats', '@SenatorSinema': 'democrats', '@RepBonnie': 'democrats', '@RepFletcher': 'democrats', '@RepLarryBucshon': 'republicans', '@RepSteveStivers': 'republicans', '@RepAdamSchiff': 'democrats', '@FrankPallone': 'democrats', '@BillPascrell': 'democrats', '@congbillposey': 'republicans', '@SenatorBaldwin': 'democrats', '@GReschenthaler': 'republicans', '@USRepKeating': 'democrats', '@RepRWilliams': 'republicans', '@RepPressley': 'democrats', '@davidcicilline': 'democrats', '@SenGaryPeters': 'democrats', '@RepDMP': 'democrats', '@RepAbraham': 'republicans', '@RepKarenBass': 'democrats', '@RepGregStanton': 'democrats', '@RepDustyJohnson': 'republicans', '@RepRickLarsen': 'democrats', '@hrw': 'thinktanks', '@CSIS': 'thinktanks', '@RepMcEachin': 'democrats', '@RepBillFlores': 'republicans', '@RepBrianHiggins': 'democrats', '@daveloebsack': 'democrats', '@RepHarley': 'democrats', '@RepZoeLofgren': 'democrats', '@SenBobCasey': 'democrats', '@SenJackyRosen': 'democrats', '@RepAndyHarrisMD': 'republicans', '@RandPaul': 'republicans', '@RepPeteOlson': 'republicans', '@RepHorsford': 'democrats', '@RepTjCox': 'democrats', '@RepCindyAxne': 'democrats', '@SenatorRisch': 'republicans', '@RepDougCollins': 'republicans', '@RepMalinowski': 'democrats', '@RepKayGranger': 'republicans', '@SenBillCassidy': 'republicans', '@BrookingsGlobal': 'thinktanks', '@RepMaxineWaters': 'democrats', '@RepBarragan': 'democrats', '@RepFredUpton': 'republicans', '@DorisMatsui': 'democrats', '@RepHagedorn': 'republicans', '@MarkAmodeiNV2': 'republicans', '@RepLloydDoggett': 'democrats', '@RepCuellar': 'democrats', '@RepGwenMoore': 'democrats', '@JohnCornyn': 'republicans', '@RepMoolenaar': 'republicans', '@RepBrindisi': 'democrats', '@RepPeteStauber': 'republicans', '@SenMarkey': 'democrats', '@RepRutherfordFL': 'republicans', '@RepDrewFerguson': 'republicans', '@senrobportman': 'republicans', '@RepSchrader': 'democrats', '@RepJohnKatko': 'republicans', '@RepCunningham': 'democrats', '@KenCalvert': 'republicans', '@RepJoshG': 'democrats', '@RoyBlunt': 'republicans', '@RepBlaine': 'republicans', '@repjimcooper': 'democrats', '@RodneyDavis': 'republicans', '@RepColinAllred': 'democrats', '@RepBobbyRush': 'democrats', '@RepRaskin': 'democrats', '@repdinatitus': 'democrats', '@SenJeffMerkley': 'democrats', '@CFR_org': 'thinktanks', '@RepStephMurphy': 'democrats', '@RepKenMarchant': 'republicans', '@RepJimmyPanetta': 'democrats', '@SenHawleyPress': 'republicans', '@RepBrownley': 'democrats', '@RepWalterJones': 'republicans', '@MartinHeinrich': 'democrats', '@SenWarren': 'democrats', '@RepEdCase': 'democrats', '@RepJimBanks': 'republicans', '@RepJohnYarmuth': 'democrats', '@SenJohnHoeven': 'republicans', '@RepBera': 'democrats', '@RepFrankLucas': 'republicans', '@gillibrand': 'democrats', '@RepNewhouse': 'republicans', '@SenatorLeahy': 'democrats', '@RepJimBaird': 'republicans', '@repmarkpocan': 'democrats', '@RepLouCorrea': 'democrats', '@RepCheri': 'democrats', '@SusanWBrooks': 'republicans', '@BradSherman': 'democrats', '@RepChrisSmith': 'republicans', '@JohnBoozman': 'republicans', '@RepDavidTrone': 'democrats', '@cathymcmorris': 'republicans', '@RepMarkMeadows': 'republicans', '@RepSchneider': 'democrats', '@RepJohnLarson': 'democrats', '@SenTinaSmith': 'democrats', '@EconomicPolicy': 'thinktanks', '@RepBryanSteil': 'republicans', '@JacksonLeeTX18': 'democrats', '@RepCohen': 'democrats', '@RepKimSchrier': 'democrats', '@RepEspaillat': 'democrats', '@BrookingsGov': 'thinktanks', '@NormaJTorres': 'democrats', '@RepLoriTrahan': 'democrats', '@repbenraylujan': 'democrats', '@RepDonaldPayne': 'democrats', '@repkevinhern': 'republicans', '@RepWalberg': 'republicans', '@USRepKCastor': 'democrats', '@repblumenauer': 'democrats', '@RepGonzalez': 'republicans', '@EdProgress': 'thinktanks', '@RepGallagher': 'republicans', '@RepSlotkin': 'democrats', '@TomColeOK04': 'republicans', '@JimLangevin': 'democrats', '@CarnegieEndow': 'thinktanks', '@RepMaloney': 'democrats', '@CAPimmigration': 'thinktanks', '@NydiaVelazquez': 'democrats', '@RepShimkus': 'republicans', '@rep_stevewomack': 'republicans', '@RepRonEstes': 'republicans', '@RepAnnieKuster': 'democrats', '@RepMeuser': 'republicans', '@RepLaMalfa': 'republicans', '@VernBuchanan': 'republicans', '@RepChrisPappas': 'democrats', '@RepRiggleman': 'republicans', '@RepJohnRose': 'republicans', '@RepMarciaFudge': 'democrats', '@RepDeSaulnier': 'democrats', '@RepGraceMeng': 'democrats', '@SenDougJones': 'democrats', '@replouiegohmert': 'republicans', '@RepLucyMcBath': 'democrats', '@RepGregPence': 'republicans', '@RepAOC': 'democrats', '@RepGilCisneros': 'democrats', '@RepLaHood': 'republicans', '@Robert_Aderholt': 'republicans', '@RepMcKinley': 'republicans', '@WhipClyburn': 'democrats', '@RepJudyChu': 'democrats', '@SenAlexander': 'republicans', '@RepRonKind': 'democrats', '@RepJoeCourtney': 'democrats', '@RepSires': 'democrats', '@RonWyden': 'democrats', '@RepTomRice': 'republicans', '@RepLizCheney': 'republicans', '@RepRickAllen': 'republicans', '@RepSwalwell': 'democrats', '@SenatorTomUdall': 'democrats', '@RepCardenas': 'democrats', '@RepThomasMassie': 'republicans', '@RepAndyBiggsAZ': 'republicans', '@LindseyGrahamSC': 'republicans', '@RepYvetteClarke': 'democrats', '@RepTimRyan': 'democrats', '@USRepGaryPalmer': 'republicans', '@repjohnlewis': 'democrats', '@RepHaleyStevens': 'democrats', '@RepJoeKennedy': 'democrats', '@RepScottPeters': 'democrats', '@SenSasse': 'republicans', '@RepPeterDeFazio': 'democrats', '@repdonyoung': 'republicans', '@RepAnnaEshoo': 'democrats', '@RepKinzinger': 'republicans', '@Ilhan': 'democrats', '@RepJoshHarder': 'democrats', '@RepDavids': 'democrats', '@RepMikeJohnson': 'republicans', '@SenatorCardin': 'democrats', '@RepEBJ': 'democrats', '@RepJeffDuncan': 'republicans', '@RepKathleenRice': 'democrats', '@urbaninstitute': 'thinktanks', '@RepMattGaetz': 'republicans', '@RepBalderson': 'republicans', '@SenPatRoberts': 'republicans', '@RepMoBrooks': 'republicans', '@RepArmstrongND': 'republicans', '@RepHalRogers': 'republicans', '@RepMcClintock': 'republicans', '@RepJimCosta': 'democrats', '@RepRobinKelly': 'democrats', '@LeaderHoyer': 'democrats', '@RepGolden': 'democrats', '@RepMarkWalker': 'republicans', '@RepAngieCraig': 'democrats', '@RepMaxRose': 'democrats', '@RepVisclosky': 'democrats', '@repcleaver': 'democrats', '@Sen_JoeManchin': 'democrats', '@RepValDemings': 'democrats', '@RepBobGibbs': 'republicans', '@RepTedLieu': 'democrats', '@RepDanCrenshaw': 'republicans', '@RepSpeier': 'democrats', '@SenThomTillis': 'republicans', '@RepAGonzalez': 'republicans', '@GerryConnolly': 'democrats', '@gracenapolitano': 'democrats', '@RepDavidRouzer': 'republicans', '@RepBenMcAdams': 'democrats', '@RepPaulCook': 'republicans', '@RepTrentKelly': 'republicans', '@SenToomey': 'republicans', '@Jim_Jordan': 'republicans', '@RepSeanMaloney': 'democrats', '@RepAlLawsonJr': 'democrats', '@GOPLeader': 'republicans', '@RepMichaelWaltz': 'republicans', '@RepAnnWagner': 'republicans', '@RepOHalleran': 'democrats', '@RepBrianBabin': 'republicans', '@RepSmucker': 'republicans', '@RepMikeQuigley': 'democrats', '@OceanProgress': 'thinktanks', '@RepMarcyKaptur': 'democrats', '@RepVanTaylor': 'republicans', '@RepDennyHeck': 'democrats', '@JimPressOffice': 'republicans', '@RepSteveChabot': 'republicans', '@RepGuthrie': 'republicans', '@RepHankJohnson': 'democrats', '@RepMichaelGuest': 'republicans', '@HerreraBeutler': 'republicans', '@SenDuckworth' : 'democrats'}


def makeNetworkList(filepath = '/Users/kabirkapur/Desktop/TweetTracker/Untruncated With RTs'):
	''' tells you which accounts are 'in-network'. Accounts are considered in-network 
if they are accounts of American congresspeople or select think tanks.'''
	ls = []
	for i in list(os.listdir(filepath)): # returns tuple with index 2 value being a list
		content = i[:(len(i)-len('tweets.csv'))] # assuming the directory follows my pesonal naming convention for theese files
		if '@' in content and 'tweets' in i: # only congressional accounts have '@' in the name as per my nomenclature choices
			ls.append(content)
	if len(ls) == 0:
		ls = None
	return ls # return congressional accounts and thinkTanks list


def makeAdjMatrix(ls = None, filepath = '/Users/kabirkapur/Desktop/TweetTracker/Untruncated With RTs'):
	'''array representation -- rows: account itself ('from') columnns: rt account ('to') 
	intersection: weight of connection (number of times from rtd to'''
	row = {rt_acct : 0 for rt_acct in ls}
	adj = {acct : row for acct in ls} # master dict
	count = 0
	innercount = 0
	
	# filepath = '/Users/kabirkapur/Desktop/TweetTracker/Untruncated With RTs'
	# filepath = '/Users/kabirkapur/Desktop/TweetTracker/Untruncated With RTs'
	if ls == None:
		print("Call makeNetworkList() function on a valid directory")
		return
	for i in list(os.listdir(filepath)): # returns tuple with index 2 value being a list
		pathAndName = filepath + "/" + str(i)
		user = str(i)
		count += 1
		if ('.csv' in user):
			with open(pathAndName, "r") as f:
				innerdict = {}
				reader = csv.reader(f, delimiter=',')
				for j in reader:	
					innercount += 1
					try:	
						if 'RT @' in j[4] and (j[4].split(' ')[1][:len(j[4].split(' ')[1]) - 1]) in ls:
							try:
								adj[user[:(len(user)-len('tweets.csv'))]][j[4].split(' ')[1][:len(j[4].split(' ')[1]) - 1]] += 1
							except KeyError: 
								print(user[:(len(user)-len('tweets.csv'))])
					except IndexError:
						print("IndexError handling " + i + "!")
	return adj		



def makePartiesDict(inputList = makeNetworkList()):
	'''use manual input to create a dictionary to record party affiliation.
	The Dictionary: 
	keys -- account handles
	values -- party affiliation/status as thinktank
	Since the function requires manual input, the user is expected to keep track of the dictionary on their own accord'''
	outputDict = {}
	possibilities = ['r', 'd', 'i', 't']
	try:	
		print("Would you like to skip to a certain index? y/n")
		skip = input()
		if skip == "y":
			print("Enter key: ")
			skipAcct = input()
			i = inputList.index(skipAcct)
		elif skip == "n":
			i = 0
		while i < len(inputList):
			print("Enter party abbreviation for " + inputList[i] + ", or enter undo, redo, or print: ")
			val = input()
			if val == "redo" or val == "redo ":
				i -= 1
			elif val == "skip" or val == "undo ":
				i += 1
			elif val == "print" or val == "print ":
				print(outputDict)
				print("Next index: " + inputList[i+1])
			elif val in possibilities:
				outputDict[inputList[i]] = val
				i += 1
			else:
				print("Invalid input! Try again.")
	except KeyboardInterrupt:
		print(outputDict)
		print("Next index: " + inputList[i+1])
		return(outputDict)
	print(outputDict)
	return outputDict

					
def makeDiGraph(adjacencyMatrix = None):
	G = nx.DiGraph() # DiGraph is a directed graph with looping
	for i in adjacencyMatrix:
		G.add_node(i)
	for i in adjacencyMatrix:
		for j in adjacencyMatrix[i]:
			if adjacencyMatrix[i][j] > 0:
				G.add_edge(i, j, weight = adjacencyMatrix[i][j])
	# nx.nx_agraph.graphviz_layout(G, prog = 'my_shit') # need pygraphviz and that is a whole ordeal
	plt.figure(figsize = (20,20))
	nx.draw_circular(G)
	plt.show()