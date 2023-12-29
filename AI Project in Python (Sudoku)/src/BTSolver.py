import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time
import random
from collections import defaultdict

class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc

    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Part 1 TODO: Implement the Forward Checking Heuristic

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        Note: remember to trail.push variables before you assign them
        Return: a tuple of a dictionary and a bool. The dictionary contains all MODIFIED variables, mapped to their MODIFIED domain.
                The bool is true if assignment is consistent, false otherwise.
    """
    def forwardChecking ( self ):
        assignedVars = []

        # assigned variables
        for v in self.network.variables:
            if v.isAssigned():
                assignedVars.append(v)

        modVars = dict()
        for v in assignedVars:
            if v.isAssigned():
                for n in self.network.getNeighborsOfVariable(v):
                    if v.getAssignment() == n.getAssignment():
                        return (modVars, False)

                    if not n.isAssigned() and v.getAssignment() in n.domain.values:
                        self.trail.push(n)
                        n.removeValueFromDomain(v.getAssignment())
                        if n.size() == 0:
                            return (modVars, False)
                        if n.size() == 1:
                            n.assignValue(n.domain.values[0])
                            assignedVars.append(n)
                            # mod[n] = n.domain.values[0]

                        for c in self.network.getModifiedConstraints():
                            if not c.isConsistent():
                                return (modVars, False)
                            else:
                                modVars[n] = c

        return (modVars, True)


    # =================================================================
	# Arc Consistency
	# =================================================================
    def arcConsistency( self ):
        assignedVars = []
        for c in self.network.constraints:
            for v in c.vars:
                if v.isAssigned():
                    assignedVars.append(v)
        while len(assignedVars) != 0:
            av = assignedVars.pop(0)
            for neighbor in self.network.getNeighborsOfVariable(av):
                if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(av.getAssignment()):
                    neighbor.removeValueFromDomain(av.getAssignment())
                    if neighbor.domain.size() == 1:
                        neighbor.assignValue(neighbor.domain.values[0])
                        assignedVars.append(neighbor)

    
    """
        Part 2 TODO: Implement both of Norvig's Heuristics

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        (2) If a constraint has only one possible place for a value
            then put the value there.

        Note: remember to trail.push variables before you assign them
        Return: a pair of a dictionary and a bool. The dictionary contains all variables 
		        that were ASSIGNED during the whole NorvigCheck propagation, and mapped to the values that they were assigned.
                The bool is true if assignment is consistent, false otherwise.
    """
    def norvigCheck ( self ):
        assignedVars = {}
    
        if self.forwardChecking()[1]:

            for unit in self.network.constraints:
                counter = defaultdict(int)
                for i in range(1, self.gameboard.N):
                    for var in unit.vars:

                        # if var.domain.size() == 1 and not var.isAssigned():
                        #     assignedVars[var] = var.domain.values[0]
                        #     # self.trail.push(var)
                        #     var.assignValue(var.domain.values[0])
                        #     if not self.forwardChecking()[1]:
                        #         return (assignedVars, False)
                            

                        for value in var.domain.values:
                            counter[value] += 1
                
                for i in range(1, self.gameboard.N):
                    if counter[i] == 1:
                        for var in unit.vars:
                            if i in var.domain:
                                self.trail.push(var)
                                var.assignValue(i)
                                assignedVars[var] = i

        else:
            return (assignedVars, False)

        return (assignedVars, True)


    """
         Optional TODO: Implement your own advanced Constraint Propagation

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournCC ( self ):
        return self.norvigCheck()

    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Part 1 TODO: Implement the Minimum Remaining Value Heuristic

        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        vardict = dict()
        for var in self.network.variables:
            if not var.isAssigned():
                vardict[var] = var.domain.size()

        sortedvardict = sorted(vardict.items(), key=lambda x : x[1])
        if len(sortedvardict) > 0 and len(sortedvardict[0]) > 0:
            return sortedvardict[0][0]
        return None


    """
        Part 2 TODO: Implement the Minimum Remaining Value Heuristic
                       with Degree Heuristic as a Tie Breaker

        Return: The unassigned variable with the smallest domain and affecting the most unassigned neighbors.
                If there are multiple variables that have the same smallest domain with the same number of unassigned neighbors, add them to the list of Variables.
                If there is only one variable, return the list of size 1 containing that variable.
    """
    def MRVwithTieBreaker ( self ):

        # variable mapped to domain size
        vardict = dict() 
        for var in self.network.variables:
            if not var.isAssigned():
                vardict[var] = var.domain.size()

        # all spots have been filled, return None
        if len(vardict.keys()) == 0:
            return [None]

        mindomain = min(vardict.values())
        possibles = []

        # variables tied for having the smallest domain
        for k, v in vardict.items():
            if v == mindomain:
                possibles.append(k)

        return [possibles[0]]
            
        # no tie, return only choice
        if len(possibles) == 1:
            return [possibles[0]]

        # variable mapped to unassigned neighbor count
        vardict.clear()
        vardict = defaultdict(int)
        for v in possibles:
            for n in self.network.getNeighborsOfVariable(v):
                if not n.isAssigned():
                    ndomain = set(n.domain.values)
                    mydomain = set(v.domain.values)
                    z = ndomain.intersection(mydomain)
                    if len(z) > 0:
                        vardict[v] += 1

        maxunassigned = max(vardict.values())
        tr = []
        

        # variables tied for both cases
        for k, v in vardict.items():
            if v == maxunassigned:
                tr.append(k)
   
        # sanity check
        if len(tr) > 0:
            tr.sort(key=lambda x : x.name)
            return tr
        return [None]


        # vardict = dict()
        # for var in self.network.variables:
        #     if not var.isAssigned():
        #         vardict[var] = []
        #         vardict[var].append(var.domain.size())

        #         count = 0
        #         # mydomain = set(var.getDomain().values)

        #         for neighbor in self.network.getNeighborsOfVariable(var):
        #             if not neighbor.isAssigned():

        #                 # ndomain = set(neighbor.getDomain().values)
        #                 # overlap = ndomain.intersection(mydomain)
        #                 # if (len(overlap) > 0):
        #                 count += 1

        #         vardict[var].append(-1 * count)


        # if len(vardict) == 0:
        #     return [None]

        # sortedvardict = sorted(vardict.items(), key=lambda x : x[1])
        # tr = []

        # if len(sortedvardict) > 0 and len(sortedvardict[0]) > 0:

        #     for i in range(len(sortedvardict)):
        #         if sortedvardict[0][1] == sortedvardict[i][1]:
        #             tr.append(sortedvardict[i][0])

        #     return tr

        # return [None]



    """
         Optional TODO: Implement your own advanced Variable Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVar ( self ):
        return self.getMRV()

    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Part 1 TODO: Implement the Least Constraining Value Heuristic

        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.

        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """
    def getValuesLCVOrder ( self, v ):
        removaldict = {}
        dom = v.domain.values
        neighbors = self.network.getNeighborsOfVariable(v)

        for var in dom:
            removaldict[var] = 0

        for neighbor in neighbors:
            ndomain = neighbor.domain.values
            for option in ndomain:
                if option in removaldict:
                    removaldict[option] += 1

        sortedrmdict = [key for key, val in sorted(removaldict.items(), key = lambda x: x[1])]
        return sortedrmdict


    """
         Optional TODO: Implement your own advanced Value Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVal ( self, v ):
        return self.getValuesLCVOrder(v)

    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self, time_left=600):
        if time_left <= 60:
            return -1

        start_time = time.time()
        if self.hassolution:
            return 0

        # Variable Selection
        v = self.selectNextVariable()

        # check if the assigment is complete
        if ( v == None ):
            # Success
            self.hassolution = True
            return 0

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )

            # Assign the value
            v.assignValue( i )

            # Propagate constraints, check consistency, recur
            if self.checkConsistency():
                elapsed_time = time.time() - start_time 
                new_start_time = time_left - elapsed_time
                if self.solve(time_left=new_start_time) == -1:
                    return -1
                
            # If this assignment succeeded, return
            if self.hassolution:
                return 0

            # Otherwise backtrack
            self.trail.undo()
        
        return 0

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()[1]

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()[1]

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()[0]

        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)