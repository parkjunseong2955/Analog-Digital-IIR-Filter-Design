import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import chirp
from matplotlib import patches, rcParams

def Frequency_response_Signal_filtering(b,a):
    system=[b,a,1] #1은 초간격
    n,hn=signal.dimpulse(system) #결과값 hn은 파이썬 배열로 나옴, 이를 numpy 배열로 바꿔줘야 수학적 연산등이 가능
    hn=np.asarray(hn).squeeze() #squeeze는 불필요한 차원 없애기

    t=np.linspace(0,1,5000)
    xn=chirp(t, f0=10, t1=0.2, f1=500, method="linear")
    yn=np.convolve(hn,xn) #filter의 impulse함수와 입력 xn을 필터링(컨볼루션)

    plt.plot(yn,"b"); plt.xlim(0,5000)
    plt.title("Frequency Filtering Result")
    plt.xlabel("Samples(Frequency(0~5000[Hz]))")
    plt.grid()

np.set_printoptions(precision=3, suppress=True)

wp=0.2*np.pi #DT에서 passband cutoff frequency
ws=0.3*np.pi #DT에서 stopband cutoff frequency
Rp=7 #passband에서 ripple parameter [dB]
As=40
T=1 #Td
Fs=1/T #sampling frequency

OmegaP=(2/T)*np.tan(wp/2); print(f"wp={wp:.3f} = {wp/np.pi:.3f}pi")
OmegaS=(2/T)*np.tan(ws/2); print(f"ws={ws:.3f} = {ws/np.pi:.3f}pi")

print("\n", "-------------Filter order, Cutoff frequency-------------")
N,wc=signal.buttord(OmegaP,OmegaS,Rp,As,analog=True)
print(f'Filter Order N={N}')
print(f"cutoff frequency wc = {wc}")

print("\n", "-----------------Analog Filter----------------")
b,a=signal.butter(N,wc,"lowpass", analog=True)
print(f"Numerator coefficient of system function Ha(s) = {b}")
print(f"Denominator coefficient of system function Ha(s) = {a}")

print("\n", "-----------------Digital Filter(Direct type)-------------")
d,c=signal.bilinear(b,a,Fs)
print(f"Numerator coefficient of system function H(z)={d}")
print(f"Denominator coefficient of system function H(z)={c}")

plt.figure(1)
Omega,H=signal.freqz(d,c)
plt.plot(Omega/np.pi, np.abs(H), "blue"); plt.grid(); plt.xlim(0,1)
plt.title("Frequency Response of Digital Butterworth Lowpass Filter")
plt.xlabel("Frequency in pi radians")
plt.ylabel("|H|, magnitude")

plt.figure(2)
Frequency_response_Signal_filtering(d,c)

plt.show()