#include <math.h>

void pairforce(double x1, double y1, double x2, double y2, double m1, double m2
    , double *f)
{
  double r = sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
      + 1.0e-9 ;
  f[0] += -m1*m2*(x1-x2)/(r*r*r);
  f[1] += -m1*m2*(y1-y2)/(r*r*r);
}
