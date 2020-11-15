class GroupObj:
    
    def __init__(self):
    
        self.tailles = []
        self.contours = []
        self.max_intensities = []
        self.max_indices = []
        self.mean_intensities = []
        self.rapps_max_creux = []
        self.means_creux = []
        self.thresholds = []


class GroupObjImage(GroupObj):
    def __init__(self):
        GroupObj.__init__(self)
        self.number = 0
        
class GroupObjFile(GroupObj):
    def __init__(self):
        GroupObj.__init__(self)
        self.number = []
        
    def add_GroupObjImage(self, group_obj_img):
        for key,value in group_obj_img.__dict__.items():
            if key == "number":
                setattr(self,key,getattr(self,key)+[value])
            else:
                setattr(self,key,getattr(self,key)+value)