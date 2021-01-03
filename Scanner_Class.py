#dictionary of reserved words and special sympols
TokenType = {
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "end": "END",
    "repeat": "REPEAT",
    "until": "UNTIL",
    "read": "READ",
    "write": "WRITE",
    "+": "PLUS",
    "-": "MINUS",
    "*":"MULT",
    "/": "DIV",
    "=": "EQUAL",
    "<": "LESSTHAN",
    "(": "LEFTBRACKET",
    ")": "RIGHTBRACKET",
    ";": "SEMICOLON",
    ":=": "ASSIGN",
}


class scanner:
    def __init__(self, fileName):
        self.fileName = fileName
    
    #read the input file (program code) from txt file and return list of lines of this code
    def readTheFile(self):
        linestring =[]
        file1 = open(self.fileName, 'r') 
        Lines = file1.readlines()
        for line in Lines: 
            linestring.append(line.strip())
        return linestring

    #function to split input tokens and append tokens into a list called listOfTokens
    def getAllTokens(self, listOfString):
        listOfTokens = []
        allTokens = []
        for i in listOfString:
            listOfTokens = i.split(' ')
            if '{' in listOfTokens:       #to remove the comments from the code
                index1 = listOfTokens.index('{')
                index2 = listOfTokens.index('}')
                del listOfTokens[index1:index2+1]
            while ("" in listOfTokens):    #remove spaces from the listOfTokens
                listOfTokens.remove("")
            if listOfTokens[-1]!= ';':
                if listOfTokens[-1][-1]==';':
                    listOfTokens[-1]= listOfTokens[-1][:-1]
                    listOfTokens.append(';')
            allTokens.append(listOfTokens)
        flat_list = []                      # flatten all lists into one list
        for sublist in allTokens:
            for item in sublist:
                flat_list.append(item)
        return flat_list

    #takes listOfTokens and return list of token types in tokentypes list
    def getTokenTypes(self, tokenlist):
        tokentypes = []
        for i in tokenlist:
            if i in TokenType:
                tokentypes.append(TokenType[i])
            elif i.isnumeric():
                tokentypes.append('NUMBER')
            else:
                tokentypes.append('IDENTIFIER')
        return tokentypes

    




