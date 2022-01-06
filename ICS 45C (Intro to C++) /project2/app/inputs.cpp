#include <iostream>
#include <string>
#include "calculate.hpp"
#include "outputs.hpp"
#include "students.hpp"

//struct Student {
//    int id;
//    char opt;
//    std::string name;
//    double score = 0.0;
    //char* grade = new char[3]
    //char g1 = 'F';
    //char g2 = 'F';
    //char g3 = 'F';
//};

void Inputs(){

    int n;
    std::cin>>n;

    int* pp = new int[n];
    int* rp = new int[n];

    for (int i=0; i<n; i++){
        std::cin>>pp[i];
    }
    for (int i=0; i<n; i++){
        std::cin>>rp[i];
    }
    
    int sn;
    std::cin>>sn;

    Student* stdnt_info = new Student[sn];

    for (int i=0; i<sn; i++){
        int i_d;
        char g;
        std::string sname;

        std::cin>>i_d>>g;
        std::getline(std::cin.ignore(1), sname);

        Student s{i_d, g, sname, 0.0}; //pass in grade[] too??
        stdnt_info[i] = s;



    }

    int rs;
    std::cin>>rs;

    //int* raws = new int[n+1];

    for (int x=0; x<rs; x++){
        int* raws = new int[n+1];
        for (int i=0; i<n+1; i++){
            std::cin>>raws[i];
        }

        double scr = Calculate(raws, pp, rp, n);
        
        for (int i=0; i<sn; i++){
            if (stdnt_info[i].id == raws[0]){
                stdnt_info[i].score = scr;
            }

        }
        delete[] raws;
        
    }
    Outputs(stdnt_info, sn);

    int c;
    std::cin>>c;

    for (int i=0; i<c; i++){
        double* ctpt = new double[4];
        for (int x=0; x<4; x++){
            std::cin>>ctpt[x];
        }
        Cutpoints(stdnt_info, sn, ctpt, i);
        delete[] ctpt;

    }
    delete[] pp;
    delete[] rp;
    delete[] stdnt_info;

}



