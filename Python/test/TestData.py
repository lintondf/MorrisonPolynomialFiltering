'''
Created on Feb 1, 2019

@author: NOOK
'''
import csv
import pymap3d
import xml.etree.ElementTree as ET 

if __name__ == '__main__':
    xmlfile = "/Users/NOOK/Google Drive/BlueStick/data/X-37 RWY 12 short.jTraj"
    filename = 'landing.csv'
    # create element tree object 
    tree = ET.parse(xmlfile) 
    root = tree.getroot() 
    
    with open(filename, 'w', newline='') as csvfile: 
        fields = ['time','east','north', 'up', 'azimuth', 'elevation', 'range']
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
        writer.writeheader() 
        sensor = [0.607302876756862, -2.1026663520973794, 100]
        samples = []
        for tspiRow in root :
            t = float(tspiRow.attrib['time'])
            E = float(tspiRow.attrib['E'])
            F = float(tspiRow.attrib['F'])
            G = float(tspiRow.attrib['G'])
            x, y, z = pymap3d.ecef2enu(E, F, G, sensor[0], sensor[1], sensor[2], deg=False)
            z = 0.456*z
            E, F, G = pymap3d.enu2ecef(x, y, z, sensor[0], sensor[1], sensor[2], deg=False)
            a, e, r = pymap3d.ecef2aer(E, F, G, sensor[0], sensor[1], sensor[2], deg=False)
            print(t-1500,x,y,z,a,e,r)
            row = {}
            row[fields[0]] = 2.72*(t-1500)
            row[fields[1]] = x
            row[fields[2]] = y
            row[fields[3]] = z
            row[fields[4]] = a
            row[fields[5]] = e
            row[fields[6]] = r
            samples.append(row)
        writer.writerows(samples)