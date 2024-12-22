#ifndef HEADER_TIMER
#define HEADER_TIMER

#include <map>
#include <ctime>
#include <iostream>

#include "type_defines.hpp"

using namespace std;

class Timer {
private:
    static map<u32, clock_t> stop_watch;
    static map<u32, clock_t> timers;
    static clock_t start_time;
public:

    static void initialize() {
        start_time = clock();
    }
    static f32 get_elapsed_time() {
        return static_cast<f32>(clock() - start_time) / CLOCKS_PER_SEC;
    }
    static void start(u32 channel) {
        stop_watch[channel] = clock();
    }
    static f32 stop(u32 channel) {
        clock_t count = clock() - stop_watch[channel];
        timers[channel] += count;
        return static_cast<f32>(count) / CLOCKS_PER_SEC;
    }
    static void show() {
        for (auto it = timers.begin(); it != timers.end(); ++it) {
            cerr << "Channel: " << it->first << endl;
            cerr << "Time   : " << static_cast<f32>(it->second) / CLOCKS_PER_SEC << endl;
            cerr << "" << endl;
        }
    }
};

map<u32, clock_t> Timer::stop_watch;
map<u32, clock_t> Timer::timers;
clock_t Timer::start_time = 0;

#endif // HEADER_TIMER
