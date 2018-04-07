import sys
import math
import random as rn

##############################################################

class Point:
    point_count=0
    x=0
    y=0
    z=0
    def __init__(self,X,Y,Z):
        self.x=X
        self.y=Y
        self.z=Z
        Point.point_count += 1
    def displayCount(self):
        print ("Total Point Created %d" % Point.point_count)
    def dispaly(self):
        print ('x: {0}, y: {1}, z: {2}'.format(self.x,self.y,self.z))
    def toString(self):
    	loc='x: {0} y: {1} z: {2}'.format(self.x,self.y,self.z)
    	return loc
    def distance(self,p):
        d=math.sqrt(math.pow(self.x-p.x,2)+math.pow(self.y-p.y,2)+math.pow(self.z-p.z,2))
        return d

##############################################################
class Cell:
	'Class cell'
	cell_count=0
	cellId=0
	vertices=[]
	nodes = []
	def __init__(self,cellId,v,nodes=[]):
		self.cellId=cellId
		self.vertices=v
		self.nodes=nodes
		Cell.cell_count += 1
	def printInfo(self):
		print('Cell Id: {0}'.format(self.cellId))
		print('Nodes inside this cell {0}'.format(self.nodes))
		for v in self.vertices:
			v.dispaly()
		return 1
	def toString(self):
		info='Cell Id: {0} , Nodes list: {1} , Vertices :'.format(self.cellId,self.nodes)
		for v in self.vertices:
			info=info + v.toString() + ' , '
		return info+'\n'

##############################################################

class Sensor:
	'Class to define sensor node'
	nodeId=-1
	sensor_count=0
	location=Point(0,0,0)
	Ec=0
	Cr=0
	Sr=0
	netForce=0
	nodeType=0 # 0 mean normal node, 1 is centriod , 2 is cluster head
	cellId=-1
	status=0	# 0 mean sleeping, 1 mean active
	
	def __init__(self,nodeId,location,Ec,Cr,Sr,netForce=0,nodeType=0,cellId=-1,status=0):
		self.nodeId=nodeId
		self.location=location
		self.Ec=Ec
		self.Cr=Cr
		self.Sr=Sr
		self.netForce=netForce
		self.nodeType=nodeType
		self.cellId=cellId
		self.status=status
		Sensor.sensor_count += 1

	def getLocation(self):
		return self.location

	def printInfo(self):
		#print ("Sensor Id: %d Position: (%d,%d,%d) Remaining Charge: %d Communication Range %d Sensing Range %d", %(self.nodeId,self.x,self.y,self.z))
		print ('Sensor Id: {0} \n Position: {1} \n Remaining Charge: {2} \n Communication Range: {3} \n Sensing Range: {4} \n Node Type: {5} \n Cell Id: {6}' \
			.format(self.nodeId,self.location.toString(),self.Ec,self.Cr,self.Sr,self.nodeType,self.cellId))

##############################################################


def distance(S1,S2):
    d=math.sqrt(math.pow(S1.x-S2.x,2)+math.pow(S1.y-S2.y,2)+math.pow(S1.z-S2.z))
    return d

def createSensors(N,Ec,Cr,Sr):
	contaier=[]
	for i in range(0,N):
		new_location=Point(rn.randrange(0,space_x,1),rn.randrange(0,space_y,1),rn.randrange(0,space_z,1))
		new_sensor=Sensor(i,new_location,Ec,Cr,Sr,0,0,-1,0)
		contaier.append(new_sensor)
	return contaier

def selectCentriod(contaier,space_x,space_y,space_z):
	distances=[]
	center=Point(space_x/2,space_y/2,space_z/2)
	for sensor in contaier:
		p=sensor.getLocation()
		d=center.distance(p)
		distances.append(d)
	minmumDistance=min(distances)
	i=distances.index(minmumDistance)
	contaier[i].nodeType=1
	return 1

def createCells(space_dimension,cRange):
	r=0
	cells=[]
	A=math.floor(cRange/math.sqrt(5))
	print ('Optimum Value for cell dimension should be less than : {}'.format(A))
	for i in reversed(range(1,A+1)):
		#print('Value of i:{}'.format(i))
		if space_dimension%i==0:
			r=i
			break
			#print('Vlaue of r:{}'.format(r))
	print ('Cell Dimension : {}'.format(i))
	#nCells=math.pow(pace_dimension/r,3)
	L=list(range(0,space_dimension,r))
	cellId=0
	for z in L:
		for y in L:
			for x in L:
				vertices=[Point(x,y,z),Point(x+r,y,z),Point(x,y+r,z),Point(x+r,y+r,z),Point(x,y,z+r),Point(x+r,y,z+r),Point(x,y+r,z+r),Point(x+r,y+r,z+r)]
				new_cell=Cell(cellId,vertices,[])
				cells.append(new_cell)
				cellId+=1
	return cells

def assignCellToSensors(cellContainer,sensorsContainer):
	for s in sensorsContainer:
		#print('debug 1')
		if s.cellId < 0:
			loc=s.location
			for c in cellContainer:
				if checkSensorLocationInCell(loc,c) == 1:
					#print("Point {0} is inside this cell{1}".format(loc.toString(),c.cellId))
					#print('appending node {} to cell {} '.format(s.nodeId,c.cellId))
					c.nodes.append(s.nodeId)
					#print('Node appended to this cell{}'.format(c.nodes))
					s.cellId=c.cellId
					#print("Node {0} is added to cell{1}".format(s.nodeId,c.cellId))
					break
	return 1

def checkSensorLocationInCell(location,cell):
	vertices=cell.vertices
	X=[]
	Y=[]
	Z=[]
	for v in vertices:
		X.append(v.x)
		Y.append(v.y)
		Z.append(v.z)
	# print(X)
	# print(Y)
	# print(Z)
	# print('#####################')
	max_x=max(X)
	max_y=max(Y)
	max_z=max(Z)
	min_x=min(X)
	min_y=min(Y)
	min_z=min(Z)

	if min_x <= location.x <= max_x:
		if min_y <= location.y <= max_y:
			if min_z <= location.z <= max_z:
				return 1
	return 0

##############################################################

sensorsContainer=[]
cellContainer=[]
initialElectricCharge=50 # initial value for electric charge
cRange=20	# Communication range 
sRange=6	# Sensing range 
nSensors=1000 # Number of sesors
space_dimension=space_x=space_y=space_z=100 # space dimension

sensorsContainer=createSensors(nSensors,initialElectricCharge,cRange,sRange)
#for s in sensorsContainer:
#	s.printInfo()
centriod_index=selectCentriod(sensorsContainer,space_x,space_y,space_z)
# sensorsContainer[centriod_index].nodeType=1

cellContainer=createCells(space_dimension,cRange)
print ('Total Number of Cell Created {}'.format(Cell.cell_count))
assignCellToSensors(cellContainer,sensorsContainer)
print('Space Dimenssion : {} * {} * {}'.format(space_x,space_y,space_z))
print('Total Number of Cells: {}'.format(len(cellContainer)))
for s in sensorsContainer:
	s.printInfo()
#f = open("cell.txt", "w")
with open("cell.txt", "w") as f:
	for c in cellContainer:
		f.write(c.toString())
#f.close()
# for c in range(0,100):
# 	print(checkSensorLocationInCell(Point(2,1,1),cellContainer[c]))







