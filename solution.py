rows ='ABCDEFGHI'
cols ='123456789'


#def cross(a,b):
#    return [s+t for s in a for t in b]

def cross(a,b):
    result = []
    for eacha in a:
        for eachb in b:
            result.append(eacha + eachb)
    return result

def square_units():
     square = []
     rowsquare = ["ABC","DEF","GHI"]
     colsquare = ["123","456","789"]
     for eachrowset in rowsquare:
         for eachcolset in colsquare:
             temp = []
             temp = cross(eachrowset,eachcolset)
             square.append(temp)
     return square


def row_lines(rows,cols):
    result = []
    for eachrow in rows:
       result.append(cross(eachrow,cols)) 
    return result

def col_lines(rows,cols):
    result =[]
    for each in cols:
        result.append(cross(rows,each))
    return result

def units(boxes,unit_list):
   result = {}
   for eachbox in boxes:  #List
       for unit in unit_list:   #List
         if eachbox in unit:  

            result.setdefault(eachbox,[]).append(unit) 
            # This is the classic where it saves the entire element as LIST as well
            # as with the existing elements
   return result

           
def peers(boxes,unit):
    result = {}
    for eachbox in boxes:
        for u in unit:
            if eachbox in u:
                result.setdefault(eachbox,[]).append(unit[eachbox])

    return result

    #print count
    #return result

boxes = cross(rows,cols)
row_units= row_lines(rows,cols)
col_units= col_lines(rows,cols)
square_units= square_units()
unit_list= row_units + col_units + square_units 
units = units(boxes,unit_list)  # this is required to get the
peers = peers(boxes,units)


assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    #---------------------------------#
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    # Choose one of the unfilled squares with the fewest possibilities
    print "NAKED_TWINS"
    
    if values:
        for eachboxes in boxes:
            tmp =[]
            for eachunits in units[eachboxes]:
                # if eachboxes in eachunits:
                #  eachunits.remove(eachboxes)
                tmp += eachunits


            print "val", values[eachboxes]

            if len(values[eachboxes]) > 1:
                n,s=min((len(values[s]),s) for s in tmp if len(values[s])!=1 and len(values[s])>1)
                for eachi in tmp:
                    sourcevalue = values[s]
                    #Check the minimum value is in other related units

                    if eachi != eachboxes and sourcevalue != values[eachi] and values[s] in values[eachi]:
                        #make sure you are not removing the minimum values in other boxes if there are any
                        #print eachboxes,"MIN INDEX",s,"VALUE OF MIN" , sourcevalue , "TARGET INDEX",eachi, "VALUE OF TARGET INDEX",values[eachi]
                        print eachboxes,s,eachi
                        # Get the index
                        # if the replaced value is already updated in units
                        # then you cannot replace the value because it is already available in units
                        tmp = values[eachi].replace(sourcevalue,"")

                        if len(tmp) ==1 and tmp in values.values():
                            print "cannot update", values[eachboxes],values[s],values[eachi]
                        else:
                            values[eachi]=values[eachi].replace(sourcevalue,"")

                        #replace minimum value in the target box if it exists
                        #print "Replaced value",values[eachi]

    return values
        
         

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys : The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    dict = {}
    count=0
    for row in rows:
       for col in cols:
            tmp=grid[count:count+1]
            if tmp in "." :
                tmp="123456789"
            tmpval = row+col
            #print "INSERTING",tmpval,tmp
            dict[tmpval]=tmp 
            count = count +1
  
    return dict


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    print "Calling display"
    tmp = values
    tabcount = 3
    rowcount = 9
    count =1
    displaystr ="    "
    for row in rows:
       for col in cols:
            rowcol = row+col
            if rowcol  in values:
               tmpkey = rowcol
               value = values[tmpkey]
               displaystr += " "+ value + " "
               if  (count) % tabcount == 0:
                   displaystr+=" | "
               if  (count) % rowcount == 0:
                   displaystr+="\n-----------------------------------\n"
            count = count+1

    return displaystr


def eliminate(values):
    if all(len(values[s]) == 1 for s in boxes): 
       return values ## Solved!
    for eachvalue in values:
         unitvalue = values[eachvalue] 
         if(len(unitvalue) ==1):
             if eachvalue in peers:
                tmp = []
                tmp = peers[eachvalue]
                #print eachvalue,tmp

                for horizontal,vertical,square in tmp:
                    #print "UNITVALUE",unitvalue
                    #print horizontal
                    #print vertical
                    #print square
                    for h in horizontal:
                        if h != eachvalue:
                            #print "INDEX",h
                            #print "VALUE",values[h]
                            if unitvalue in values[h]:
                                tmp = values[h].replace(unitvalue,"")
                                values[h]=tmp
                                #print "REPLACED VALUE",values[h]
                    for v in vertical:
                        if v != eachvalue:
                            #print "INDEX",v
                            #print "VALUE" ,values[v]
                            if unitvalue in values[v]:
                                tmp = values[v].replace(unitvalue,"")
                                values[v]=tmp
                                #print "REPLACED VALUE",values[v]
                    for s in square:
                        if s != eachvalue:
                            #print "INDEX",s
                            #print "VALUE",values[s]
                            if unitvalue in values[s]:
                                tmp = values[s].replace(unitvalue,"")
                                values[s]=tmp
                                #print "REPLACED VALUE",values[s]

    return values

# val = values[unit]
#         valofunit= list(val)
#         if(len(valofunit) > 1):
#             for eachval in valofunit:
#                 tmp =[]
#                 tmp = units[unit]

def only_choice(values):
    #pass
    if all(len(values[s]) == 1 for s in boxes): 
       return values ## Solved!
    for unit in unit_list:
        for digit in '123456789':
            tmp=[]
            for box in unit:
                if digit in values[box]:
                   tmp.append(box)
            #print "SECOND",tmp
            if(len(tmp)==1):
                values[tmp[0]]=digit
    return values

   
    
    
def reduce_puzzle(values):
    if all(len(values[s]) == 1 for s in boxes): 
       return values ## Solved!
    stalled = False
    print "calling reduce_puzzle"
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values=eliminate(values)
        # Your code here: Use the Eliminate Strategy
        values=only_choice(values)
        # Your code here: Use the Only Choice Strategy
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    print n,s
    for value in values[s]:
        values = values.copy()
        values[s] = value
        attempt = search(values)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    dict=grid_values(diag_sudoku_grid)
    #dict=search(dict)
    dict=naked_twins(dict)
    dict=search(dict)
    print display(dict)

      #print display(dict)
    # for each in units:
    #    print each
    #    tmp = []
    #    tmp = units[each]
    #    for eachi in tmp:
    #        print eachi

