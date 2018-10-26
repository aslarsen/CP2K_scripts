import sys
import numpy as np
import math

class XYZtoPDB:
    def __init__(self, xyzfile, cellfile):
        self._cellfile = cellfile
        self._xyzfile = xyzfile
        self._A = None
        self._B = None
        self._C = None

    def vector_angle(self, a, b, c):
    
        # In case numpy.dot() returns larger than 1
        # and we cannot take acos() to that number
        acos_out_of_bound = 1.0
        v1 = a - b
        v2 = c - b
        v1 = v1 / math.sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2)
        v2 = v2 / math.sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)
        dot_product = np.dot(v1,v2)
    
        if dot_product > acos_out_of_bound:
            dot_product = acos_out_of_bound
        if dot_product < -1.0 * acos_out_of_bound:
            dot_product = -1.0 * acos_out_of_bound
    
        return np.arccos(dot_product)


    def read_xyzfile(self, xyzfile):
        models = []
        f = open(xyzfile, 'r')
        model = []
        for line in f:
            if len(line.split()) == 1:
                if len(model) != 0:
                    models.append(model)
                    model = []
                    model.append(line.replace('\n',''))
                else:
                    model.append(line.replace('\n',''))
            else:
                model.append(line.replace('\n',''))
        models.append(model)
        f.close()
        return models

    def read_cellfile(self, cellfile):
        f = open(cellfile, 'r')
        cells = []
        for line in f:
            if '#' not in line:
               cells.append(line.replace('\n',''))
        return cells 
    
    def read_vectors(self, cell):
        cell = cell.split()
        A = np.array([float(cell[2]), float(cell[3]), float(cell[4] ) ])
        B = np.array([float(cell[5]), float(cell[6]), float(cell[7] ) ])
        C = np.array([float(cell[8]), float(cell[9]), float(cell[10]) ])
        return A,B,C

    def write_pdb(self, list_of_structures, name):

        # write pdb file     
        modelnumber = 0
        OUT = ''

        for model in list_of_structures:
                cell   = model[0]
                struct = model[1]
    
                atomnumber = 1
                modelnumber += 1

                #CRYST = 'CRYST1 %.3f %.3f %.3f %.3f %.3f %.3f \n' % (cell[0], cell[1], cell[2], cell[3], cell[4], cell[5])

                CRYST = 'CRYST1%9.2f%9.2f%9.2f%7.2f%7.2f%7.2f  P 1\n' % (cell[0], cell[1], cell[2], cell[3], cell[4], cell[5])

                OUT += CRYST 

                OUT += 'MODEL'
                for i in range(0,9-len(str(modelnumber))):
                        OUT += ' '
                OUT += str(modelnumber)+'\n'
    
                #print len(struct)
                for atom in struct:
                        #print atom
                        #atom = atom.split()
                        ATOM = 'ATOM'

                        ATOMNUMBER = str(atomnumber)
                        for i in range(0,7-len(ATOMNUMBER)):
                                ATOMNUMBER = ' ' + ATOMNUMBER

                        ATOMTYPE = '  '+atom[0]
                        for i in range(0,(4-len(atom[0]))):
                                ATOMTYPE += ' '

                        RESIDUE = 'XXX A   1    '

                        X = ("%.3f" % float(atom[1][0]))
                        for i in range(0,(8-len(X))):
                                X = ' ' + X

                        Y = ("%.3f" % float(atom[1][1]))
                        for i in range(0,(8-len(Y))):
                                Y = ' ' + Y

                        Z = ("%.3f" % float(atom[1][2]))
                        for i in range(0,(8-len(Z))):
                                Z = ' ' + Z

                        ENDATOM = '  1.00 0.00            '+atom[0]


                        #ENDATOM = '                       '+atom[0]

                        LINE = ATOM + ATOMNUMBER + ATOMTYPE + RESIDUE + X + Y + Z + ENDATOM + '\n'
       
                        OUT += LINE

                        atomnumber += 1

                OUT += 'ENDMDL\n'
        f = open(name,'w')
        f.write(OUT)
        f.close()
 
    def get_atoms(self, model):
        ATOMS = []
        N = 0
        for line in model:
            N += 1
            if N > 2:
                line = line.split()
                ATOM = [ line[0], np.array([float(line[1]), float(line[2]), float(line[3])]) ]
                ATOMS.append(ATOM)
        return ATOMS   


    def write_xyz(self, atoms, tag, filename):
        number_of_atoms = len(atoms)
        f = open(filename, 'w')
        f.write(str(number_of_atoms) + '\n')
        f.write(tag + '\n')
        for atom in atoms: 
            LINE = atom[0] + '   ' + str(atom[1][0]) + '   ' + str(atom[1][1]) + '   ' + str(atom[1][2]) + '\n'
            f.write(LINE)
        f.close() 

    def run(self):
        # read
        xyz_models = self.read_xyzfile(self._xyzfile)
        cells = self.read_cellfile(self._cellfile)

        models = []
        for xyz, cell in zip(xyz_models, cells):
            A, B, C = self.read_vectors(cell)
            ATOMS = self.get_atoms(xyz)
            origin = np.array([0,0,0])
            alpha = np.rad2deg(self.vector_angle(B,origin,C))
            beta  = np.rad2deg(self.vector_angle(C,origin,A))
            gamma = np.rad2deg(self.vector_angle(B,origin,A))
            A_length = np.linalg.norm(A)
            B_length = np.linalg.norm(B)
            C_length = np.linalg.norm(C)
            model = [[A_length, B_length, C_length, alpha, beta, gamma],ATOMS]
            models.append(model)

        #print "%0.2f %0.2f %0.2f %0.3f %0.3f %0.3f" % (A_length, B_length, C_length, alpha, beta, gamma)


        # write pdb
        self.write_pdb(models, 'temp.pdb')



xyzfile = sys.argv[1]
cellfile = sys.argv[2]

XYZ = XYZtoPDB(xyzfile, cellfile)
XYZ.run()
