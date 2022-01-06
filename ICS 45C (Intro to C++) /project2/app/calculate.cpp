#include <cmath>

double Calculate(int* r, int* p, int* pr, int x){
    double total  = 0.0;

    for (int i=0; i<x; i++){
        double t = ((double)r[i+1]/(double)p[i]) * (double)pr[i];
        total = total + t;
    }

    return total;
}

