#include <stdio.h>
#include <math.h>
#include <float.h>
#include <stdlib.h>

#define NPLANET 10

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

void run()
{
  int p1, np;
  double *vorb, *porb;
  double masses[] = {m_sol, 0.0553,0.815,1.0,0.11,317.8,95.2,14.6,17.2, 0.002};
  double radii[] = {0.0, 0.39, 0.723, 1.0, 1.524, 5.203, 9.539, 19.18, 30.06, 
      39.53};
  double minporb = DBL_MAX; double maxporb = 0.0;
  double dt; int nits, it;
  FILE * output;

  planet *planets = NULL;
  planets = malloc(sizeof(planet) * NPLANET);
  vorb = malloc(sizeof(double) * NPLANET);
  porb = malloc(sizeof(double) * NPLANET);

  vorb[0] = 0.0; porb[0] = 0.0;
  for (p1 = 0; p1 < NPLANET; ++p1){
    masses[p1] *= m_earth; radii[p1] *= r_au;
    planets[p1].mass = masses[p1];
    if (p1 == 0) continue;
    vorb[p1] = sqrt(bigG * m_sol * m_earth / fabs(radii[p1]));
    porb[p1] = 2.0 * M_PI * radii[p1] / vorb[p1];
    if (porb[p1] > maxporb) maxporb = porb[p1];
    if (porb[p1] < minporb) minporb = porb[p1];
  }
  //10 Iterations over fastest orbit
  dt = minporb/10.0;
  nits = (ceil(maxporb/dt));

  nits *= 1000;

  for (p1 = 0; p1 < NPLANET; ++p1){
    planets[p1].x = malloc(sizeof(double) * (nits+1));
    planets[p1].y = malloc(sizeof(double) * (nits+1));
    planets[p1].vx = malloc(sizeof(double) * (nits+1));
    planets[p1].vy = malloc(sizeof(double) * (nits+1));
    planets[p1].x[0] = radii[p1];
    planets[p1].y[0] = 0.0;
    planets[p1].vx[0] = 0.0;
    planets[p1].vy[0] = vorb[p1];
  }


  for (it = 0; it< nits; ++it){
    iterate(planets, dt, NPLANET, it);
  }


  output = fopen("planets.dat","wb");
  np = NPLANET;
  fwrite(&np, sizeof(int), 1, output);
  np = nits + 1;
  fwrite(&np, sizeof(int), 1, output);
  
  for (p1 = 0; p1 < NPLANET; ++p1)
    {fwrite(planets[p1].x, sizeof(double), nits+1, output);}
  for (p1 = 0; p1 < NPLANET; ++p1)
    {fwrite(planets[p1].y, sizeof(double), nits+1, output);}
  for (p1 = 0; p1 < NPLANET; ++p1)
    {fwrite(planets[p1].vx, sizeof(double), nits+1, output);}
  for (p1 = 0; p1 < NPLANET; ++p1)
    {fwrite(planets[p1].vy, sizeof(double), nits+1, output);}
  fclose(output);

  for (p1 = 0; p1 < NPLANET; ++p1){
    free(planets[p1].x);
    free(planets[p1].y);
    free(planets[p1].vx);
    free(planets[p1].vy);
  }

  free(planets); free(vorb); free(porb);
}

int main (int argc, char ** argv)
{

  double f[2];

  run();

  pair_force(1.0,1.0, 0.0, 0.0, 1.0, 1.0, f);



  return 0;
}
