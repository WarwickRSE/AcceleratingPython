#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from ctypes import *
from numba import jit
from timeit import default_timer as timer
import sys

bigG = 1.0 #Just put G=1 for simplicity
m_earth = 1.0 #Mass of earth in earth masses
m_sol = 332946# Mass of sun in earth masses
r_au = 1.0 # 1 AU
so_fn = None

class planet_c(Structure):
    _fields_ = [('x', POINTER(c_double)),
                ('y', POINTER(c_double)),
                ('vx', POINTER(c_double)),
                ('vy', POINTER(c_double)),
                ('mass', c_double)]
    def __init__(self, count):
        self.x = (c_double * count)()
        self.y = (c_double * count)()
        self.vx = (c_double * count)()
        self.vy = (c_double * count)()
        self.mass = np.float64(1.0)



def load_so():
    global so_fn
    so = CDLL('./planets_lib.so')
    so.run.argtypes=[POINTER(planet_c), c_int, c_double, c_int]
    so_fn = so.run

def run():

  mass = np.array([m_sol, 0.0553,0.815,1.0,0.11,317.8,95.2,14.6,17.2, 0.002]) * m_earth
  radii = np.array([0.0, 0.39, 0.723, 1.0, 1.524, 5.203, 9.539, 19.18, 30.06, 39.53]) * r_au
  nplanets = np.shape(mass)[0]

  vorb = np.zeros(nplanets)
  #Zero initial velocity for sun
  #Approximate from circular motion
  vorb[1:] = np.sqrt(bigG * m_sol * m_earth / np.abs(radii[1:]))

  #Orbital period. Meaninless for sun so ignore
  porb = np.zeros(nplanets)
  porb[1:] = 2.0*np.pi * radii[1:]/vorb[1:]
  min_porb = np.min(porb[1:])
  max_porb = np.max(porb[1:])

  #10 Iterations over fastest orbit
  dt = min_porb/10.0
  nits = int(np.ceil(max_porb/dt))

  plist = [planet_c(nits+1) for x in range(10)]
  planets = (planet_c*10)(*plist)

  for p in range(nplanets):
      planets[p].x[0] = radii[p]
      planets[p].y[0] = 0.0
      planets[p].vx[0] = 0.0
      planets[p].vy[0] = vorb[p]
      planets[p].mass = mass[p]

  #Don't time the loading of the shared object
  load_so()
  so_fn(planets, 10, dt, nits)

  pout = np.zeros([10, 2, nits])
  vout = np.zeros([10 ,2, nits])

  for p in range(10):
      for it in range(nits):
          pout[p, 0, it] = planets[p].x[it]
          pout[p, 1, it] = planets[p].y[it]
          vout[p, 0, it] = planets[p].vx[it]
          vout[p, 1, it] = planets[p].vy[it]

  return nplanets, nits, planets

def demo():

  nplanets, nits, planets = run()

  nplotx = 6
  nploty = 4
  nplot = nplotx * nploty
  arr = np.linspace(0.1,1.0,nplot)
  thisit = [int(el) for el in np.ceil(arr * np.float64(nits))]
  plt.figure()
  for it in range(1,nplot+1):
    plt.subplot(nploty,nplotx,it)
    for p1 in range(0, nplanets):
      plt.plot(planets[p1].x[0:thisit[it-1]], planets[p1].y[0:thisit[it-1]])
    axes = plt.gca()
    axes.set_xlim([-40,40])
    axes.set_ylim([-40,40])

  plt.show()

def main(demo_flag):

  if (demo_flag):
    demo()
  else:
    start = timer()
    v=run()
    end = timer()
    print("Run took ", (end-start), " seconds")

if __name__ == "__main__":

  try:
    demo_flag = sys.argv[1].strip() == "demo"
  except:
    demo_flag = False

  main(demo_flag)

