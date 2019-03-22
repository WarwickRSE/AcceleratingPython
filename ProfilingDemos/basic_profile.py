
from math import sin, pi

def calc_wave_amplitude(time, freq, phase):

  return sin(2.0*pi*freq*time + phase)

def simple_calc_w_temporaries(frequencies, phases, amplitudes, axis, wave):

  wave_temp = wave
  for i in range(0,len(frequencies)):
    print(frequencies[i], phases[i])
    for j in range(0,len(axis)):
      wave_temp[j] = calc_wave_amplitude(axis[j], frequencies[i], phases[i])
    wave = wave + amplitudes[i]*wave_temp

def simple_calc(frequencies, phases, amplitudes, axis, wave):

  for i in range(0,len(frequencies)):
    print(frequencies[i], phases[i])
    for j in range(0,len(axis)):
      wave[j] = wave[j] + (amplitudes[i] * calc_wave_amplitude(axis[j], frequencies[i], phases[i]))

def main():

  frequencies = [0.1, 0.01, 0.001, 0.0001]
  phases = [0, 0, 0, 0]
  amplitudes = [1, 1, 1, 1]

  ax_len = 100000
  wave = [0]*ax_len
  axis = range(0,ax_len)
  for el in axis:
    el = el *100

  simple_calc(frequencies, phases, amplitudes, axis, wave)
  simple_calc_w_temporaries(frequencies, phases, amplitudes, axis, wave)

if __name__== "__main__":

  import cProfile as prof

  prof.run("main()")
