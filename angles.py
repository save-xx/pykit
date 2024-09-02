import numpy as np
import cmath

class Angle:
    def __init__(self, deg=None, rad=None, complex=None) -> None:
        if complex: self.complex = complex
        elif rad:   self.radian = rad
        elif deg:   self.degree = deg
        else:       self.degree = 0

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
        return self.radian if self.degree<np.pi else self.radian-2*np.pi

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
        '''Equivalency accounting for Float error'''
        if isinstance(value,Angle):
            comparison_value = value.degree
        else:
            comparison_value = value
        diff = abs(comparison_value - self.degree)
        # If on the border between 0 and 360
        if diff > 359: diff -= 360
        return np.isclose(diff,0,rtol=1e-12)  

    # def __gt__(self,value):
    #     if self.__eq__(value): return False


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



if __name__ == "__main__":
    a = Angle(deg=-20)
    b = Angle(deg=70)
    c = mean_angle([a,b])
    print(c.degree)
    print(angspace(a,c,101))
    print(len(angspace(a,c,101)))




