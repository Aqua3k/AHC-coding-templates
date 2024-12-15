#ifndef HEADER_SIMULATED_ANNEALING
#define HEADER_SIMULATED_ANNEALING

#include <stdint.h>
#include <iostream>
#include <tuple>

#include "type_defines.hpp"

using namespace std;

template <typename Status, typename Score, typename Diff>

class SimulatedaAnnealingTemplate {
private:
    Status initial_status;
    Score initial_score;

public:
    SimulatedaAnnealingTemplate(
        Status initial_status,
        Score initial_score
        ): initial_status(initial_status), initial_score(initial_score) {}

    virtual bool should_terminate() {
        return true;
    }

    Status optimize(double temperature, double rate) {
        
    }

    virtual tuple<Diff, Score> dry_run() {}

    virtual Status operate(Status status, Diff diff) {}

};

#endif // HEADER_SIMULATED_ANNEALING
