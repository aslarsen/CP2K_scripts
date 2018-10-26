import sys

def read_xyzfile(xyzfile):
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
    models.append(model)
    f.close()
    return models


input_file    = sys.argv[1]
xyz_file      = sys.argv[2]
index = -1 # -1 equal to last frame


xyz_data = read_xyzfile(xyz_file)[index]
del xyz_data[0]
del xyz_data[0]

input_data = []
f = open(input_file, 'r')
for line in f:
    input_data.append(line)
f.close()

output_data = []
found_start = False
found_end = False
skip = False
for line in input_data:
    if '&COORD' in line:
        skip = True
        found_start = True
        output_data.append(line)
    if skip == False:
        output_data.append(line)
    if '&END COORD' in line:
        skip = False
        found_end = True
        for coord in xyz_data:
            coord = coord.split()
            XYZ = '      ' + coord[0] + '  ' + coord[1] + '  ' + coord[2] + '  ' + coord[3] + '\n'
            output_data.append(XYZ)
        output_data.append(line)

if found_start == True and found_end == True:
    f = open(input_file, 'w')
    for line in output_data:
        f.write(line)
    f.close()
else:
    print 'FATAL ERROR: ABORT NO &COORD OR &END COORD FOUND!!!!'
