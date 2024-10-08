# Copyright (C) 2024  Saverio Iacoponi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
### -----------------------------------------------------------------###

import numpy as np
import cmath

class Angle:
    def __init__(self, deg=None, rad=None, complex=None) -> None:
        if complex: self.complex = complex
        elif rad:   self.radian = rad
        elif deg:   self.degree = deg
        else:       self.degree = 0

    def __str__(self):
        return f'{self.degree:.8f}'

    @property
    def degree(self):
        return self._degree

    @degree.setter
    def degree(self, value):
        self._degree = float(value%360)
        self._radian = np.deg2rad(self._degree)
        self._complex = cmath.rect(1,self._radian)

    @property
    def radian(self):
        return self._radian

    @radian.setter
    def radian(self, value):
        self._radian = float(value%(2*np.pi))
        self._degree = np.rad2deg(self._radian)
        self._complex = cmath.rect(1,self._radian)

    @property
    def complex(self):
        return self._complex

    @complex.setter
    def complex(self, value):
        r,ang = cmath.polar(value)
        if r==0: self._complex(1+0j)                    # Handle Singularity as 0
        self._complex = value/r                         # Normalized value
        self._radian = float(ang%(2*np.pi))
        self._degree = np.rad2deg(self._radian)

    @property
    def sin(self):
        return np.imag(self.complex)
    @property
    def cos(self):
        return np.real(self.complex)
    @property
    def tan(self):
        return np.tan(self.radian)
    @property
    def sinh(self):
        return np.sinh(self.sradian)
    @property
    def cosh(self):
        return np.cosh(self.sradian)
    @property
    def tanh(self):
        return np.tanh(self.sradian)

    @property
    def sdegree(self):
        return self.degree if self.degree<180 else self.degree-360
    @property
    def sradian(self):
        return self.radian if self.radian<np.pi else self.radian-2*np.pi
    
    @property
    def frac(self):
        return self.radian/(2*np.pi)

    def __add__(self,value):
        if isinstance(value,Angle):
            deg_res = value.degree + self.degree
        else:
            deg_res = value + self.degree
        return Angle(deg=deg_res)
    
    def __sub__(self,value):
        if isinstance(value,Angle):
            deg_res = value.degree - self.degree
        else:
            deg_res = value - self.degree
        return Angle(deg=deg_res)    
    
    def __neg__(self):
        return Angle(complex=np.conjugate(self.complex))

    def __eq__(self,value):
        '''Equivalency accounting for Float64 numerical error'''
        if isinstance(value,Angle):
            comparison_value = value.degree
        else:
            comparison_value = value
        diff = abs(comparison_value - self.degree)
        # If on the border between 0 and 360
        if diff > 359: diff -= 360
        return np.isclose(diff,0,rtol=1e-12)  
    
    def __ne__(self,value):
        return not self.__eq__(value)

    def _gt(self,value):
        if isinstance(value,Angle):
            return self.sdegree>value.sdegree
        else:
            value %= 360
            if value>180:value-=360
            return self.sdegree>value

    def __gt__(self,value):
        if self.__eq__(value): return False
        return self._gt(value)

    def __ge__(self,value):
        if self.__eq__(value): return True
        return self._gt(value)
    
    def _lt(self,value):
        if isinstance(value,Angle):
            return self.sdegree<value.sdegree
        else:
            value %= 360
            if value>180:value-=360
            return self.sdegree<value

    def __lt__(self,value):
        if self.__eq__(value): return False
        return self._lt(value)

    def __le__(self,value):
        if self.__eq__(value): return True
        return self._lt(value)

    def __abs__(self):
        ''' return value in the first semicircle (0-180 degrees) '''
        if np.imag(self.complex) < 0: return self.__neg__()
        else: return self

### External Functions With angles

def mean_angle(angle_list: list):
    '''
    Return the calculate mean of the angle contained in the list
        angle_list: list[Angles]

        Output: Angle
    '''
    number_of_elements  = 0
    sum_of_angles = 0+0j
    for elem in angle_list:
        # Exclude All not Angle elements
        if not isinstance(elem,Angle): continue
        number_of_elements +=1
        sum_of_angles += elem.complex
    result = sum_of_angles/number_of_elements
    return Angle(complex=result)

def angspace(start:Angle, end:Angle, steps=100):
    '''
    Return a list of floats of angles in degree
    the list is the subdivision of the angluar space between start and end, in ascending order.
    the number of subdivision is equal to steps (default 100)
    start: Angle, starting angle
    end: Angle, ending angle
    steps: Int, number of segments. steps must be >= 2

    output: list[float]
    '''
    if type(steps) != int or steps <2: raise ValueError('Parameter steps must be an integer >= 2')
    sweepsize = (end.degree-start.degree)%360
    increment = sweepsize / (steps-1)
    result = []
    for i in range(steps):
        result.append((start.degree+i*increment)%360)
    return result


def geometric_median(angle_list: list) -> Angle:
    ''' 
    Return the geometric median of a list of angles 
    The returnin angle is the angle whose collective distance from all the others is the minimal
    If more than one angle correspond to the description the mean of all eligible angles is then returned
    '''
    distances = []
    for angle in angle_list:
        distances.append(sum([(abs(angle-c)).degree for c in angle_list]))
    min_value = min(distances)
    min_idx = [index for index, value in enumerate(distances) if value == min_value]
    angle_list = [ angle_list[ index ] for index in min_idx ]
    return mean_angle(angle_list)

    

if __name__ == "__main__":
    a = Angle(deg=-20)
    b = Angle(deg=70)
    d = Angle(deg=99)
    c = mean_angle([a,b])

    print(geometric_median([a,a,d,b,a]))




