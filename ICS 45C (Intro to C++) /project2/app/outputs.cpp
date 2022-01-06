#include <iostream>
#include "inputs.hpp"
#include "students.hpp"

void Outputs(Student* st, int x){
    std::cout<<"TOTAL SCORES"<<"\n";
    for (int i=0; i<x; i++){
        std::cout<<st[i].id<<" "<<st[i].name<<" "<<st[i].score<<"\n";
    }

}

void Cutpoints(Student* st, int x, double* c, int j){
    std::cout<<"CUTPOINT SET "<<j+1<<"\n";

    for (int i=0; i<x; i++){
        char grade;
        if (st[i].score >= c[0]){
            grade = 'A';
        } else if (st[i].score < c[0] and st[i].score >= c[1]){
            grade = 'B';
        }else if (st[i].score < c[1] and st[i].score >= c[2]){
            grade = 'C';
        }else if (st[i].score < c[2] and st[i].score >= c[3]){
            grade = 'D';
        } else{
            grade = 'F';
        }

        if (st[i].opt == 'G'){
            std::cout<<st[i].id<<" "<<st[i].name<<" "<<grade<<"\n";
        } else if (st[i].opt == 'P'){
            if (grade == 'A' or grade == 'B' or grade == 'C'){
                std::cout<<st[i].id<<" "<<st[i].name<<" "<<"P"<<"\n";
            } else{
                std::cout<<st[i].id<<" "<<st[i].name<<" "<<"NP"<<"\n";
            }
        }

        //std::cout<<st[i].id<<" "<<st[i].name<<" "<<st[i].grade[j]<<"\n";
    }



}