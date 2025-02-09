import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches, rcParams
from scipy import signal

def splane(b,a,filename=None):
    gig=plt.figure()
    ax=plt.subplot(111)

    #정규화
    if np.max(b)>1:
        kn=np.max(b)
        b=b/float(kn)
    else:
        kn=1

    if np.max(a)>1:
        kd=np.max(a)
        a=a/float(kd)
    else:
        kd=1
    
    p=np.roots(a)
    z=np.roots(b)
    k=kn/float(kd)

    # Plot the zeros and set their properties
    t1 = plt.plot(z.real, z.imag, 'go', ms=10)  # Zeros are plotted as green circles
    # Plot the poles and set their properties
    t2 = plt.plot(p.real, p.imag, 'gx', ms=10)  # Poles are plotted as green crosses
    plt.setp(t1, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', markerfacecolor='b')  # Zero marker style
    plt.setp(t2, markersize=10.0, markeredgewidth=3.0, markeredgecolor='r', markerfacecolor='r')  # Pole marker style

    # Move the axes to the center
    ax.spines['left'].set_position('center')  # Move the y-axis to the center
    ax.spines['bottom'].set_position('center')  # Move the x-axis to the center
    ax.spines['right'].set_visible(False)  # Hide the right spine
    ax.spines['top'].set_visible(False)  # Hide the top spine

    # Set the ticks for the plot
    r = 1.5  # Axis scaling factor
    plt.axis('scaled')  # Set equal scaling for both axes
    plt.axis([-r, r, -r, r])  # Set the axis limits
    ticks = [-1, -0.5, 0, 0.5, 1]  # Define tick positions
    plt.xticks(ticks)  # Set x-axis ticks
    plt.yticks(ticks)  # Set y-axis ticks

    # Display or save the plot
    if filename is None:
        plt.show()  # Display the plot
    else:
        plt.savefig(filename)  # Save the plot to the specified file

    # Return the zeros, poles, and gain
    return z, p, k

np.set_printoptions(precision=3, suppress=True)

wp=0.2*np.pi
ws=0.3*np.pi
Rp=1 #pass band ripple
As=16 #stop band ripple dB

N, wc=signal.cheb1ord(wp, ws, Rp, As, analog=True)
print(f'Filter Order N={N}')
print(f'Cutoff Frequency wc={wc:.3f}={wc/np.pi:.3f}pi')

b,a=signal.cheby1(N,Rp,wc, "lowpass", analog=True)
print(f"Numerator coefficient od system function Ha(s)={b}")
print(f"Denominator coefficient of system function Ha(s)={a}")

z,p,k=signal.cheby1(N, Rp, wc, "lowpass", analog=True, output="zpk")
print(f"Zero={z}")   #cheby1은 passband에 리플 존재해서 Rp고려!
print(f"Pole={p}")
print(f"Gain={k:.3f}")

plt.figure(1)
splane(b,a)


w, H=signal.freqs(b,a)  #Rp 고려
plt.figure(2)
plt.plot(w/np.pi, np.abs(H), "blue"); plt.grid(); plt.xlim(0,1)
plt.title("Magnitude response of Chebyshev-1 Lowpass Filter")
plt.xlabel("Frequency in pi radians")
plt.ylabel("|H|, Magnitude")

plt.show()