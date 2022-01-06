#include <iostream>
#include <string>
#include "distance.hpp"

double lat;
char ns;
double lon;
char ew;
std::string arpt;
int n;

double max = 0;
double min = 99999.9;
double clt;
char cns;
double cln;
char cew;
std::string carpt;
double flt;
char fns;
double fln;
char few;
std::string farpt;

void Input(){
    std::cin>>lat;
    std::cin.ignore(1)>>ns>>lon;
    std::cin.ignore(1)>>ew;
    std::getline(std::cin.ignore(1), arpt);

    std::cin>>n;

    for (int i=1; i<n+1; i++){
        double lat2;
        char ns2;
        double lon2;
        char ew2;
        std::string arpt2;

        std::cin>>lat2;
        std::cin.ignore(1)>>ns2>>lon2;
        std::cin.ignore(1)>>ew2;
        std::getline(std::cin.ignore(1), arpt2);

        //std::cout<<lat<<" "<<ns<<" "<<lon<<" "<<ew<<" "<<lat2<<" "<<ns2<<" "<<lon2<<" "<<ew2<<"\n";
        double dis = Distance(lat, ns, lon, ew, lat2, ns2, lon2, ew2);
        //std::cout<<dis<<"\n";
        if (dis < min){
            min=dis, clt=lat2, cns=ns2, cln=lon2, cew=ew2, carpt=arpt2;
        }
        if (dis > max){
            max=dis, flt=lat2, fns=ns2, fln=lon2, few=ew2, farpt=arpt2;
        }
    }
}

void Output(){
    std::cout<<"Start Location: "<<lat<<"/"<<ns<<" "<<lon<<"/"<<ew<<" "<<"("<<arpt<<")"<<"\n";
    std::cout<<"Closest Location: "<<clt<<"/"<<cns<<" "<<cln<<"/"<<cew<<" "<<"("<<carpt<<")"<<" "<<"("<<min<<" miles"<<")"<<"\n";
    std::cout<<"Farthest Location: "<<flt<<"/"<<fns<<" "<<fln<<"/"<<few<<" "<<"("<<farpt<<")"<<" "<<"("<<max<<" miles"<<")"<<"\n";
}


//void StartOutput(lt, n_s, ln, e_w, name, mil){
//    std::cout<<"Start Location: "<<lt<<"/"<<n_s<<" "<<ln<<"/"<<e_w<<" "<<"("<<name<<")"<<"\n";    
//}

//void ClosestOutput(lt, n_s, ln, e_w, name, mil){
//    std::cout<<"Closest Location: "<<lt<<"/"<<n_s<<" "<<ln<<"/"<<e_w<<" "<<"("<<name<<")"<<" "<<"("<<mil<<" miles"<<")"<<"\n";

//}

//void FarthestOutput(lt, n_s, ln, e_w, name, mil){
//    std::cout<<"Farthest Location: "<<lt<<"/"<<n_s<<" "<<ln<<"/"<<e_w<<" "<<"("<<name<<")"<<" "<<"("<<mil<<" miles"<<")"<<"\n";
//}