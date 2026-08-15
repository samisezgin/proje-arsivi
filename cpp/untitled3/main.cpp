#include <iostream>
#include <thread>
#include <chrono>
void threadFunc()
{
    int i = 0;
    while (true)
    {
        // Print Thread ID and Counter i
        std::cout<<std::this_thread::get_id()<<" :: "<<i++<<std::endl;
        // Sleep this thread for 200 MilliSeconds
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }
}
int main()
{
    std::thread th(&threadFunc);
    th.join();
    return 0;
}