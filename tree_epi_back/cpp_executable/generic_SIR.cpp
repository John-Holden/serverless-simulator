// SIR model re-written in cpp
#include <iostream>
#include <sstream>
#include <string>
#include "SIR.h"

using namespace std; // use all std object names etc. 

// Class holding one public function
class Simulation{
    // one pubic function to execute a simulation
    public: int ExecuteRun(int a){
            std::ostringstream oss; // 
            oss << "sometext 1 " << a << " some text 2";
            std::string var_out = oss.str();
            std::cout << var_out  << std::endl;
            inHeaderFileFunct("input text from main");
            return 0;
        }
};

extern "C" {
    Simulation* newSimOjb(){ return new Simulation(); }
    int execute(Simulation* simulation, int a){ return simulation->ExecuteRun(a); }
    }
