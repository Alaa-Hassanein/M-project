obs =[]

for i in range(0,self.obsNum) :
    rectang=None
    startgoalcol =True
    while startgoalcol:
        upper = self. makeRandomRect ()
        rectang=pygame.Rect(upper,(self.obsDim,self.obsDim))
        if rectang. collidepoint(self.start) or rectang.collidepoint(self.goal):
            startgoalcol=True
        else:
            startgoalcol=False
        obs.append(rectang)
    self. obstacles=obs. copy ()
    return obs|