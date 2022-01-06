#ifndef STUDENTS_HPP
#define STUDENTS_HPP
#include <string>


struct Student {
    int id;
    char opt;
    std::string name;
    double score = 0.0;
    //char* grade = new char[3]
    //char g1 = 'F';
    //char g2 = 'F';
    //char g3 = 'F';
};

#endif