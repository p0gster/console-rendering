import numpy as np
import time
import os


def render(lightdict,lightarray,shape):
   """
    Parameters
    ----------
    lightdict : dictionary between integers and console string outputs
    lightarray : array of integers
    shape : 2 tuple of lightarray shape

    Returns
    -------
    render to console

    """
   os.system("clear")
   string=""
   for y in range(shape[1]):
        
        for x in range(shape[0]):
            string+=lightdict[int(lightarray[x,y])]
            #string+="#"
        string+="\n"
   print(string)
 
   time.sleep(0.05)

def rawdonutcoordinate(angle1, angle2, radius1, radius2):
    """
    Gets an unrotated donut coordinate. all inputs are float

    """
    
    xunit=np.array([1,0,0])
    yunit=np.array([0,1,0])
    zunit=np.array([0,0,1])
    
    inner_vector=radius1*( np.cos(angle1)*xunit + np.sin(angle1)*zunit )
    inner_vectorunit=inner_vector/np.linalg.norm(inner_vector)
    
    outer_vector=radius2*(np.cos(angle2)*inner_vectorunit+np.sin(angle2)*(-yunit))
    outer_vectorunit=outer_vector/np.linalg.norm(outer_vector)
    return inner_vector+outer_vector, outer_vectorunit

def translate(coordinate,translation):
    """
    translates

    """
    return coordinate+translation


def rotate(coordinate,angle1,angle2,angle3):
    """
    

    Parameters
    ----------
    coordinate : . 
    angle1 : xnormal counterclockwise rotation
    angle2 : ynormal counterclockwise rotation
    angle3 : znormal counterclockwise rotation

    Returns
    -------
    rotated coordinate

    """
    
    #transpose coordinate
     
    transcoord=np.atleast_2d(coordinate).T
    
    #rotate coordinate
    transcoord=np.matmul(Rx(angle1),transcoord)
    transcoord=np.matmul(Ry(angle2),transcoord)
    transcoord=np.matmul(Rz(angle3),transcoord)
    
    #transpose coord to row coordinate
    coordinate=transcoord.T
    
    #numpy doesn't like me
    return np.array([coordinate[0,0],coordinate[0,1],coordinate[0,2]])



    
def project2d(zwall,coordinate):
    """
    Projects point onto wall in front of observer
    Observer is treated as always being at origin

    Parameters
    ----------
    zwall : distance of wall from origin
    coordinate : coordinate of point (numpy array)

    Returns
    -------
    2d numpy array of coord on wall

    """
    if coordinate[2]>0:
        scalefactor=zwall/coordinate[2]
        
        coordonwall=coordinate*scalefactor
        
        twoDwallcoord=np.array([coordonwall[0],coordonwall[1]])
        
        return twoDwallcoord
    else:
        return False
    
def twodtoscreen(screenshape,coordinate):
    """
    

    Parameters
    ----------
    screenshape : nparrray 
    coordinate : nparray

    Returns
    -------
    intpos : integer coordinate on screen

    """
    centrescreen=0.5*(screenshape-1)
    
    #scaling in x direction to match screen
    coordinate*=np.array([2,1])
    
    fractpos=centrescreen+coordinate
    
    intpos=fractpos.astype(int)
    
    x=intpos[0]
    y=intpos[1]
    
    coordx=screenshape[0]
    coordy=screenshape[1]
    
    
    if (x<=(coordx-1) and x>=0) and (y<=(coordy-1) and y>=0):
        return intpos
    else:
        return False
    

    
    
def Rx(theta):
  return np.matrix([[ 1, 0           , 0           ],
                   [ 0, np.cos(theta),-np.sin(theta)],
                   [ 0, np.sin(theta), np.cos(theta)]])
  
def Ry(theta):
  return np.matrix([[ np.cos(theta), 0, np.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-np.sin(theta), 0, np.cos(theta)]])
  
def Rz(theta):
  return np.matrix([[ np.cos(theta), -np.sin(theta), 0 ],
                   [ np.sin(theta), np.cos(theta) , 0 ],
                   [ 0           , 0            , 1 ]])

def donutcoordinate(donangle1, donangle2, radius1, radius2, centre, angle1,angle2,angle3):
    """
    True donut coordinate

    """
    
    donutcoord,normal=rawdonutcoordinate(donangle1, donangle2, radius1, radius2)
    
    #rotate donut
    rot=rotate(donutcoord,angle1,angle2,angle3)
    rotnorm=rotate(normal,angle1,angle2,angle3)
    
    #translate donut
    transrot=translate(rot,centre)
    

    return transrot, rotnorm


def projecttoscreen(zwall,coordinate,screenshape):
    """
    
    projects coordinate to screen 
    
    """
    twodvec=project2d(zwall,coordinate)
    if type(twodvec)==bool:
        return False
    

    screencoord=twodtoscreen(screenshape,twodvec)
    if type(screencoord)==bool:
        return False
    
    return screencoord



def lightarray(screenshape,changeangle, radius1, radius2, centre, angle1,angle2,angle3,zwall,lightsize):
    #initialise arrays
    lightarr=np.zeros(screenshape)
    distances=np.zeros(screenshape)
    distances.fill(np.inf)
    
    #plan
    
    #iterate through all angles
    
        #for an angle
        #calculate donut pos
        #calculate screen position of donut 
        #if false
            #skip angle
        #else
            #calculate donut distance
            #if donutdistance less than distance in distances
                #calculate dotproduct
                #convert to lighting according to light dict
                #update light array
            #else
                #skip angle
                
    
    #iterate through all angles
    for donangle1 in np.arange(0,2*np.pi,changeangle):
        for donangle2 in np.arange(0,2*np.pi,changeangle):
            
            #for an angle
            #calculate donut pos
            donutcoord,normal=donutcoordinate(donangle1, donangle2, radius1, radius2, centre, angle1,angle2,angle3)
            
            #calculate screen position of donut 
            screencoord=projecttoscreen(zwall,donutcoord,screenshape)
            
            #if false
            if type(screencoord)==bool:
                
                #skip angle
                pass
            
            #else
            else:
                
                
                #calculate donut distance
                donutdistance=np.linalg.norm(donutcoord)
                
                #if donutdistance less than distance in distances
                if donutdistance<distances[screencoord[0],screencoord[1]]:
                    
                    #update distances
                    distances[screencoord[0],screencoord[1]]=donutdistance
                
                    
                    #calculate dotproduct
                    unitdonutcoord=donutcoord/np.linalg.norm(donutcoord)
                    dotprod=np.dot(unitdonutcoord,normal)
                    
                    if dotprod<0:
                   
                                  
                        #convert to lighting according to light dict
                        lighting=-(lightsize-1)*dotprod
                        lighting=int(round(lighting,0))
                        
                        #update light array
                        lightarr[screencoord[0],screencoord[1]]=lighting
                        
                    else:
                        pass
                    
                #else
                else:
                    
                    #skip angle
                    pass    
    return lightarr
    
#initialise

lightarr=np.zeros((225,63)).astype(int)
lightdict={0:" ",1:".",2:",",3:"-",4:"~",5:":",6:";",7:"=",8:"!",9:"*",10:"#",11:"$",12:"@"}

#trial lightdict
#lightdict={0:" ",1:",",2:"-",3:"/",4:"{",5:"[",6:"^",7:"?",8:"%",9:"$",10:"£",11:"@"}

screenshape=np.array(lightarr.shape)

tau=2*np.pi

changeangle=0.030 
radius1=3
radius2=1

centre=np.array([-0,0,40])

zwall=260
lightsize=len(lightdict)

changerotangle=tau/50

angle1,angle2, angle3=tau/4,0,0
lightarrays=[]


frameneed=int(round(tau/changerotangle,0))
for _ in range(frameneed):
    
    start=time.time()
    
    framedone=_+1
    
    angle1+=changerotangle
    angle2+=changerotangle*1
    angle3+=changerotangle*0
    lightarr=lightarray(screenshape,changeangle, radius1, radius2, centre, angle1,angle2,angle3,zwall,lightsize)
    lightarrays+=[lightarr]
    
    end=time.time()
    print("frames done: "+str(framedone)+"/"+str(frameneed))
    print(str(end-start)+" seconds elapsed")
    print("Approx "+str((frameneed-framedone)*(end-start))+" seconds remaing")
    print("")



while True:
    for _ in range(len(lightarrays)):
        start=time.time()
        render(lightdict,lightarrays[_],screenshape)

        

    

















    
    
    
    

