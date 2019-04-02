"""
Connect 4 AI player , it isn't dumb enough to lose to me at least. 6 plies takes about a minute each move. 
"""
__author__ = "Nathaniel Livingston" 
__license__ = "MIT"
__date__ = "February 2018"

import random

class ComputerPlayer:
    
    playerID = 0
    difficulty = 0
    rows = 0
    columns = 0
    
    def __init__(self, id, difficulty_level):
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        self.playerID = id
        self.difficulty = difficulty_level
        
    def pick_move(self, rack):
        """
        Pick the move to make. It will be passed a rack with the current board
        layout, column-major. A 0 indicates no token is there, and 1 or 2
        indicate discs from the two players. Column 0 is on the left, and row 0 
        is on the bottom. It must return an int indicating in which column to 
        drop a disc. The player current just pauses for half a second (for 
        effect), and then chooses a random valid move.
        """
        
        if(self.playerID == 1): # determine the IDs
            enemypid = 2
        else:
            enemypid = 1
            
        possibleMoves = {} # prepare a map of moves and their alphas
        
        for col in range(len(rack)): # fill the map
            if self.isPossibleMove(rack, col):
                temp = self.makeMove(rack, col, self.playerID)
                possibleMoves[col]=-self.search(self.difficulty-1, temp, enemypid) # recursively
                
        winningAlpha = -1000000
        winningMove = None
        
        moves = possibleMoves.items()
        random.shuffle(list(moves)) # shuffle it for some sweet randomness
        
        for move, alpha in moves: # go through the list and find the winning move
            if alpha >= winningAlpha:
                winningAlpha = alpha
                winningMove = move
        
        return winningMove
    

    def search(self, depth, rack, pid):
        """
        The search function, finds and returns the alpha of the best move given a rack, player, and depth to search to.
        """
        possibleMoves = [] # prepare you possible moves
        
        if(pid == 1): # determine players
            enemypid = 2
        else:
            enemypid = 1
        
        for i in range(len(rack)): # fill out the possible moves
            if self.isPossibleMove(rack, i):
                temp = self.makeMove(rack, i, pid)
                possibleMoves.append(temp)

        if (depth == 0 or len(possibleMoves) == 0 or self.isGameOver(rack)): # if the game is over, finish
            return self.calcStateValue(rack, pid)

        alpha = -1000000
        for child in possibleMoves: # go through the children
            if (child == None):
                print("no child, how did we let this happen!?")
            alpha = max(alpha, -self.search(depth-1, child, enemypid)) # keep only the child with the greatest alpha
        return alpha


    def isGameOver(self, rack):
        """
        Determines if the game is over or not given a rack. 
        """
        # the number comparisons here are flawed, it could make mistakes with an enourmous board, but it would take 100 3 in a rows to offset an enemy win
        if(self.calcStateValue(rack,1))>=90000: # player 1 win
            return True
        elif(self.calcStateValue(rack,2))>=90000: # player 2 win
            return True
        else: return False
        
        
    def makeMove(self, rack, col, pid):
        """
        Makes a move given a rack, column and pid. Returns the rack with the move completed. 
        """
        
        temp = list(map(list, rack))

        for i in range(len(rack)):
            if(rack[col][i] == 0): # fill in the first 0
                index = i
                break
        
        temp[col][index] = pid
        newRack = tuple(temp)
        return newRack # return the new rack   
    
        
        
    def isPossibleMove(self, rack, col):
        """
        Determines if a given move is possible or not, given the rack and the column.
        """
        for i in range(len(rack[0])):
            if(rack[col][i] == 0): # a 0 means you can move in that column
                return True
        return False
            
     
    def calcStateValue(self, rack, pid):
        """
        Given a rack and a player, determines the heuristic point value for that rack for that player. 
        """
        rackPoints = 0
        
        if(pid == 1): # determine players
            enemypid = 2
        else:
            enemypid = 1
            
        numCols = len(rack)
        numRows = len(rack[1])
        
        for i in range(numCols): # for each space, determine the points you get and subtract the points your opponent gets
            for j in range(numRows):
                rackPoints += self.verticalPoints(j,i,rack,pid)
                rackPoints += self.horizontalPoints(j,i,rack,pid)
                rackPoints += self.diagonalPoints(j,i,rack,pid)
                
                rackPoints -= self.verticalPoints(j,i,rack,enemypid)
                rackPoints -= self.horizontalPoints(j,i,rack,enemypid)
                rackPoints -= self.diagonalPoints(j,i,rack,enemypid)
        return rackPoints # return the point total
            
    def verticalPoints(self, row, col, rack, pid):
        """
        Determines the number of vertical points a space is worth for a given tile location, rack, and player.
        Only checks backwards. 
        """
        
        if(pid == 1): # determine players
            enemypid = 2
        else:
            enemypid = 1
        
        
        consecutive = 0
        
        if ((row-3) < 0): # if there's not enough space
            return 0 # it's worth nothing 
        
        for i in range(row, (row-4), -1):
            if rack[col][i] == pid:
                consecutive += 1 # calculate the number of consecutive pieces
            elif(rack[col][i] == enemypid): # if there's an enemy piece there, it's useless so return 0
                return 0
            
        if consecutive == 0: # return a point value based on the number of consecutive pieces
                return 0
        elif consecutive == 1:
            return 1
        elif consecutive == 2:
            return 10
        elif consecutive == 3:
            return 100
        elif consecutive == 4:
            return 100000
    
    def horizontalPoints(self, row, col, rack, pid):
        """
        Determines the number of horizontal points a certain space is worth given that space's location, the player, and the rack.
        Only checks down. 
        """
        
        if(pid == 1): # determine the players
            enemypid = 2
        else:
            enemypid = 1
        
        
        consecutive = 0
        
        if((col-3)<0): # If there's not enough space
            return 0 # it's worth nothing
        
        for j in range(col, (col-4),-1):
            if rack[j][row] == pid: # count the number of consecutive
                consecutive += 1
            elif(rack[j][row] == enemypid): # if you find the enemy
                return 0 # it's worth nothing
            
        if consecutive == 0: # return points based on number of consecutive pieces
            return 0
        elif consecutive == 1:
            return 1
        elif consecutive == 2:
            return 10
        elif consecutive == 3:
            return 100
        elif consecutive == 4:
            return 100000
    
    
    def diagonalPoints(self, row, col, rack, pid):
        """
        Determines the number of points a given space is worth, based on the pid and the rack. 
        Checks diagonals only to the right, but searches for both diagonals going up and those going down.
        """
        points = 0
        
        numCols = len(rack)
        numRows = len(rack[1])        
        
        if(pid == 1): # determines the players
            enemypid = 2
        else:
            enemypid = 1
        
        # check for diagonals going up
        consecutive = 0
        j = col
        
        
        for i in range(row, (row+4)):
            
            if (i >= numRows): # if it breaks the boundries, it's worth nothing
                consecutive = 0
                break
            if (j >= numCols): # the column boundry matters too
                consecutive = 0
                break
            
            elif rack[j][i] == pid: # check for consecutivity
                consecutive += 1
            elif rack[j][i] == enemypid: # if there's an enemy it's worth nothing
                consecutive = 0
                break
            j += 1 #move to the next column
            
        if consecutive == 1: # determine points based on the number of consecutive pieces
            points+= 1
        elif consecutive == 2:
            points+= 10
        elif consecutive == 3:
            points += 100
        elif consecutive == 4:
            points += 100000
        
        # check for diagonals going down
        
        j = col # let's start over 
        consecutive = 0
        
        for i in range(row, (row-4),-1):
            if (i < 0): # check for boundry break
                consecutive = 0
                break
            if (j >= numCols): # check for boundry break
                consecutive = 0
                break
            
            elif rack[j][i] == pid:
                consecutive += 1 # add up the consecutive pieces
            elif rack[j][i] == enemypid: # if there's an enemy, it's worth nothing
                consecutive = 0
                break
            j += 1 # move to the next column
        
        
        if consecutive == 1: # determine points based on consecutivity
            points+= 1
        elif consecutive == 2:
            points+= 10
        elif consecutive == 3:
            points += 100
        elif consecutive == 4:
            points += 100000
               
        return points # return those points