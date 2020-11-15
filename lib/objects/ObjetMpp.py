class ObjetMpp:
    
    def __init__(self,center,major_axis):
        self.center = center
        self.major_axis = int(round(major_axis))
        
    def create_window(self,img,distmap):
        bord_gauche = self.center.x - self.major_axis
        bord_droit = self.center.x + self.major_axis
        bord_haut = self.center.y - self.major_axis
        bord_bas = self.center.y + self.major_axis
        
        if bord_gauche < 0:
            bord_gauche = 0
        if bord_haut < 0:
            bord_haut = 0
        if bord_droit > distmap.shape[0]-1:
            bord_droit = distmap.shape[0]-1
        if bord_bas > distmap.shape[1]-1:
            bord_bas = distmap.shape[1]-1
            
        self.coordinates = [bord_gauche,bord_droit,bord_haut,bord_bas]
        self.local_distmap = distmap[self.coordinates[2]:self.coordinates[3],
                                     self.coordinates[0]:self.coordinates[1]]
        self.local_img = img.matrix_img[self.coordinates[2]:self.coordinates[3],
                                     self.coordinates[0]:self.coordinates[1]]
    
    