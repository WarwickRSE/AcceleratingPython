#include <stdio.h>
#include <math.h>
#include <float.h>
#include <stdlib.h>

double bigG = 1.0; //Just put G=1 for simplicity
double m_earth = 1.0; //Mass of earth in earth masses
double m_sol = 332946; //Mass of sun in earth masses
double r_au = 1.0; // 1 AU

typedef struct planet planet;

struct planet{
  double *x, *y;
  double *vx, *vy;
  double mass;
};

void pair_force(double x1, double y1, double x2, double y2, double m1, double m2
    , double *f)
{
  double r = sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)) 
      + 1.0e-9 * r_au;
  f[0] += -bigG * m1*m2*(x1-x2)/(r*r*r);
  f[1] += -bigG * m1*m2*(y1-y2)/(r*r*r);

}

void iterate(planet *planets, double dt, int n_planets, int it)
{
  int p1, p2;
  double f[2], *vxprime, *vyprime;

  vxprime = malloc(sizeof(double) * n_planets);
  vyprime = malloc(sizeof(double) * n_planets);

  for (p1 = 1; p1 < n_planets; ++p1){
    f[0] = 0.0; f[1] = 0.0;
    for (p2 = 0; p2 < n_planets; ++p2){
      if (p1 == p2) continue;
      pair_force(planets[p1].x[it], planets[p1].y[it], planets[p2].x[it], 
          planets[p2].y[it], planets[p1].mass, planets[p2].mass, f);
    }
    vxprime[p1] = planets[p1].vx[it] + dt/2.0 * f[0]/planets[p1].mass;
    vyprime[p1] = planets[p1].vy[it] + dt/2.0 * f[1]/planets[p1].mass;
    planets[p1].x[it+1] = planets[p1].x[it] + dt * vxprime[p1];
    planets[p1].y[it+1] = planets[p1].y[it] + dt * vyprime[p1];
  }

  for (p1 = 1; p1 < n_planets; ++p1){
    f[0] = 0.0; f[1] = 0.0;
    for (p2 = 0; p2 < n_planets; ++p2){
      if (p1 == p2) continue;
      pair_force(planets[p1].x[it+1], planets[p1].y[it+1], planets[p2].x[it+1], 
          planets[p2].y[it+1], planets[p1].mass, planets[p2].mass, f);
    }
    planets[p1].vx[it+1] = vxprime[p1] + dt/2.0 * f[0]/planets[p1].mass;
    planets[p1].vy[it+1] = vyprime[p1] + dt/2.0 * f[1]/planets[p1].mass;
  }

  free(vxprime); free(vyprime);
}

void run(planet *planets, int n_planets, double dt, int nits)
{
  int p1;
  int it;

  for (it = 0; it< nits; ++it){
    iterate(planets, dt, n_planets, it);
  }

}
