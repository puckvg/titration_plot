#!/usr/bin/env python3 

import numpy as np 
import matplotlib.pyplot as plt 
import random
from titration_plot.titration_plot import Solute, Titration

def make_plot():
    acid = Solute([7.1e-3, 6.3e-8, 4.5e-13], CS = 1e-3, acid = True)
    base = Solute([0.63], CS = 1e-2, acid = False)
    titration = Titration(base, acid)
    titration.plot_titration(6, 25)

if __name__ == "__main__":
    points = 0
    # virtual titration 
    print("""
            Welcome to the virtual titration machine. Today we are going to explore the titration of the acid H3PO4 with the base NaOH (an acid-base titration). 
            Here H3PO4 is the titrant and NaOH is the titre. In other words, we have a fixed volume and concentration of H3PO4 and we are adding NaOH dropwise to determine the concentration required to neutralise H3PO4. 
            Since H3PO4 is triprotic, we are effectively carrying out three subsequent acid-base titrations. In reality, we only see two, as the pKas in order of protonation are 2.15, 7.20, and 12.35. 
            A pKa of 12.35 is a very poor acid. Hence, in practice, we will observe two titration end-points. We require two different indicators for the two different end-points. 
            First we will use methyl orange. Then we will use thymolphthalein. Please take the time to look up the pH region in which these indicators change colour, to give an indication of what we will expect in our titration curve. 
            Once we have understood what's going on, let's start the experiment! 
            """)
    
    print("""
          The experiment is set up. We have 25 mL of H3PO4 with a concentration of 1e-3 mol / L in a conical flask with a burette containing 1e-2 mol / L NaOH. 
          The flask also contains a few drops of the two indicators, methyl orange and thymolpthalein.
          Please calculate the number of moles of NaOH required to neutralise the first proton in H3PO4. Then, convert this to a volume of NaOH. Once you are sure of 
          your answer, please type the volume of NaOH in mL (take a note of this as you will need to enter it for points later):
          """)


    print("""
          What about the volume of NaOH required to neutralise the second deprotonation? (Make sure you give your answer as the total volume of NaOH added, as this is 
          what you will read on your burette). This question is not assessed but is useful for you to understand the titration:
          """)

    vol_naoh = input()
    print("""
        Ok, now that we know approximately where our end-points will be, we can start adding NaOH to H3PO4. You have the option to add drop-wise (at a rate of approximately 0.05 mL / drop,
        but in reality we get somewhere between 0.04 - 0.06 mL per drop), or allow for a bigger burst of liquid to flow from the titration (at a rate of approximately 0.5 mL per drop, 
        but in reality with a range of 0.4 - 0.8 mL per "flow"). Please enter "flow" or "drop" to choose the rate at which your liquid flows from the burette. I will keep asking until a colour 
        change is observed. Be careful, because if you choose to add too much liquid, you might over-shoot the colour change and record a volume that is too large!
        """)

    volume = 0
    while volume < 2.5:
        flow_rate = input()
        if flow_rate == "flow":
            volume += random.uniform(0.4, 0.8)
        elif flow_rate == "drop":
            volume += random.uniform(0.04, 0.06)
        else:
            print("Please enter 'flow' or 'drop' to continue the titration process")

    print("A colour change has been observed from red to yellow at "+"{:.2f}".format(volume)+" mL! Please take a note of this volume."
            "This is the first end-point of your titration and has been stored in the machine. Now we can proceed to the next "
            "deprotonation step with the second indicator. As before, please carry out the titration using the 'flow' or 'drop' options:")
    while volume < 5:
        flow_rate = input()
        if flow_rate == "flow":
            volume += random.uniform(0.4, 0.8)
        elif flow_rate == "drop":
            volume += random.uniform(0.04, 0.06)
        else:
            print("Please enter 'flow' or 'drop' to continue the titration process")

    print("A colour change has been observed from yellow to blue at "+"{:.2f}".format(volume)+" mL! This is the end of the titration. You achieved ",points," out of a total of 3 points. Let's see what happened in a plot...")
    make_plot()
