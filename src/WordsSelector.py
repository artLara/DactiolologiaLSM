
class WordsSelector():
    def __init__(self):
        self.__sw = SimilarWords()

    def getFrase(self, wordsSet, selector='max'):
        if selector == 'max':
            return self.maxSelect(wordsSet)

        if selector == 'contextGraph':
            return self.ContextGraph(wordsSet)

        print(selector, 'does not an option, try with max or contextGraph')

    def maxSelect(self, wordsSet):
        pass

    def ContextGraph(self, wordsSet):
        pass

    def clean_with_context(self, words):
        V = len(words) ** 2
        INF = 999999
        def getProb(w1,w2):
            offset = 100000
            try:
                return dictFrec[(w1,w2)]*offset/maxFrec[1]
            except:
                return 1*offset/maxFrec[1]
        def getMI(w1,w2):
            offset = 100000
            try:
                # return dictFrec[(w1,w2)]*offset/maxFrec[1]
                return sw.mutualInformation.similitud(w1,w2)
            except:
                return 1/sw.mutualInformation.N

        def printSolution(dist):
            print("Following matrix shows the shortest distances\
        between every pair of vertices")
            for i in range(V):
                for j in range(V):
                    if(dist[i][j] == INF):
                        print("%7s\t" % ("INF"), end=" ")
                    else:
                        print("%.7f\t" % (dist[i][j]), end=' ')
                    if j == V-1:
                        print()

        graph = []
        for i in range(len(words)**2):
            tmp = []
            for j in range(len(words)**2):
                if i==j:
                    tmp.append(0)
                else:
                    tmp.append(INF)
            graph.append(tmp)

        tam = len(words)
        stride = tam
        sw=0
        for stride in range(tam,tam*(tam-1)+1,stride):
            for i in range(len(words)):
                for j in range(len(words)):
                    #Metric with probality
                    # graph[i+stride-tam][j+stride] = (words[sw][i][1] + words[sw+1][j][1]) * -getProb(words[sw][i][0],words[sw+1][j][0])

                    #Just MI
                    graph[i+stride-tam][j+stride] = -getMI(words[sw][i][0],words[sw+1][j][0])

                    # print('prob:(',words[sw][i][0],',',words[sw+1][j][0],')')
                    # graph[i+stride-tam][j+stride] = -getProb(words[sw][i][0],words[sw+1][j][0])

            sw += 1

        def initialise(V, dis, Next):
            # global dis, Next

            for i in range(V):
                for j in range(V):
                    dis[i][j] = graph[i][j]

                    # No edge between node
                    # i and j
                    if (graph[i][j] == INF):
                        Next[i][j] = -1
                    else:
                        Next[i][j] = j

            return dis, Next

        def constructPath(u, v, dis, Next):
            # global dis, Next

            # If there's no path between
            # node u and v, simply return
            # an empty array
            if (Next[u][v] == -1):
                return {}

            # Storing the path in a vector
            path = [u]
            values = []
            while (u != v):
                oldu = u
                u = Next[u][v]
                path.append(u)
                values.append(dis[oldu][u])

            return path, values

        # Standard Floyd Warshall Algorithm
        # with little modification Now if we find
        # that dis[i][j] > dis[i][k] + dis[k][j]
        # then we modify next[i][j] = next[i][k]
        def floydWarshall(V, dis, Next):
            # maxOptWords = 7
            # global dist, Next
            for k in range(V):
                for i in range(V):
                    # for j in range(V):
                    for j in range((i//maxOptWords+1) * maxOptWords, V, 1):
                        # We cannot travel through
                        # edge that doesn't exist
                        if (dis[i][k] == INF or dis[k][j] == INF):
                            continue
                        if (dis[i][j] > dis[i][k] + dis[k][j]):
                            dis[i][j] = dis[i][k] + dis[k][j]
                            Next[i][j] = Next[i][k]
            return dis, Next

        # Print the shortest path
        def printPath(path):
            n = len(path)
            if n==0:
                print('Not path')
                return
            for i in range(n - 1):
                print(path[i], end=" -> ")
            print(path[n - 1])

        MAXM,INF = 1000,INF
        dis = [[-1 for i in range(MAXM)] for i in range(MAXM)]
        Next = [[-1 for i in range(MAXM)] for i in range(MAXM)]

        # Function to initialise the
        # distance and Next array
        dis, Next = initialise(V,dis, Next)

        # Calling Floyd Warshall Algorithm,
        # this will update the shortest
        # distance as well as Next array
        dis, Next = floydWarshall(V, dis, Next)
        path = []
        # printSolution(dis)
        # Path from node 1 to 3
        shortes = INF
        start = -1
        end = -1
        for i in range(len(words)):
            for j in range(len(words)):
                # print("Shortest path from 0 to : 12", end = "")
                if shortes > dis[i][j+(len(words)* (len(words)-1))]:
                    shortes = dis[i][j+(len(words)* (len(words)-1))]
                    start = i
                    end = j+(len(words)* (len(words)-1))

        # print('start:',start,' end=',end)
        # print(constructPath(start, end, dis, Next))
        path, values = constructPath(start, end, dis, Next)
        # printPath(path)
        res = []
        for i,j in enumerate(path):
            # print(words[i][j-(tam*i)][0], end='->')
            res.append(words[i][j-(tam*i)][0])
        # print('')
        # print('value:', dis[start][end])
        # print(res)
        return res
