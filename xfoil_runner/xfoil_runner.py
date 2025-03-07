"""Runs an XFOIL analysis for a given airfoil and flow conditions"""
import os
import subprocess
import numpy as np
from matplotlib import pyplot as plt 


def run_xfoil(airfoil_name, alpha_i, alpha_f, alpha_step, Re, mach):
    # %% Inputs
    #airfoil_name = "NACA0012"
    #alpha_i = 0
    #alpha_f = 10
    #alpha_step = 0.25
    #Re = 1000000
    n_iter = 100

    # %% XFOIL input file writer 

    if os.path.exists("polar_file.txt"):
        os.remove("polar_file.txt")

    input_file = open("input_file.in", 'w')
    input_file.write("LOAD {0}.dat\n".format(airfoil_name))
    input_file.write(airfoil_name + '\n')
    input_file.write("PANE\n")
    input_file.write("OPER\n")
    input_file.write("Visc {0}\n".format(Re))
    input_file.write("PACC\n")
    input_file.write("polar_file.txt\n\n")
    input_file.write("ITER {0}\n".format(n_iter))
    input_file.write("ASeq {0} {1} {2}\n".format(alpha_i, alpha_f, alpha_step))
    input_file.write("\n\n")
    input_file.write("quit\n")
    input_file.close()

    subprocess.call("xfoil.exe < input_file.in", shell=True)
    polar_data = np.loadtxt("polar_file.txt", skiprows=12)
    return polar_data


if __name__ == "__main__":
    airfoil_name = "NACA0012"
    alpha_i = -20
    alpha_f = 20
    alpha_step = 0.5
    Re = 1000000
    mach = 0.179
    polar_data = run_xfoil(airfoil_name, alpha_i, alpha_f, alpha_step, Re, mach)

    #alpha    CL        CD       CDp       CM     Top_Xtr  Bot_Xtr
    # 0       1         2        3         4       5       6
    alpha = cl=polar_data[:,0]
    cl = polar_data[:,1]
    cd = polar_data[:,2]
    cdp = polar_data[:,3]
    cm = polar_data[:,4]
    plt.figure()
    plt.title("Aero foil {0}".format(airfoil_name)) 
    plt.subplot(2, 2, 1)
    plt.plot(alpha, cl, label="CL")
    plt.xlabel("alpha") 
    plt.ylabel("Cl") 
    plt.legend(loc="upper left")
    plt.grid(True)

    plt.subplot(2, 2, 2) 
    plt.plot(alpha, cd, label="Cd")
    plt.xlabel("alpha") 
    plt.ylabel("Cd") 
    plt.legend(loc="upper left")
    plt.grid(True)

    plt.subplot(2, 2, 3) 
    plt.plot(cd, cl, label="Cl vs Cd")
    plt.xlabel("cd") 
    plt.ylabel("cl") 
    plt.legend(loc="upper left")
    plt.grid(True)

    plt.subplot(2, 2, 4) 
    plt.plot(alpha, cm, label="Cm")
    plt.xlabel("alpha") 
    plt.ylabel("Cm") 
    plt.legend(loc="upper left")
    plt.grid(True)

    plt.show()
    print("OK")
