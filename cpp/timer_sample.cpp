#include <iostream>
#include <chrono>
#include <thread>

#include "timer.hpp"

using namespace std;

void wait_1sec() {
    this_thread::sleep_for(chrono::seconds(1));
}

void do_nothing() {
    volatile u8 foo;
    foo = 1;
}

int main() {
    Timer::initialize();
    atexit(Timer::show);

    for (u8 i = 0; i < 3; i++) {
        Timer::start(1);
        wait_1sec();
        Timer::stop(1);

        Timer::start(2);
        do_nothing();
        Timer::stop(2);
    }
    return 0;
}
