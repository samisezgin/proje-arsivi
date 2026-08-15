#include <iostream>
#include <thread>
#include <chrono>
#include "SortEngine.hpp"

using namespace Sort;

/**
 * @constructor
 * @param inputQueue, sortType
 */
SortEngine::SortEngine(std::queue<std::vector<int>> &inputQueue, SORT_TYPE sortType)
    : mInputQueue(&inputQueue), mSortType(sortType) {}

/**
 * This function handles the vectors coming from RandomVectorGenerator. Gets vectors in the queue and sorts the values of the vector in ascending order.
 * If no vector available in the queue waits until a new vector comes.
 */
void SortEngine::Process()
{
    while (true)
    {
#if N_DEBUG
        auto start = std::chrono::high_resolution_clock::now();
#endif
        std::lock_guard<std::mutex> process_lock(input_queue_mutex); /** Lock the mutex for data protection from other threads, it automatically unlocks at the end of the block. */
        try
        {
            if (!mInputQueue->empty())
            {
                std::vector<int> &inputVector{mInputQueue->front()};
#if N_DEBUG
                std::cout << "BEFORE SORT" << std::endl;

                for (const int data : inputVector)
                {
                    std::cout << data << ",";
                }
                std::cout << "\n";
#endif
                switch (mSortType)
                {
                case SORT_TYPE::BUBBLE:
                    BubbleSort(inputVector);
                    break;
                case SORT_TYPE::QUICK:
                    QuickSort(inputVector, 0, inputVector.size() - 1);
                    break;
                case SORT_TYPE::SELECTION:
                    SelectionSort(inputVector);
                    break;
                default:
                    break;
                }
#if N_DEBUG
                std::cout << "\nAFTER SORT :" << static_cast<int>(mSortType) << std::endl;
                for (const int data : inputVector)
                {
                    std::cout << data << ",";
                }
                std::cout << "\n";
#endif
                mInputQueue->pop();
            }
        }
        catch (std::exception &exc)
        {
            std::cerr << exc.what() << std::endl;
        }
        catch (...)
        {
            std::cerr << "Unknown Exception" << std::endl;
        }

#if N_DEBUG
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "Process completed in: " << duration.count() << " microseconds" << std::endl;
#endif
    }
}
/**
 *
 * @param inputVector
 * @return
 */
std::vector<int> Sort::SortEngine::BubbleSort(std::vector<int> &inputVector)
{
    bool swap = true;
    while (swap)
    {
        swap = false;
        for (size_t i = 0; i < inputVector.size() - 1; i++)
        {
            if (inputVector[i] > inputVector[i + 1])
            {
                inputVector[i] += inputVector[i + 1];
                inputVector[i + 1] = inputVector[i] - inputVector[i + 1];
                inputVector[i] -= inputVector[i + 1];
                swap = true;
            }
        }
    }

    return inputVector;
}
/**
 *
 * @param inputVector
 * @param left
 * @param right
 * @return
 */
std::vector<int> Sort::SortEngine::QuickSort(std::vector<int> &inputVector, int left, int right)
{

    if (left < right)
    {
        int pivotIndex = Partition(inputVector, left, right);
        Sort::SortEngine::QuickSort(inputVector, left, pivotIndex - 1);
        Sort::SortEngine::QuickSort(inputVector, pivotIndex, right);
    }
    return inputVector;
}
/**
 *
 * @param inputVector
 * @return
 */
std::vector<int> Sort::SortEngine::SelectionSort(std::vector<int> &inputVector)
{
    auto itr = inputVector.begin();
    while (itr != inputVector.end())
    {
        auto itr_min = itr;
        for (auto i = itr + 1; i != inputVector.end(); i++)
        {
            if (*i < *itr_min)
            {
                itr_min = i;
            }
        }
        std::iter_swap(itr, itr_min);
        itr++;
    }
    return inputVector;
}
/**
 *
 * @param inputVector
 * @param left
 * @param right
 * @return
 */
int SortEngine::Partition(std::vector<int> &inputVector, int left, int right)
{
    int pivotIndex = left + (right - left) / 2;
    int pivotValue = inputVector[pivotIndex];
    int i = left, j = right;
    int temp;
    while (i <= j)
    {
        while (inputVector[i] < pivotValue)
        {
            i++;
        }
        while (inputVector[j] > pivotValue)
        {
            j--;
        }
        if (i <= j)
        {
            temp = inputVector[i];
            inputVector[i] = inputVector[j];
            inputVector[j] = temp;
            i++;
            j--;
        }
    }
    return i;
}