"""
@file File Documentation
"""


class AllNames:
    """Class that determines the names of players playing in a match with the name of the corresponding player in the dataset. Since both of these come from different sources, there is a big possibilities that the names do not match.
    """

    def __init__(self, first, second):
        """!Constructor that defines the players playing in the match, and the list of all players in the dataset to which these names are to be mapped.
        @param first: List of all names playing in the match.
        @param second: List of all names of players in the dataset.
        """
        # List of names of players playing in that match. Nomenclature is defined by Dream11 website.
        self.fr = first
        # List of names of players in the dataset. This nomenclature is independant of Dream11.
        self.sn = second
        self.first = []
        self.second = []

        '''def __init__(self, dream11, allcsv):
        """!Constructor that opens files where the list of players playing in a match are stored, and the list of all names contained in the dataset.
        @param dream11: Name of file containing names of players playing in the match.
        @param allcsv: Name of file containing names of players contained in the dataset.
        """
        ##File object of the file containing the players playing in this match.
        self.dream11 = open(dream11, 'r')
        ##File object of the file containing the players in the entire dataset.
        self.allcsv = open(allcsv, 'r')
        self.first = []
        self.second = []'''

    def get_players(self):
        """Using the file objects of self, this function populates the list ```self.first``` and ```self.second```.
        """

        for i in self.fr:
            self.first.append(FullName(i.replace(" ", "")))
        ls = []
        for i in self.sn:
            self.second.append(FullName(i[0:-1].replace(" ", "")))
            ls.append(i[0:-1].replace(" ", ""))
        self.sn = ls

        '''
        x = 0
        try:
            while True:
                p = next(self.dream11)
                self.first.append(FullName(p[0:-1].replace(" ", "")))
        except:
            x = 0
        try:
            while True:
                p = next(self.allcsv)
                self.second.append(FullName(p[0:-1].replace(" ", "")))
        except:
            x = 0
	'''

    def print_all_players(self):
        """Function simply prints the set of players playing in the match, and the set of players in the dataset. Used in the initial stages of development for debugging purposes.
        """
        print(self.first)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(self.second)

    def mapped_player(self, player):
        """!Given a particular player with name given as per Dream11, this function determines what the player's name is most likely to be in the dataset.
        @param player: FullName object of a player playing in the match. The name is given as per Dream11 nomenclature.
        """
        index = 0
        maxlcs = 0
        pls = []
        for i in range(len(self.second)):
            if player.small == self.second[i].small:
                pls.append(self.second[i])
        pl = FullName('')
        for i in range(len(pls)):
            lcs = LCS(player.caps, pls[i].caps)
            if lcs > maxlcs:
                maxlcs = lcs
                pl = pls[i]
        return pl

    def all_players(self):
        """Determines the names of all the players playing in the match by mapping it to the dataset names. Uses the function ```self.mapped_player(...)``` internally.
        """
        name = []
        indx = []
        for i in range(len(self.first)):
            
            p = self.mapped_player(self.first[i])

            try:
                t = self.sn.index(p.fullname)
                name.append(p.fullname)
                indx.append(t)
            except:
                t = -1
        return(name , indx)

class FullName:
    """Class that contains information related to an individuals name. This information can be used to determine what the name might be mapped to if written in a different format.
    """

    def __init__(self, name):
        """!Constructor used to initialize a player's full name.
        @param name: Player's name passed as a simple string
        """
        # Contains the list of capital letters (initials) in a person's name
        self.caps = get_initials(name)
        # Contains the list of small letters in a person's name
        self.small = get_small(name)
        # Contains the name of the person.directly
        self.fullname = name


def get_initials(s):
    """!Function that returns the initials of the name passed as argument.
    @param s: Name passed as string to the function
    """
    l = ''
    for ch in s:
        if ch.isupper():
            l += ch
    return l


def get_small(s):
    """!Function that returns the list of all small characters in a person's name.
    @param s: Name passed as string to the function
    """
    l = ''
    for ch in s:
        if ch.islower():
            l += ch
    return l


def LCS(s1, s2):
    """!Function that returns the length of the longest common subsequence (LCS) between two strings. LCS can be used as a heuristic to determine how similar two names are.
    @param s1: First string
    @param s2: Second string
    @return Length of the longest common subsequence.
    """
    m = len(s1)
    n = len(s2)

    L = [[None]*(n + 1) for i in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif s1[i - 1] == s2[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    return L[m][n]


def ED(s1, s2):
    """!Function that returns the edit distance between two strings, i.e. The minimum number of insertions, deletions, and replacements to be done on one string to convert it to the other.
    @param s1: First String
    @param s2: Second String
    @return Edit distance between the two strings.
    """
    m = len(s1)
    n = len(s2)

    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1]
                                   [j], dp[i - 1][j - 1])
    return dp[m][n]


'''
allcsv = "allcsv.txt"
dream11 = "dream11.txt"
n = AllNames(dream11, allcsv)
n.get_players()
# n.print_all_players()
n.all_players()'''
