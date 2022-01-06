#include <cmath>
#include <string>

double Distance(double lat1, char ns1, double lon1, char ew1, double lat2, char ns2, double lon2, char ew2){
    double R = 3959.9;
    double dlat = 0.0;
    double dlon = 0.0;

    if (ns1 != ns2){
        dlat = (lat2+lat1)*(3.1415923565/180.0);
    } else if (ns1 == ns2){
        dlat = (lat2-lat1)*(3.1415923565/180.0);
    } else{}
    if (ew1 != ew2){
        dlon = (lon2+lon1)*(3.1415923565/180.0);
    } else if (ew1 == ew2){
        dlon = (lon2-lon1)*(3.1415923565/180.0);
    } else{}


    double a = pow(sin(dlat/2.0),2) + cos(lat1*(3.1415923565/180.0)) * cos(lat2*(3.1415923565/180.0)) * pow(sin(dlon/2.0),2);
    double c = 2.0 * atan2(sqrt(a), sqrt(1 - a));
    double d = R * c;

    return d;
}