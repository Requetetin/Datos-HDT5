class Process:
    name = ''
    RAM_Needed = 0
    Instructions = 0
    
    def __init__(self, name, RAM_Needed, Instructions):
        self.name = name
        self.RAM_Needed = RAM_Needed
        self.Instructions = Instructions
        
    def getName(self):
        print ('Process %s' % self.name)
        
    def getRAM(self):
        return self.RAM_Needed

    def getInstructions(self):
        return self.Instructions

    def setInstructions(self, Instructions):
        self.Instructions = Instructions
