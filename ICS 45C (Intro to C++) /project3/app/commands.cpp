#include "commands.hpp"
//#include "HashMap.hpp"
#include <iostream>
#include <string>
#include <sstream>

//void HashMap::getCommands(){
//    std::string
//}

void Commands::Inputs(){
    std::string cmd;
    bool Flag = true;

    while (Flag == true){
        
        std::string cmd1 = "";
        std::string cmd2 = "";
        std::string cmd3 = "";
        std::getline(std::cin, cmd);
        std::istringstream line (cmd);
        //line << cmd;
        line >> cmd1;
        line >> cmd2;
        line >> cmd3;

        //std::cin>>cmd2>>cmd3;
        if (cmd1 == "CREATE"){
            if (cmd2 != "" && cmd3 != ""){
                Commands::create(cmd2, cmd3);
            } else{
                std::cout<<"INVALID"<<"\n";
            }
        } else if (cmd1 == "LOGIN" && cmd2 != "" && cmd3 != ""){
            Commands::login(cmd2, cmd3);
        } else if (cmd1 == "LOGIN" && cmd2 == "COUNT" && cmd3 == ""){
            Commands::loginCount();
        } else if (cmd1 == "REMOVE"){
            if (cmd2 != "" && cmd3 == ""){
                Commands::Remove(cmd2);
            } else {
                std::cout<<"INVALID"<<"\n";
            }
        } else if (cmd1 == "CLEAR" && cmd2 == "" && cmd3 == ""){
            //if (cmd2 == "" && cmd3 == ""){
                Commands::clear();
            //} else {
            //    std::cout<<"INVALID"<<"\n";
            //}
        } else if (cmd1 == "DEBUG"){
            //if (cmd2 != "" && cmd3 == ""){
            if ((cmd2 == "ON" || cmd2 == "OFF") && cmd3 == ""){
                Commands::debug(cmd2);
            } else {
                std::cout<<"INVALID"<<"\n";
            }
            //} else {
            //    std::cout<<"INVALID"<<"\n";
            //}
        } else if (cmd1 == "BUCKET"){
            if (cmd2 == "COUNT" && cmd3 == ""){
                Commands::BucketCount();
            } else {
                std::cout<<"INVALID"<<"\n";
            }
        } else if (cmd1 == "LOAD"){
            if (cmd2 == "FACTOR" && cmd3 == ""){
                Commands::LoadFactor();
            } else {
                std::cout<<"INVALID"<<"\n";
            }
        } else if (cmd1 == "MAX" && cmd2 == "BUCKET" && cmd3 == "SIZE"){
            Commands::MaxBucketSize();
        } else if (cmd1 == "QUIT" && cmd2 == "" && cmd3 == ""){
            Flag = false;
            std::cout<<"GOODBYE"<<"\n";
        } else {
            std::cout<<"INVALID"<<"\n";
        }
    }
}


Commands::Commands()
    :dbg{false}
{}

void Commands::create(const std::string& username, const std::string& password){
    if (hmap.contains(username) == false){
        hmap.add(username, password);
        std::cout<<"CREATED"<<"\n";
    } else{
        std::cout<<"EXISTS"<<"\n";
    }
}

void Commands::login(const std::string& username, const std::string& password){
    if (password == hmap.value(username)){
        std::cout<<"SUCCEEDED"<<"\n";
    } else{
        std::cout<<"FAILED"<<"\n";
    }
}

void Commands::Remove(const std::string& username){
    if (hmap.contains(username) == true){
        hmap.remove(username);
        std::cout<<"REMOVED"<<"\n";
    } else{
        std::cout<<"NONEXISTENT"<<"\n";
    }
}

void Commands::clear(){
    hmap.clearbuckets();
    std::cout<<"CLEARED"<<"\n";
}

void Commands::debug(const std::string& o_f){
    if (o_f == "ON" && dbg == false){
        dbg = true;
        std::cout<<"ON NOW"<<"\n";
    } else if (o_f == "ON" && dbg == true){
        std::cout<<"ON ALREADY"<<"\n";
    } else if (o_f == "OFF" && dbg == true){
        dbg = false;
        std::cout<<"OFF NOW"<<"\n";
    } else if (o_f == "OFF" && dbg == false){
        std::cout<<"OFF ALREADY"<<"\n";
    } else{
        std::cout<<"INVALID"<<"\n";
    }
}

void Commands::loginCount(){
    //std::cout<<dbg<<"\n";
    if (dbg == true){
        std::cout<<hmap.size()<<"\n";
    } else{
        std::cout<<"INVALID"<<"\n";
    }
}

void Commands::BucketCount(){
    if (dbg == true){
        std::cout<<hmap.bucketCount()<<"\n";
    } else{
        std::cout<<"INVALID"<<"\n";
    }
}

void Commands::LoadFactor(){
    if (dbg == true){
        std::cout<<hmap.loadFactor()<<"\n";
    } else{
        std::cout<<"INVALID"<<"\n";
    }
}

void Commands::MaxBucketSize(){
    if (dbg == true){
        std::cout<<hmap.maxBucketSize()<<"\n";
    } else{
        std::cout<<"INVALID"<<"\n";
    }
}