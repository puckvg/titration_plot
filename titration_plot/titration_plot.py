#!/usr/bin/env python3
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.optimize import brentq
import matplotlib.pyplot as plt

KWT = {0:0.114e-14, 10:0.681e-14, 20: 0.929e-14, 25: 1.008e-14, 30: 1.469e-14, 40: 2.919e-14, 50: 5.474e-14, 60: 9.610e-14}

class KW_T(object):
    def __init__(self,werte=KWT):
        werte = sorted(werte.items())
        self.spline = InterpolatedUnivariateSpline([x for (x,y) in werte],[y for (x,y) in werte])

    def __call__(self,t):
        return float(self.spline(t))

class Solute(object):
    def __init__(self,KS,CS=1,acid=True):
        '''
        Parameters 
        ----------
        KS : list 
            The list [KS1,...,KSn] contains the K-values (not the pK-values) of the
            solute. 
        CS : float 
            CSis the concentration of the solute in mol/L.
        acid : bool 
            True or False (if the solute is a base).
            
        Returns 
        -------
        None
        '''

        self.KS = KS
        self.acid = acid
        self.n = len(self.KS) # Maximal number of H^+ resp. OH^- ions
        self.CS = CS
        self.volume = 0.0 # needed for the computation of total_volume

    def set_volume(self,volume):
        '''
        Parameters 
        ----------
        volume: float 
                volume of the titre in mL

        Returns 
        -------
        None
        '''
        self.volume = volume 
        self.solution.compute_total_volume()

    def __call__(self,ph):
        '''
        This function returns the total charge (in mol/L) of the substance.

        Parameters 
        ----------
        ph : int 
                pH of the substance

        Returns 
        -------
        charge : int 
                    charge in mol / L of the substance
        '''
            
        concentration = 10**(-ph) # pH-value -> concentration
        proportion = self.volume/self.total_volume
        if not self.acid:
            concentration = self.solution.KW/concentration
            # For bases the pK-value must be transformed first
        actual = 1.0
        for ks in self.KS:
            actual = 1 + concentration*actual/ks
        actual = self.CS * proportion / actual
        charge = self.n*actual 
        for i in range(self.n-1,0,-1):
            actual *= concentration / self.KS[i]
            charge += i*actual
        return charge 



class Solution(object):

    def __init__(self,*solutes):
        '''
        Determines the solved solutes. These are instances of Solute.

        Parameters 
        ----------
        solutes : solute objects 
                    Variable number of them

        Returns 
        -------
        None 
        '''
        self.number_solutes = len(solutes)
        self.solutes = solutes
        for solute in solutes:
            solute.solution = self
        self.Temp = 25
        self.kw = KW_T()
        self.KW = self.kw(25)

    def compute_total_volume(self):
        '''
        Calculates the total volume by summing solute volumes
        '''
        self.total_volume = sum((solute.volume for solute in self.solutes))
        for solute in self.solutes:
            solute.total_volume = self.total_volume
            # Each component must know the total volume 

    def set_Temp(self,temp):
        'calculates temperature dependent constants'

        self.Temp = temp
        self.KW = self.kw(temp)
 
    def f(self,ph):
        '''
        This function calculates the total charge of the solution dependent on pH-value ph.
        If f(ph) = 0, then ph is the pH-value of the solution.

        Parameters 
        ----------
        ph : float 
                pH of solution 
                
        Returns 
        -------
        charge : float 
                    charge of solution 
        '''

        hplus = 10**(-ph)        # pH-Value -> [H^+]
        ohminus = self.KW/hplus  # pH-Value -> [OH^-]
        charge = hplus - ohminus # charge of H^+ and OH^-
        for solute in self.solutes:
            if solute.acid:
                charge -= solute(ph)
            else:
                charge += solute(ph)
        return charge    
   
    def PH(self):
        """
        Compute a zero of function f with the Brent (1973) method for pH-values
        between -2 and 16. This zero is the unknown pH-value of the solution.
        """

        return brentq(self.f,-2,16,xtol=1e-10) # tolerance 1e-10 should be sufficient


class Acid(Solution):

    def __init__(self,KAH,CA=1,Temp=25.0):
        """
        Construct an instance of Acid class with Ka values, concentration and temperature 

        KAH: list 
                list of Ka values 
        CA: float 
            concentration
        Temp : float 
                temperature in degrees C for which Ka values are defined (default is 25)
        """
        acid = Solute(KAH,CS=CA)
        Solution.__init__(self,acid)
        self.set_Temp = Temp
        self.solutes[0].set_volume(1.0) # This value must be not zero

def PH_Acid(KAH,CA=1):
    return Acid(KAH,CA).PH()

class Base(Solution):

    def __init__(self,KBH,CB=1,Temp=25.0):
        """
        Construct an instance of Base class with Kb values, concentration and temperature 

        KBH: list 
                Kb values 
        CB: float 
            concentration 
        Temp: float 
                temperature in degrees C for which pKb values are defined (default is 25)
        """
        base = Solute(KBH,CS=CB,acid=False)
        Solution.__init__(self,base)
        self.set_Temp = Temp
        self.solutes[0].set_volume(1.0)

def PH_Base(KBH,CB=1):
    return Base(KBH,CB).PH()


class Titration(Solution):
    '''
    Calculate and plot the titration curve for a solution with arbitrary many solutes.    
    The volume of one solute varies, the others are fixed.
    '''

    def __init__(self,to_titrate,*rest_solutes):
        '''
        Determines the solved solutes. These are instances of Solute.
        The volume of to_titrate varies, the volumes of the solutes in rest_solutes
        are fixed. These volumes are parameters of plot_titration

        Parameters 
        ----------
        to_titrate : float 
                        volume of titer in ML 
        rest_solutes : float 
                        volumes of titrants in solution (variable number) in mL
                        
        Returns 
        -------
        None
        '''
        solutes = [to_titrate]+list(rest_solutes)
        self.to_titrate = to_titrate
        self.rest_solutes = rest_solutes
        # to_titrate (one solute) is variable, all other solutes are fixed
        Solution.__init__(self,*solutes)
        self.precision = 1000
        self.delta = 1.0/self.precision

    def compute_PH(self,V_titrate):
        '''
        Computes the pH-value, if V_titrate is the volume of to_titrate (variable).
        The remaining solutes are constant.

        Parameters 
        ----------
        V_titrate : float 
                    volume of titer in mL

        Returns 
        -------
        pH: float 
            pH of solution 
        '''
        self.to_titrate.set_volume(V_titrate)
        return self.PH()

    def plot_titration(self, max_to_titrate,*V_rest_solutes):
        '''
        Plot of the titration curve.
        The volume of to_titrate is variable in the range 0 ... max_to_titrate,
        *V_rest_solutes are the volumes of the remaining solutes. The volume
        of solutes must have the same order as in __init__!

        Parameters 
        ----------
        max_to_titrate : float 
                            max volume to titrate up to in mL 
        V_rest_solutes : float 
                            volume of the remaining solutes (variable number) 

        Returns 
        -------
        None 
        '''

        for i in range(len(self.rest_solutes)):  
            self.rest_solutes[i].set_volume(V_rest_solutes[i])
            # Determines the volume of the constant solutes.
        dd = max_to_titrate*self.delta
        xwerte = [dd*i for i in range(self.precision+1)]
        ywerte = [self.compute_PH(x) for x in xwerte]
        titration_line = plt.plot(xwerte,ywerte,color='r')
        plt.axhline(y=7,xmin=0,xmax=1,color='g')
        plt.axvline(x=V_rest_solutes[0]*self.rest_solutes[0].CS/self.to_titrate.CS,ymin=0,ymax=1,color='g')
        plt.axvline(x=2*V_rest_solutes[0]*self.rest_solutes[0].CS/self.to_titrate.CS,ymin=0,ymax=1,color='g')
        plt.xlabel('Volume')
        plt.ylabel('pH')
        plt.grid(True)
        plt.title('Titration Curve')
        plt.show()

if __name__ == "__main__":
    acid = Solute(KS = [5.01e-7], CS = 2, acid = True) 
    base = Solute(KS = [0.63], CS = 5, acid = False)
    titration = Titration(base, acid)
    titration.plot_titration(15, 25) 
