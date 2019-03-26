
from math import sin, pi
import numpy as np
import time

sin_v = np.vectorize(sin)

def calc_wave_amplitude(time, freq, phase):

  return sin(2.0*pi*freq*time + phase)

calc_wave_amplitude_v = np.vectorize(calc_wave_amplitude, excluded =[2, 3])

def calc_wave_arg(time, freq, phase):

  return 2.0*pi*freq*time + phase

def simple_calc(frequencies, phases, amplitudes, axis, wave):

  for i in range(0,len(frequencies)):
    print(frequencies[i], phases[i])
    wave = wave + (amplitudes[i] * calc_wave_amplitude_v(axis, frequencies[i], phases[i]))


def better_calc(frequencies, phases, amplitudes, axis, wave):
#In this version, even if we change how we combine the parts
#of the argument, we still have a function doing it
#But we're taking full advantage of array ops

  for i in range(0,len(frequencies)):
    print(frequencies[i], phases[i])
    wave = wave + (amplitudes[i] * np.sin(calc_wave_arg(axis, frequencies[i], phases[i])))

def non_future_proofed_calc(frequencies, phases, amplitudes, axis, wave):
#Here we embed the "sin" call right into our code, meaning if the details change
#in future we'll have potentially a lot of work to do

  for i in range(0,len(frequencies)):
    print(frequencies[i], phases[i])
    wave = wave + (amplitudes[i] * sin_v(axis*frequencies[i]*2.0*pi + phases[i]))

def non_future_proofed_calc_a(frequencies, phases, amplitudes, axis, wave):
#Here we embed the "sin" call right into our code, meaning if the details change
#in future we'll have potentially a lot of work to do

  for i in range(0,len(frequencies)):
    print(frequencies[i], phases[i])
    wave = wave + (amplitudes[i] * np.sin(axis*frequencies[i]*2.0*pi + phases[i]))

def main():

  frequencies = np.array([0.1, 0.01, 0.001, 0.0001])
  phases = np.array([0, 0, 0, 0])
  amplitudes = np.array([1, 1, 1, 1])

  ax_len = 100000
  wave = np.array(ax_len)
  axis = np.arange(ax_len)*100

  start = time.time()
  non_future_proofed_calc(frequencies, phases, amplitudes, axis, wave)
  end = time.time()
  print("Vectorized sin took ", end-start, "s")

  start = time.time()
  non_future_proofed_calc_a(frequencies, phases, amplitudes, axis, wave)
  end = time.time()
  print("Numpy sin took ", end-start, "s")

  start = time.time()
  simple_calc(frequencies, phases, amplitudes, axis, wave)
  end = time.time()
  print("Attempted vectorisation took ", end-start, "s")

  start = time.time()
  better_calc(frequencies, phases, amplitudes, axis, wave)
  end = time.time()
  print("Array ops took ", end-start, "s")


if __name__== "__main__":

  import cProfile as prof

  prof.run("main()")
