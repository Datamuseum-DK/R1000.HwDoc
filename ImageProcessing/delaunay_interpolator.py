#!/usr/local/bin/python3.8
#

'''
   Delaunay triangulation based 2D->Scalar interpolator
'''

from scipy.spatial import Delaunay
from scipy.interpolate import LinearNDInterpolator
from scipy.stats import linregress

class Interpolator():
    ''' Delaunay based interpolator '''

    def __init__(self, points):
        self.points = list(points)
        self.triangles = Delaunay(
            [(in_y,in_x) for in_y,in_x,in_val in self.points]
        )
        self.interpolator = LinearNDInterpolator(
             self.triangles,
             [in_val for _in_y,_in_x,in_val in self.points],
             -9999,
        )
        self.val_0 = None
        self.val_1 = None
        self.point_0 = None
        self.point_1 = None
        self.slope = None

    def __len__(self):
        return len(self.points)

    def dump_x(self, filename, inv=False):
        ''' Dump X-coord interpolator '''
        lr = linregress(
            [x for y, x, v in self.points],
            [v for y, x, v in self.points],
        )
        print(lr)
        self.point_0 = 0
        self.val_0 = lr.intercept
        self.slope = lr.slope
        self.dump(filename, self.ref_x, inv)

    def ref_x(self, _in_y, in_x):
        ''' Calculate X-coord reference value '''
        return self.val_0 + self.slope * (in_x - self.point_0)

    def dump_y(self, filename, inv=False):
        ''' Dump Y-coord interpolator '''
        lr = linregress(
            [y for y, x, v in self.points],
            [v for y, x, v in self.points],
        )
        print(lr)
        self.point_0 = 0
        self.val_0 = lr.intercept
        self.slope = lr.slope
        self.dump(filename, self.ref_y, inv)

    def ref_y(self, in_y, _in_x):
        ''' Calculate Y-coord reference value '''
        return self.val_0 + self.slope * (in_y - self.point_0)

    def dump(self, filename, reff, inv):
        ''' Dump interpolator state to files '''

        with open(filename + ".p", "w") as file:
            for in_y, in_x, in_val in self.points:
                ref_val = reff(in_y, in_x)
                file.write("%.3f %.3f %.3f" % (in_x, in_y, in_val))
                file.write(" %.3f %.3f\n" % (ref_val, in_val - ref_val))

        with open(filename + ".t", "w") as file:
            for triangles in self.triangles.simplices:
                for corners in (0, 1, 2, 0):
                    in_y, in_x, in_val = self.points[triangles[corners]]
                    ref_val = reff(in_y, in_x)
                    file.write("%.3f %.3f %.3f\n" % (in_x, in_y, in_val - ref_val))
                file.write("\n\n")

        with open(filename + ".i", "w") as file:
            min_x_in = min(in_x for _in_y,in_x,_val in self.points)
            min_y_in = min(in_y for in_y,_in_x,_val in self.points)
            max_x_in = max(in_x for _in_y,in_x,_val in self.points)
            max_y_in = max(in_y for in_y,_in_x,_val in self.points)
            for point_x in range(230):
                x_point = min_x_in + (max_x_in - min_x_in) * point_x / 230
                for point_y in range(149):
                    y_point = min_y_in + (max_y_in - min_y_in) * point_y / 149
                    val_point = self.lookup(y_point, x_point)
                    val_ref = reff(y_point, x_point)
                    if val_point != -9999:
                        if inv[1]:
                            file.write("%.3f %.3f %.3f\n" % (x_point, y_point, -(val_point - val_ref)))
                        else:
                            file.write("%.3f %.3f %.3f\n" % (x_point, y_point, val_point - val_ref))

        with open(filename + ".g", "w") as file:
            file.write('set palette defined ( 0 "blue", 1 "white", 2 "red" )\n')
            file.write('unset border\n')
            file.write('unset xtics\n')
            file.write('unset ytics\n')
            file.write('set size ratio -1\n')
            if inv[0]:
                file.write('plot "' + filename + '.i" using 1:(-$2):3 pt 5 palette notitle,')
                file.write(' "' + filename + '.t" using 1:(-$2) with line notitle\n')
            else:
                file.write('plot "' + filename + '.i" using 1:2:3 pt 5 palette notitle,')
                file.write(' "' + filename + '.t" with line notitle\n')

    def lookup(self, coord_y, coord_x):
        ''' Lookup value for coordinates'''
        val = self.interpolator((coord_y,coord_x))
        return float(val)
