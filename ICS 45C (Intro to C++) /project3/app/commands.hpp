#ifndef COMMANDS_HPP
#define COMMANDS_HPP

#include <iostream>
#include <string>
#include "HashMap.hpp"

class Commands
{
    public:

        Commands();
        void Inputs();

    private:

        HashMap hmap;
        bool dbg;
        void create(const std::string& username, const std::string& password);
        void login(const std::string& username, const std::string& password);
        void Remove(const std::string& username);
        void clear();
        void debug(const std::string& o_f);
        void loginCount();
        void BucketCount();
        void LoadFactor();
        void MaxBucketSize();

};

#endif
