from lib.objects.ObjetMpp import ObjetMpp

class Organoid(ObjetMpp):
    def __init__(self,center,major_axis):
        ObjetMpp.__init__(self,center,major_axis)
        self.type = "Organoid"
        self.subtype = ""
        

