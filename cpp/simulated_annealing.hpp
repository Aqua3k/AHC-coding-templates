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
        auto score = initial_score;
        auto best_score = score;

        auto status = initial_status;
        auto best_status = status;

        while(!should_terminate()) {
            auto result = dry_run();   
            auto diff = get<0>(result);
            auto new_score = get<1>(result);
            auto t = (score - new_score) / temperature;
            bool swap = true;
            if (t < 1.0) {
                swap = static_cast<double>(rand()) / RAND_MAX < exp(t);
            }

            if (swap) {
                auto status = oeprate(status, diff);
                score = new_score;
                if (score < best_score) {
                    best_score = score;
                    best_status = status;
                }
            }
            temperature *= rate;
        }
        return best_status;
    }

    virtual tuple<Diff, Score> dry_run() {}

    virtual Status operate(Status status, Diff diff) {}

};

#endif // HEADER_SIMULATED_ANNEALING
