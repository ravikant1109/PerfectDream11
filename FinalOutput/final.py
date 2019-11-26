class Players:
    def __init__(self, bowlers, batsmen, wk, ar):
        self.bowlers = bowlers
        self.batsmen = batsmen
        self.wk = wk
        self.ar = ar
        self.total = 100
        self.selected = []

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

    def __init__(self, weights, total, profit):
        """
            Constructor used to initialize variables used everywhere in the function.
            @param weights: Cost of each actor is stored in this list.
            @param total: This variable is used to denote the total budget.
            @param profit: This list indicates the profit of choosing an actor.
        """
        self.weights = weights
        self.total = total
        self.profit = profit
        self.n = self.profit.__len__()
        self.selected = np.zeros((self.n, self.total + 1))
        print(self.weights)

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
                currentW = currentW - self.weights[i]
            i = i - 1
        return self.marked

    def algorithm(self):
        """
            This function is used to compute the table in the Knapsack Algorithm. This table ```self.selected``` indicates the best profit for a set of actors.
            @return List containing the maximum profit, and the set of actors used to get this profit
        """
        for i in range(0, self.n):
            for j in range(0, self.total + 1):
                if self.weights[i] > j:
                    self.selected[i][j] = self.selected[i - 1][j]
                else:
                    self.selected[i,j] = np.maximum(self.selected[i-1,j],self.profit[i]+self.selected[i-1,j-np.int(self.weights[i])])
        return [self.selected[self.n-1,np.int(self.total)], self.getItemsUsed()]

