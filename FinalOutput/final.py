class Players:
    def __init__(self, bowlers, batsmen, wk, ar):
        self.bowlers = bowlers
        self.batsmen = batsmen
        self.wk = wk
        self.ar = ar
        self.total = 100
        self.selected = []

    def bifurcation(self, bowC, batC, wkC, arC):
        self.bowC = bowC
        self.batC = batC
        self.wkC = wkC
        self.arC = arC

    def knapsack(self):
        k1 = Knap(self.bowlers, self.bowC)
        k2 = Knap(self.batsmen, self.batC)
        k3 = Knap(self.ar, self.arC)
        k4 = Knap(self.wk, self.wkC)

        k1.algorithm()
        k2.algorithm()
        k3.algorithm()
        k4.algorithm()

        self.selected.append(k1.getItemsUsed())
        self.selected.append(k2.getItemsUsed())
        self.selected.append(k3.getItemsUsed())
        self.selected.append(k4.getItemsUsed())

        return self.selected

class Player:
    def __init__(self, credit, score):
        self.credit = credit
        self.score = score

    def __init__(self, credit):
        self.credit = credit

class Knap:
    """
        Class used for Knapsack implementation. \ Consists of two functions used for computing table, and one for evaluating which actors were chosen to create the table.
    """

    def __init__(self, players, total):
        """
            Constructor used to initialize variables used everywhere in the function.
            @param weights: Cost of each actor is stored in this list.
            @param total: This variable is used to denote the total budget.
            @param profit: This list indicates the profit of choosing an actor.
        """
        self.players = players
        self.total = total
        self.n = self.players.__len__()
        self.selected = np.zeros((self.n, self.total + 1))

    def getItemsUsed(self):
        """
            Once the table of the Knapsack Algorithm is constructed, this function can be used to determine which actors were used to get this table.
            @return Set of actors (in 0s and 1s) that maximize profit and keep the total cost in the budget as determined by Knapsack.
        """
        self.marked = np.zeros(self.n)
        i = self.n - 1
        currentW = self.total
        while (i >= 0 and currentW >= 0):
            if (i == 0 and self.selected[i, np.int(currentW)] > 0) or (i != 0 and self.selected[i, np.int(currentW)] != self.selected[i - 1, np.int(currentW)]):
                self.marked[i] = 1
                currentW = currentW - self.players[i].credit
            i = i - 1
        return self.marked

    def algorithm(self):
        """
            This function is used to compute the table in the Knapsack Algorithm. This table ```self.selected``` indicates the best profit for a set of actors.
            @return List containing the maximum profit, and the set of actors used to get this profit
        """
        for i in range(0, self.n):
            for j in range(0, self.total + 1):
                if self.players[i].credit > j:
                    self.selected[i][j] = self.selected[i - 1][j]
                else:
                    self.selected[i,j] = np.maximum(self.selected[i-1,j],self.players[i].score+self.selected[i-1,j-np.int(self.players[i].credit)])
        return [self.selected[self.n-1,np.int(self.total)], self.getItemsUsed()]





