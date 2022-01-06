#include <string>
#include "HashMap.hpp"

namespace {

    int myHashFunc(const std::string& strng){
        int ssize = strng.size();
        int mul = 31;
        int hashed = 0;

        for (int i = 0; i<ssize; i++){
            hashed = mul*hashed + strng[i];
        }
        return hashed;
    }

}

HashMap::HashMap()
    : hashFunction{myHashFunc}, BucketSize{HashMap::INITIAL_BUCKET_COUNT}, buckets{new Node* [HashMap::INITIAL_BUCKET_COUNT]}
{
    HashMap::NULLBuckets();
}

HashMap::HashMap(HashFunction hashFunction)
    : hashFunction{hashFunction}, BucketSize{HashMap::INITIAL_BUCKET_COUNT}, buckets{new Node* [HashMap::INITIAL_BUCKET_COUNT]}
{
    HashMap::NULLBuckets();
}

HashMap::HashMap(const HashMap& hm)
    : hashFunction{hm.hashFunction}, BucketSize{hm.BucketSize}, buckets{new Node* [hm.BucketSize]}
{
    HashMap::c_bucket(hm.buckets, hm.BucketSize);
}    

HashMap::~HashMap(){
    HashMap::DeleteBuckets();
}

HashMap& HashMap::operator=(const HashMap& hm){
    if (this != &hm){
        HashMap::DeleteBuckets();
        hashFunction = hm.hashFunction;
        BucketSize = hm.BucketSize;
        buckets = new Node*[hm.BucketSize];
        HashMap::c_bucket(hm.buckets, hm.BucketSize);
    }

    return *this;
}

void HashMap::add(const std::string& key, const std::string& value){
    if (HashMap::contains(key) != true){
        HashMap::AddNode(key, value);
    } else{
        return;
    }

    if (HashMap::loadFactor() > 0.8){
        int tempsize = BucketSize;
        Node** tempbucket = buckets;
        BucketSize = 2*BucketSize + 1;
        buckets = new Node* [BucketSize];
        HashMap::NULLBuckets();

        for (int i = 0; i<tempsize; i++){
            Node* current = tempbucket[i];
            while (current != nullptr){
                HashMap::AddNode(current -> key, current -> value);
                current = current -> next;
            }
        }

        for (int i = 0; i<tempsize; i++){
            if (tempbucket[i] != nullptr){
                HashMap::DeleteNode(tempbucket[i]);
            }
        }

        delete[] tempbucket;

    }
}

bool HashMap::remove(const std::string& key){
    if (HashMap::contains(key) == true){
        int index = hashFunction(key) % BucketSize;
        Node* last = buckets[index];
        Node* current = last -> next;

        if (key != last -> key){
            while (key != current -> key){
                last = current;
                current = last -> next;
            }
            last -> next = current -> next;
            delete current;
        } else{
            buckets[index] = current;
            delete last;
        }
        return true;


    } else{
        return false;
    }
}

bool HashMap::contains(const std::string& key) const{
    int index = hashFunction(key) % BucketSize;
    Node* nd = buckets[index];

    while (nd != nullptr){
        if (key == nd -> key){
            return true;
        }
        nd = nd -> next;
    }
    return false;
}

std::string HashMap::value(const std::string& key) const{
    if (HashMap::contains(key) == true){
        int index = hashFunction(key) % BucketSize;
        Node* nd = buckets[index];

        while (key != nd -> key){
            nd = nd -> next;
        }
        return nd -> value;
    } else{
        return "";
    }
}

unsigned int HashMap::size() const{
    int mapsize = 0;
    for (int i = 0; i<BucketSize; i++){
        if (buckets[i] != nullptr){
            mapsize = mapsize + HashMap::NodeCount(buckets[i]);
        }
    }
    return mapsize;
}

unsigned int HashMap::bucketCount() const{
    int num = 0;
    for (int i = 0; i<BucketSize; i++){
        if (buckets[i] != nullptr){
            num += 1;
        }
    }
    return num;
}

double HashMap::loadFactor() const{
    double lf = (double)HashMap::size()/BucketSize;
    return lf;
}

unsigned int HashMap::maxBucketSize() const{
    int max = 0;
    for (int i = 0; i<BucketSize; i++){
        if (buckets[i] != nullptr){
            if (HashMap::NodeCount(buckets[i]) > max){
                max = HashMap::NodeCount(buckets[i]);
            }
        }
    }
    return max;
}

void HashMap::clearbuckets(){
    HashMap::DeleteBuckets();
    buckets = new Node* [BucketSize];
    HashMap::NULLBuckets();
}

void HashMap::AddNode(const std::string& key, const std::string& value){
    int index = hashFunction(key) % BucketSize;
    if (buckets[index] != nullptr){
        Node* nd = buckets[index];
        while (nd -> next != nullptr){
            nd = nd -> next;
        }
        nd -> next = new Node{key, value, nullptr};
    } else{
        buckets[index] = new Node{key, value, nullptr};
    }
}

void HashMap::DeleteNode(Node* nod){
    while (nod -> next != nullptr){
        nod = nod -> next;
    }
    delete nod;
}

const int HashMap::NodeCount(const Node* nod) const{
    int c = 1;
    while (nod -> next != nullptr){
        c += 1;
        nod = nod -> next;
    }
    return c;
}

void HashMap::c_bucket(Node** nod, unsigned int size){
    HashMap::NULLBuckets();
    for (int i = 0; i<BucketSize; i++){
        if (nod[i] != nullptr){
            Node* newnode = nod[i];
            buckets[i] = new Node{newnode -> key, newnode -> value, nullptr};
            Node* reach = buckets[i];
            newnode = newnode -> next;
            
            while(newnode != nullptr){
                reach -> next = new Node{newnode -> key, newnode -> value, nullptr};
                reach = reach -> next;
                newnode = newnode -> next;

            }
        }
    }
}

void HashMap::NULLBuckets(){
    for (int i = 0; i<BucketSize; i++){
        buckets[i] = nullptr;
    }
}

void HashMap::DeleteBuckets(){
    for (int i = 0; i<BucketSize; i++){
        if (buckets[i] != nullptr){
            HashMap::DeleteNode(buckets[i]);
        }
    }
    delete[] buckets;
}

int HashMap::BucketsCount(){
    int c = 0;
    for (int i = 0; i<BucketSize; i++){
        if (buckets[i] != nullptr){
            c = c + HashMap::NodeCount(buckets[i]);
        }
    }
    return c;
}

