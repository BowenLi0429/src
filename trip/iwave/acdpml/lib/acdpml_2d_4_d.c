/*        Generated by TAPENADE     (INRIA, Tropics team)
    Tapenade 3.7 (r4786) - 21 Feb 2013 15:53
*/
#include "cstd.h"

/*
  Differentiation of acdpml_2d_4 in forward (tangent) mode:
   variations   of useful results: **phi0 **up **phi1
   with respect to varying inputs: **csq **uc **phi0 **up **phi1
   RW status of diff variables: **csq:in **uc:in **phi0:in-out
                **up:in-out **phi1:in-out
   Plus diff mem management of: csq:in *csq:in uc:in *uc:in phi0:in
                *phi0:in up:in *up:in phi1:in *phi1:in
*/
void acdpml_2d_4_d(float **uc, float **ucd, float **up, float **upd, float **
        csq, float **csqd, float **phi1, float **phi1d, float **phi0, float **
        phi0d, float *dp1, float *dp0, float *di, float dt, int *s, int *e, 
        float c0, float *c1, float *c2, int *lbc, int *rbc) {
    /* current field
    // previous field
    // csq
    // phi1
    // phi0
    // damping profile zeta_x
    // damping profile zeta_x
    // start index
    // end index */
    int i1, i0;
    /* fprintf(stderr, "dp0[%d] = %f\n",e[0], dp0[e[0]]);
    // PML
    //fprintf(stderr, " after computing Du_x Du_z acdpml_2d_2!!!\n");
    // \phi separate loops along boundary !!!!!!!!!!!!!!!! csq and damp profile
    // compute interior of the domain
    // update wavefield up */
    for (i1 = s[1]; i1 < e[1]+1; ++i1)
        for (i0 = s[0]; i0 < e[0]+1; ++i0) {
            float lap = c0*uc[i1][i0] + c1[1]*(uc[i1-1][i0]+uc[i1+1][i0]) + c2
            [1]*(uc[i1-2][i0]+uc[i1+2][i0]) + c1[0]*(uc[i1][i0-1]+uc[i1][i0+1]
            ) + c2[0]*(uc[i1][i0-2]+uc[i1][i0+2]);
            float lapd = c0*ucd[i1][i0] + c1[1]*(ucd[i1-1][i0]+ucd[i1+1][i0]) 
            + c2[1]*(ucd[i1-2][i0]+ucd[i1+2][i0]) + c1[0]*(ucd[i1][i0-1]+ucd[
            i1][i0+1]) + c2[0]*(ucd[i1][i0-2]+ucd[i1][i0+2]);
            float cff = 1.0/(1.0+(dp1[i1]+dp0[i0])*dt/2.0);
            float cffuc = (2.0-dp1[i1]*dp0[i0]*dt*dt)*cff;
            float cffup = ((dp1[i1]+dp0[i0])/2.0*dt-1.0)*cff;
            float cff1 = dt*dt/2.0/di[1]*cff;
            float cff0 = dt*dt/2.0/di[0]*cff;
            upd[i1][i0] = cffuc*ucd[i1][i0] + cffup*upd[i1][i0] + cff*(csqd[i1
                ][i0]*lap+csq[i1][i0]*lapd) + cff1*(phi1d[i1][i0-1]+phi1d[i1][
                i0]-phi1d[i1-1][i0-1]-phi1d[i1-1][i0]) + cff0*(phi0d[i1-1][i0]
                +phi0d[i1][i0]-phi0d[i1-1][i0-1]-phi0d[i1][i0-1]);
            up[i1][i0] = cffuc*uc[i1][i0] + cffup*up[i1][i0] + cff*csq[i1][i0]
                *lap + cff1*(phi1[i1][i0-1]+phi1[i1][i0]-phi1[i1-1][i0-1]-phi1
                [i1-1][i0]) + cff0*(phi0[i1-1][i0]+phi0[i1][i0]-phi0[i1-1][i0-
                1]-phi0[i1][i0-1]);
        }
    for (i1 = s[1]; i1 < e[1]; ++i1)
        for (i0 = s[0]; i0 < e[0]; ++i0) {
            float cff1 = (2.0-dt*dp1[i1])/(2.0+dt*dp1[i1]);
            float cff0 = (2.0-dt*dp0[i0])/(2.0+dt*dp0[i0]);
            float tmp = (csq[i1][i0]+csq[i1+1][i0]+csq[i1][i0+1]+csq[i1+1][i0+
            1])/4.0*2.0*dt;
            float tmpd = 2.0*dt*(csqd[i1][i0]+csqd[i1+1][i0]+csqd[i1][i0+1]+
            csqd[i1+1][i0+1])/4.0;
            float tmpux = (uc[i1+1][i0]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1][i0+1]
            +up[i1+1][i0]+up[i1+1][i0+1]-up[i1][i0]-up[i1][i0+1])/4.0/di[1]*(
            dp0[i0]-dp1[i1])/(2.0+dt*dp1[i1]);
            float tmpuxd = (dp0[i0]-dp1[i1])*(ucd[i1+1][i0]+ucd[i1+1][i0+1]-
            ucd[i1][i0]-ucd[i1][i0+1]+upd[i1+1][i0]+upd[i1+1][i0+1]-upd[i1][i0
            ]-upd[i1][i0+1])/(4.0*di[1])/(2.0+dt*dp1[i1]);
            float tmpuz = (uc[i1][i0+1]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1+1][i0]
            +up[i1][i0+1]+up[i1+1][i0+1]-up[i1][i0]-up[i1+1][i0])/4.0/di[0]*(
            dp1[i1]-dp0[i0])/(2.0+dt*dp0[i0]);
            float tmpuzd = (dp1[i1]-dp0[i0])*(ucd[i1][i0+1]+ucd[i1+1][i0+1]-
            ucd[i1][i0]-ucd[i1+1][i0]+upd[i1][i0+1]+upd[i1+1][i0+1]-upd[i1][i0
            ]-upd[i1+1][i0])/(4.0*di[0])/(2.0+dt*dp0[i0]);
            phi1d[i1][i0] = cff1*phi1d[i1][i0] + tmpuxd*tmp + tmpux*tmpd;
            phi1[i1][i0] = phi1[i1][i0]*cff1 + tmpux*tmp;
            phi0d[i1][i0] = cff0*phi0d[i1][i0] + tmpuzd*tmp + tmpuz*tmpd;
            phi0[i1][i0] = phi0[i1][i0]*cff0 + tmpuz*tmp;
        }
    i1 = s[1] - 1;
    i0 = s[0] - 1;
    float cff1 = (2.0-dt*dp1[i1])/(2.0+dt*dp1[i1]);
    float cff0 = (2.0-dt*dp0[i0])/(2.0+dt*dp0[i0]);
    float tmpux = (uc[i1+1][i0]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1][i0+1]+up[i1+1
    ][i0]+up[i1+1][i0+1]-up[i1][i0]-up[i1][i0+1])/4.0/di[1]*(dp0[i0]-dp1[i1])/
    (2.0+dt*dp1[i1]);
    float tmpuxd = (dp0[i0]-dp1[i1])*(ucd[i1+1][i0]+ucd[i1+1][i0+1]-ucd[i1][i0
    ]-ucd[i1][i0+1]+upd[i1+1][i0]+upd[i1+1][i0+1]-upd[i1][i0]-upd[i1][i0+1])/(
    4.0*di[1])/(2.0+dt*dp1[i1]);
    float tmpuz = (uc[i1][i0+1]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1+1][i0]+up[i1][
    i0+1]+up[i1+1][i0+1]-up[i1][i0]-up[i1+1][i0])/4.0/di[0]*(dp1[i1]-dp0[i0])/
    (2.0+dt*dp0[i0]);
    float tmpuzd = (dp1[i1]-dp0[i0])*(ucd[i1][i0+1]+ucd[i1+1][i0+1]-ucd[i1][i0
    ]-ucd[i1+1][i0]+upd[i1][i0+1]+upd[i1+1][i0+1]-upd[i1][i0]-upd[i1+1][i0])/(
    4.0*di[0])/(2.0+dt*dp0[i0]);
    phi1d[i1][i0] = cff1*phi1d[i1][i0] + 2.0*dt*(tmpuxd*csq[i1+1][i0+1]+tmpux*
        csqd[i1+1][i0+1]);
    phi1[i1][i0] = phi1[i1][i0]*cff1 + tmpux*2.0*dt*csq[i1+1][i0+1];
    phi0d[i1][i0] = cff0*phi0d[i1][i0] + 2.0*dt*(tmpuzd*csq[i1+1][i0+1]+tmpuz*
        csqd[i1+1][i0+1]);
    phi0[i1][i0] = phi0[i1][i0]*cff0 + tmpuz*2.0*dt*csq[i1+1][i0+1];
    /* compute i1=s[1]-1 */
    i1 = s[1] - 1;
    for (i0 = s[0]; i0 < e[0]+1; ++i0) {
        cff1 = (2.0-dt*dp1[i1])/(2.0+dt*dp1[i1]);
        cff0 = (2.0-dt*dp0[i0])/(2.0+dt*dp0[i0]);
        tmpuxd = (dp0[i0]-dp1[i1])*(ucd[i1+1][i0]+ucd[i1+1][i0+1]-ucd[i1][i0]-
            ucd[i1][i0+1]+upd[i1+1][i0]+upd[i1+1][i0+1]-upd[i1][i0]-upd[i1][i0
            +1])/(4.0*di[1])/(2.0+dt*dp1[i1]);
        tmpux = (uc[i1+1][i0]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1][i0+1]+up[i1+1][
            i0]+up[i1+1][i0+1]-up[i1][i0]-up[i1][i0+1])/4.0/di[1]*(dp0[i0]-dp1
            [i1])/(2.0+dt*dp1[i1]);
        tmpuzd = (dp1[i1]-dp0[i0])*(ucd[i1][i0+1]+ucd[i1+1][i0+1]-ucd[i1][i0]-
            ucd[i1+1][i0]+upd[i1][i0+1]+upd[i1+1][i0+1]-upd[i1][i0]-upd[i1+1][
            i0])/(4.0*di[0])/(2.0+dt*dp0[i0]);
        tmpuz = (uc[i1][i0+1]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1+1][i0]+up[i1][i0
            +1]+up[i1+1][i0+1]-up[i1][i0]-up[i1+1][i0])/4.0/di[0]*(dp1[i1]-dp0
            [i0])/(2.0+dt*dp0[i0]);
        phi1d[i1][i0] = cff1*phi1d[i1][i0] + 2.0*dt*(tmpuxd*csq[i1+1][i0]+
            tmpux*csqd[i1+1][i0]);
        phi1[i1][i0] = phi1[i1][i0]*cff1 + tmpux*2.0*dt*csq[i1+1][i0];
        phi0d[i1][i0] = cff0*phi0d[i1][i0] + 2.0*dt*(tmpuzd*csq[i1+1][i0]+
            tmpuz*csqd[i1+1][i0]);
        phi0[i1][i0] = phi0[i1][i0]*cff0 + tmpuz*2.0*dt*csq[i1+1][i0];
    }
    /* compute i0=s[0]-1 */
    i0 = s[0] - 1;
    for (i1 = s[1]; i1 < e[1]+1; ++i1) {
        cff1 = (2.0-dt*dp1[i1])/(2.0+dt*dp1[i1]);
        cff0 = (2.0-dt*dp0[i0])/(2.0+dt*dp0[i0]);
        tmpuxd = (dp0[i0]-dp1[i1])*(ucd[i1+1][i0]+ucd[i1+1][i0+1]-ucd[i1][i0]-
            ucd[i1][i0+1]+upd[i1+1][i0]+upd[i1+1][i0+1]-upd[i1][i0]-upd[i1][i0
            +1])/(4.0*di[1])/(2.0+dt*dp1[i1]);
        tmpux = (uc[i1+1][i0]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1][i0+1]+up[i1+1][
            i0]+up[i1+1][i0+1]-up[i1][i0]-up[i1][i0+1])/4.0/di[1]*(dp0[i0]-dp1
            [i1])/(2.0+dt*dp1[i1]);
        tmpuzd = (dp1[i1]-dp0[i0])*(ucd[i1][i0+1]+ucd[i1+1][i0+1]-ucd[i1][i0]-
            ucd[i1+1][i0]+upd[i1][i0+1]+upd[i1+1][i0+1]-upd[i1][i0]-upd[i1+1][
            i0])/(4.0*di[0])/(2.0+dt*dp0[i0]);
        tmpuz = (uc[i1][i0+1]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1+1][i0]+up[i1][i0
            +1]+up[i1+1][i0+1]-up[i1][i0]-up[i1+1][i0])/4.0/di[0]*(dp1[i1]-dp0
            [i0])/(2.0+dt*dp0[i0]);
        phi1d[i1][i0] = cff1*phi1d[i1][i0] + 2.0*dt*(tmpuxd*csq[i1][i0+1]+
            tmpux*csqd[i1][i0+1]);
        phi1[i1][i0] = phi1[i1][i0]*cff1 + tmpux*2.0*dt*csq[i1][i0+1];
        phi0d[i1][i0] = cff0*phi0d[i1][i0] + 2.0*dt*(tmpuzd*csq[i1][i0+1]+
            tmpuz*csqd[i1][i0+1]);
        phi0[i1][i0] = phi0[i1][i0]*cff0 + tmpuz*2.0*dt*csq[i1][i0+1];
    }
    /* compute i1=e[1] */
    i1 = e[1];
    for (i0 = s[0]; i0 < e[0]+1; ++i0) {
        cff1 = (2.0-dt*dp1[i1])/(2.0+dt*dp1[i1]);
        cff0 = (2.0-dt*dp0[i0])/(2.0+dt*dp0[i0]);
        tmpuxd = (dp0[i0]-dp1[i1])*(ucd[i1+1][i0]+ucd[i1+1][i0+1]-ucd[i1][i0]-
            ucd[i1][i0+1]+upd[i1+1][i0]+upd[i1+1][i0+1]-upd[i1][i0]-upd[i1][i0
            +1])/(4.0*di[1])/(2.0+dt*dp1[i1]);
        tmpux = (uc[i1+1][i0]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1][i0+1]+up[i1+1][
            i0]+up[i1+1][i0+1]-up[i1][i0]-up[i1][i0+1])/4.0/di[1]*(dp0[i0]-dp1
            [i1])/(2.0+dt*dp1[i1]);
        tmpuzd = (dp1[i1]-dp0[i0])*(ucd[i1][i0+1]+ucd[i1+1][i0+1]-ucd[i1][i0]-
            ucd[i1+1][i0]+upd[i1][i0+1]+upd[i1+1][i0+1]-upd[i1][i0]-upd[i1+1][
            i0])/(4.0*di[0])/(2.0+dt*dp0[i0]);
        tmpuz = (uc[i1][i0+1]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1+1][i0]+up[i1][i0
            +1]+up[i1+1][i0+1]-up[i1][i0]-up[i1+1][i0])/4.0/di[0]*(dp1[i1]-dp0
            [i0])/(2.0+dt*dp0[i0]);
        phi1d[i1][i0] = cff1*phi1d[i1][i0] + 2.0*dt*(tmpuxd*csq[i1][i0]+tmpux*
            csqd[i1][i0]);
        phi1[i1][i0] = phi1[i1][i0]*cff1 + tmpux*2.0*dt*csq[i1][i0];
        phi0d[i1][i0] = cff0*phi0d[i1][i0] + 2.0*dt*(tmpuzd*csq[i1][i0]+tmpuz*
            csqd[i1][i0]);
        phi0[i1][i0] = phi0[i1][i0]*cff0 + tmpuz*2.0*dt*csq[i1][i0];
    }
    /* compute i0=e[0] */
    i0 = e[0];
    for (i1 = s[1]; i1 < e[1]; ++i1) {
        cff1 = (2.0-dt*dp1[i1])/(2.0+dt*dp1[i1]);
        cff0 = (2.0-dt*dp0[i0])/(2.0+dt*dp0[i0]);
        tmpuxd = (dp0[i0]-dp1[i1])*(ucd[i1+1][i0]+ucd[i1+1][i0+1]-ucd[i1][i0]-
            ucd[i1][i0+1]+upd[i1+1][i0]+upd[i1+1][i0+1]-upd[i1][i0]-upd[i1][i0
            +1])/(4.0*di[1])/(2.0+dt*dp1[i1]);
        tmpux = (uc[i1+1][i0]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1][i0+1]+up[i1+1][
            i0]+up[i1+1][i0+1]-up[i1][i0]-up[i1][i0+1])/4.0/di[1]*(dp0[i0]-dp1
            [i1])/(2.0+dt*dp1[i1]);
        tmpuzd = (dp1[i1]-dp0[i0])*(ucd[i1][i0+1]+ucd[i1+1][i0+1]-ucd[i1][i0]-
            ucd[i1+1][i0]+upd[i1][i0+1]+upd[i1+1][i0+1]-upd[i1][i0]-upd[i1+1][
            i0])/(4.0*di[0])/(2.0+dt*dp0[i0]);
        tmpuz = (uc[i1][i0+1]+uc[i1+1][i0+1]-uc[i1][i0]-uc[i1+1][i0]+up[i1][i0
            +1]+up[i1+1][i0+1]-up[i1][i0]-up[i1+1][i0])/4.0/di[0]*(dp1[i1]-dp0
            [i0])/(2.0+dt*dp0[i0]);
        phi1d[i1][i0] = cff1*phi1d[i1][i0] + 2.0*dt*(tmpuxd*csq[i1][i0]+tmpux*
            csqd[i1][i0]);
        phi1[i1][i0] = phi1[i1][i0]*cff1 + tmpux*2.0*dt*csq[i1][i0];
        phi0d[i1][i0] = cff0*phi0d[i1][i0] + 2.0*dt*(tmpuzd*csq[i1][i0]+tmpuz*
            csqd[i1][i0]);
        phi0[i1][i0] = phi0[i1][i0]*cff0 + tmpuz*2.0*dt*csq[i1][i0];
    }
    /* Homogeneous Dirichlet boundary conditions */
    if (lbc[1])
        for (i0 = s[0]; i0 < e[0]+1; ++i0) {
            upd[s[1] - 2][i0] = -upd[s[1]][i0];
            up[s[1] - 2][i0] = -up[s[1]][i0];
            upd[s[1] - 1][i0] = 0.0;
            up[s[1] - 1][i0] = 0;
        }
    if (rbc[1])
        for (i0 = s[0]; i0 < e[0]+1; ++i0) {
            upd[e[1] + 2][i0] = -upd[e[1]][i0];
            up[e[1] + 2][i0] = -up[e[1]][i0];
            upd[e[1] + 1][i0] = 0.0;
            up[e[1] + 1][i0] = 0;
        }
    if (lbc[0])
        for (i1 = s[1]; i1 < e[1]+1; ++i1) {
            upd[i1][s[0] - 2] = -upd[i1][s[0]];
            up[i1][s[0] - 2] = -up[i1][s[0]];
            upd[i1][s[0] - 1] = 0.0;
            up[i1][s[0] - 1] = 0;
        }
    if (rbc[0])
        for (i1 = s[1]; i1 < e[1]+1; ++i1) {
            upd[i1][e[0] + 2] = -upd[i1][e[0]];
            up[i1][e[0] + 2] = -up[i1][e[0]];
            upd[i1][e[0] + 1] = 0.0;
            up[i1][e[0] + 1] = 0;
        }
}
