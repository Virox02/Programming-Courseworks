#include <iostream>

int main(){
    int n;
    std::cin>>n;
    for (int i=1; i<=n; i++){
        for (int s=0; s<(2*n)+1; s++){
            if (s<n-i){
                std::cout<<" ";
                }
            else if(s==n-i){
                while (s<=n+i){
                    std::cout<<"*";
                    s++;
                    }
                }
            }
        std::cout<<"\n";
        int c=0;
        for (int s=0; s<(2*n)+1; s++){
             if (s<n-i){
                std::cout<<" ";
                }
             else if(s<=n+i){
                c++;
                if (c%2==0){
                    std::cout<<" ";
                    }
                else{
                    std::cout<<"*";
                    }
                }
            }
        std::cout<<"\n";
    }
    for (int s=0; s<(2*n)+1; s++){
        std::cout<<"*";
        }
    std::cout<<"\n";

}
