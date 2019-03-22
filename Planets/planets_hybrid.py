import numpy as np
import matplotlib.pyplot as plt
import time
from ctypes import *
from numba import jit

bigG = 1.0 #Just put G=1 for simplicity
m_earth = 1.0 #Mass of earth in earth masses
m_sol = 332946# Mass of sun in earth masses
r_au = 1.0 # 1 AU
so_fn = None
#Creating this array is expensive so keep this around
res = np.zeros(2,dtype=c_double)
res_cptr = res.ctypes.data_as(POINTER(c_double))

def load_so():
    global so_fn
    so = CDLL('./pairforce.so')
    so.pair_force.argtypes=[c_double, c_double, c_double, c_double, c_double, c_double, POINTER(c_double)]
    so_fn = so.pair_force

def pair_force(x1, x2, m1, m2):

    global so_fn, res
    dummy = so_fn(x1[0], x1[1], x2[0], x2[1], m1, m2, res_cptr)
    return res

@jit
def integrate(positions, velocities, masses, dt):
    nplanets = np.shape(masses)[0]
    vprime = np.zeros(np.shape(velocities))
    pout = np.zeros([nplanets,2])
    vout = np.zeros([nplanets,2])

    #Calculate forces on planets and update velocities to half timestep
    #Note the lower bound of p1. No force on sun. Set to 0 to include this effect
    for p1 in range(1, nplanets):
      f = np.zeros(2)
      for p2 in range(0, nplanets):
        if p1 == p2: continue #no self force
        f += pair_force(positions[p1,:], positions[p2,:], masses[p1], masses[p2])
      vprime[p1,:] = velocities[p1,:] + dt/2.0 * f/masses[p1]

    #Update positions using half timestep velocities
    pout = positions + dt * vprime

    #Calculate forces on planets and update velocities to full timestep
    #Note the lower bound of p1. No force on sun. Set to 0 to include this effect
    for p1 in range(1, nplanets):
      f = np.zeros(2)
      for p2 in range(0, nplanets):
        if p1 == p2: continue #no self force
        f += pair_force(pout[p1,:], pout[p2,:], masses[p1], masses[p2])
      vout[p1,:] = vprime[p1,:] + dt/2.0 * f/masses[p1]

    return pout, vout

def run():

  global m_sol, m_earth, r_au

  #Don't time the loading of the shared object
  load_so()
  t0 =time.clock()
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

  pin = np.zeros([nplanets,2, nits+1])
  vin = np.zeros([nplanets,2, nits+1])

  pin[:,0,0] = radii
  vin[:,1,0] = vorb

  t1 = time.clock()

  for it in range(0, nits):
    pout, vout = integrate(pin[:,:,it], vin[:,:,it], mass, dt)
    pin[:,:,it+1] = pout
    vin[:,:,it+1] = vout

  t2 = time.clock()

  print('Setup time(ms) ' + str(int((t1-t0)*1000.0)))
  print('Run time(ms) ' + str(int((t2-t1)*1000.0)))
  print('Total time(ms) ' + str(int((t2-t0)*1000.0)))

  return pin, vin

def demo():

  pin, vin = run()

  nits = np.shape(pin)[2]
  nplanets = np.shape(pin)[0]

  nplotx = 6
  nploty = 4
  nplot = nplotx * nploty
  arr = np.linspace(0.1,1.0,nplot)
  thisit = [int(el) for el in np.ceil(arr * np.float64(nits))]
  plt.figure()
  for it in range(1,nplot+1):
    plt.subplot(nploty,nplotx,it)
    for p1 in range(0, nplanets):
      plt.plot(pin[p1,0,0:thisit[it-1]], pin[p1,1,0:thisit[it-1]])
    axes = plt.gca()
    axes.set_xlim([-40,40])
    axes.set_ylim([-40,40])

  plt.show()
