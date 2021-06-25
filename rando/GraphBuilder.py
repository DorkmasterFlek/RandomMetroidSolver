
import utils.log, random, copy

from graph.graph_utils import GraphUtils, vanillaTransitions, vanillaBossesTransitions, escapeSource, escapeTargets
from logic.logic import Logic
from graph.graph import AccessGraphRando as AccessGraph

# creates graph and handles randomized escape
class GraphBuilder(object):
    def __init__(self, graphSettings):
        self.graphSettings = graphSettings
        self.areaRando = graphSettings.areaRando
        self.bossRando = graphSettings.bossRando
        self.escapeRando = graphSettings.escapeRando
        self.minimizerN = graphSettings.minimizerN
        self.log = utils.log.get('GraphBuilder')

    # builds everything but escape transitions
    def createGraph(self):
        transitions = self.graphSettings.plandoRandoTransitions
        if transitions is None:
            transitions = []
            if self.minimizerN is not None:
                transitions = GraphUtils.createMinimizerTransitions(self.graphSettings.startAP, self.minimizerN)
            else:
                if not self.bossRando:
                    transitions += vanillaBossesTransitions
                else:
                    transitions += GraphUtils.createBossesTransitions()
                if not self.areaRando:
                    transitions += vanillaTransitions
                else:
                    transitions += GraphUtils.createAreaTransitions(self.graphSettings.lightAreaRando)
        return AccessGraph(Logic.accessPoints, transitions, self.graphSettings.dotFile)

    # fills in escape transitions if escape rando is enabled
    def escapeGraph(self, container, graph, maxDiff):
        if not self.escapeRando:
            return
        possibleTargets, dst, path = self.getPossibleEscapeTargets(container, graph, maxDiff)
        # update graph with escape transition
        graph.addTransition(escapeSource, dst)
        # get timer value
        self.escapeTimer(graph, path)
        self.log.debug("escapeGraph: ({}, {}) timer: {}".format(escapeSource, dst, graph.EscapeAttributes['Timer']))
        # animals
        GraphUtils.escapeAnimalsTransitions(graph, possibleTargets, dst)

    def getPossibleEscapeTargets(self, container, graph, maxDiff):
        emptyContainer = copy.copy(container)
        emptyContainer.resetCollected()
        sm = emptyContainer.sm
        # setup smbm with item pool
        # Ice not usable because of hyper beam
        # remove energy to avoid hell runs
        # (will add bosses as well)
        sm.addItems([item.Type for item in emptyContainer.itemPool if item.Type != 'Ice' and item.Category != 'Energy'])
        sm.addItem('Hyper')
        possibleTargets = [target for target in escapeTargets if graph.accessPath(sm, target, 'Landing Site', maxDiff) is not None]
        self.log.debug('getPossibleEscapeTargets. targets='+str(possibleTargets))
        # failsafe
        if len(possibleTargets) == 0:
            self.log.debug("Can't randomize escape, fallback to vanilla")
            possibleTargets.append('Climb Bottom Left')
        random.shuffle(possibleTargets)
        # pick one
        dst = possibleTargets.pop()
        path = graph.accessPath(sm, dst, 'Landing Site', maxDiff)
        # cleanup smbm
        sm.resetItems()
        return (possibleTargets, dst, path)

    # path: as returned by AccessGraph.accessPath
    def escapeTimer(self, graph, path):
        if self.areaRando == True:
            if path[0].Name == 'Climb Bottom Left':
                graph.EscapeAttributes['Timer'] = None
                return
            traversedAreas = list(set([ap.GraphArea for ap in path]))
            self.log.debug("escapeTimer path: " + str([ap.Name for ap in path]))
            self.log.debug("escapeTimer traversedAreas: " + str(traversedAreas))
            # rough estimates of navigation within areas to reach "borders"
            # (can obviously be completely off wrt to actual path, but on the generous side)
            traversals = {
                'Crateria':90,
                'GreenPinkBrinstar':90,
                'WreckedShip':120,
                'LowerNorfair':135,
                'WestMaridia':75,
                'EastMaridia':100,
                'RedBrinstar':75,
                'Norfair': 120,
                # can't be on the path
                'Kraid': 0,
                'Tourian': 0,
                'Crocomire': 0
            }
            t = 90
            for area in traversedAreas:
                t += traversals[area]
            t = max(t, 180)
        else:
            escapeTargetsTimer = {
                'Climb Bottom Left': None, # vanilla
                'Green Brinstar Main Shaft Top Left': 210, # brinstar
                'Basement Left': 210, # wrecked ship
                'Business Center Mid Left': 270, # norfair
                'Crab Hole Bottom Right': 270 # maridia
            }
            t = escapeTargetsTimer[path[0].Name]
        self.log.debug("escapeTimer. t="+str(t))
        graph.EscapeAttributes['Timer'] = t
