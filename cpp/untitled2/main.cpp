#include <iostream>
#include <thread>
#include "SortEngine.hpp"

/**
 * @variable SleepTime Value for thread to sleep
 */
int SleepTime = 500;

std::queue<std::vector<int>> InputQueue1, InputQueue2, InputQueue3;

void Observer(int overload_threshold, int underload_threshold);

void GenerateRandomVector(int amount);

int main(int argc, char **argv)
{
    /** SortEngine objects with different sorting algorithms inside.*/
    Sort::SortEngine SortEngineObject1(InputQueue1, Sort::SORT_TYPE::BUBBLE);
    Sort::SortEngine SortEngineObject2(InputQueue2, Sort::SORT_TYPE::QUICK);
    Sort::SortEngine SortEngineObject3(InputQueue3, Sort::SORT_TYPE::SELECTION);

    /**
     * If threads could not be started, they throw std::system_error.
     * If threads can not join, they throw std::system_error.
     * We need to catch it to handle.
     */
    try
    {
        std::thread random_vector_thread(&GenerateRandomVector, 1000);
        std::thread observer_thread(&Observer, 50, 5);

        std::thread thread1(&Sort::SortEngine::Process, SortEngineObject1);
        std::thread thread2(&Sort::SortEngine::Process, SortEngineObject2);
        std::thread thread3(&Sort::SortEngine::Process, SortEngineObject3);

        thread3.join();
        thread2.join();
        thread1.join();
        observer_thread.join();
        random_vector_thread.join();
    }
    catch (std::exception &exc)
    {
        std::cerr << exc.what() << std::endl;
    }
    catch (...)
    {
        std::cerr << "Unknown exception" << std::endl;
    }
    return 0;
}

/**
 * This function observes the queues for overloading. 
 * If any of queue's size is greater than overload threshold (in this case = 50), observer slows down the vector generator. 
 * If all of queue's size are less than underload threshold (in this case = 5), observer speeds up the vector generator.
 * @param overload_threshold
 * @param underload_threshold
 */
void Observer(int overload_threshold = 50, int underload_threshold = 5)
{

    while (true)
    {
        input_queue_mutex.lock(); /** Lock the mutex for data protection from other threads. */
        if (InputQueue1.size() > overload_threshold || InputQueue2.size() > overload_threshold ||
            InputQueue3.size() > overload_threshold)
        {
            SleepTime += 50;
        }
        else if (InputQueue1.size() < underload_threshold && InputQueue2.size() < underload_threshold &&
                 InputQueue3.size() < underload_threshold && SleepTime > 75)
        {
            SleepTime -= 50;
        }
        input_queue_mutex.unlock(); /** Unlock the mutex */
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
}

/**
 * Generates vectors contain the determined amount of numbers.
 * @param amount Amount of numbers to be added to the vector.
 */
void GenerateRandomVector(int amount = 1000)
{

    while (true)
    {
        std::vector<int> vec;     /** create returning vector */
        srand((unsigned)time(0)); /** declaration of random seed */

        for (int i = 0; i < amount; ++i)
        {
            vec.emplace_back((rand() % 10000)); /** getting random numbers */
        }

        input_queue_mutex.lock();
        InputQueue1.push(vec);
        InputQueue2.push(vec);
        InputQueue3.push(vec);

#if N_DEBUG
        std::cout << " (InputQ1Size: " << InputQueue1.size(); /** DEBUG */
        std::cout << " InputQ2Size: " << InputQueue2.size();  /** DEBUG */
        std::cout << " InputQ3Size: " << InputQueue3.size();  /** DEBUG */
        std::cout << " Sleeping for " << SleepTime << ") \n"
                  << std::endl; /** DEBUG */
#endif
        input_queue_mutex.unlock();
        std::this_thread::sleep_for(std::chrono::milliseconds(SleepTime));
    }
}
