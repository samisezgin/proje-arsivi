#include "SortEngine.hpp"

int SleepTime = 500;
std::queue<std::vector<int>> InputQueue1, InputQueue2, InputQueue3;

void Observer();

void GenerateRandomVector();

int main() {
    Sort::SortEngine SortEngineObject1 = Sort::SortEngine(&InputQueue1, Sort::BUBBLE);
    Sort::SortEngine SortEngineObject2 = Sort::SortEngine(&InputQueue2, Sort::QUICK);
    Sort::SortEngine SortEngineObject3 = Sort::SortEngine(&InputQueue3, Sort::SELECTION);

    std::thread random_vector_thread(&GenerateRandomVector);
    std::thread observer_thread(&Observer);
    std::thread thread1(&Sort::SortEngine::Process, SortEngineObject1);
    std::thread thread2(&Sort::SortEngine::Process, SortEngineObject2);
    std::thread thread3(&Sort::SortEngine::Process, SortEngineObject3);


    thread3.join();
    thread2.join();
    thread1.join();
    observer_thread.join();
   random_vector_thread.join();
    return 0;
}

void Observer() {
    //...

    while (true) {
        if (InputQueue1.size() > 50 || InputQueue2.size() > 50 || InputQueue3.size() > 50) {
            SleepTime += 50;
            //std::cout << "SleepTime++";
        }
        if (InputQueue1.size() < 5 && InputQueue2.size() < 5 && InputQueue3.size() < 5 ) {
            SleepTime -= 50;
            //std::cout << "SleepTime--";
        }
        //std::cout << "Sleeping for 1000ms" << std::endl;

        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
}


void GenerateRandomVector() {

    while (true) {
        std::vector<int> vec;                           // create returning vector
        srand((unsigned)time(0));          // declaration of random seed

        for (int i = 0; i < 1000; ++i) {
            vec.push_back((rand() % 10000));            // getting random numbers
        }
        InputQueue1.push(vec);
        InputQueue2.push(vec);
        InputQueue3.push(vec);
        std::cout << "InputQ1Size: " << InputQueue1.size() << " InputQ1Empty?: " << InputQueue1.empty() << std::endl;
        std::cout << "InputQ2Size: " << InputQueue2.size() << " InputQ2Empty?: " << InputQueue2.empty() << std::endl;
        std::cout << "InputQ3Size: " << InputQueue3.size() << " InputQ3Empty?: " << InputQueue3.empty() << std::endl;
        std::cout << "Sleeping for " << SleepTime << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(SleepTime));
    }

}



