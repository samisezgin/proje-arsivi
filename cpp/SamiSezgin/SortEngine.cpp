#include "SortEngine.hpp"

using namespace Sort;

SortEngine::SortEngine(std::queue <std::vector<int>> *inputQueue, SORT_TYPE sortType):mInputQueue(inputQueue),mSortType(sortType) {}

void SortEngine::Process() {
    while (true) {
            //std::cout<<"Input Queue Empty?: "<<mInputQueue.empty()<<std::endl;
            if (!mInputQueue->empty()) {
                std::vector<int> inputVector = mInputQueue->front();
                //std::cout<<"process_input_vector_size: "<<inputVector.size()<<std::endl;
                mInputQueue->pop();
                switch (mSortType) {
                    case BUBBLE:
                        //std::cout << "Bubble Sort" << std::endl;
                        BubbleSort(inputVector);
                        break;
                    case QUICK:
                        //std::cout << "Quick Sort" << std::endl;
                        QuickSort(inputVector, 0, inputVector.size()-1);
                        break;
                    case SELECTION:
                        //std::cout << "Selection Sort" << std::endl;
                        SelectionSort(inputVector);
                        break;
                    default:
                        //std::cout << "Not available" << std::endl;
                        break;
                }
            } /*else {
                std::cout << "Queue is empty, passing this lap." << std::endl;
            }*/
        }

    ///
}

std::vector<int> Sort::SortEngine::BubbleSort(std::vector<int> inputVector) {
    ///
    bool swap = true;
    while (swap) {
        swap = false;
        for (size_t i = 0; i < inputVector.size() - 1; i++) {
            if (inputVector[i] > inputVector[i + 1]) {
                inputVector[i] += inputVector[i + 1];
                inputVector[i + 1] = inputVector[i] - inputVector[i + 1];
                inputVector[i] -= inputVector[i + 1];
                swap = true;
            }
        }
    }

    return inputVector;
}

std::vector<int> Sort::SortEngine::QuickSort(std::vector<int> &inputVector, int left, int right) {

    if(left < right) {
        int pivotIndex = Partition(inputVector, left, right);
        Sort::SortEngine::QuickSort(inputVector, left, pivotIndex-1);
        Sort::SortEngine::QuickSort(inputVector, pivotIndex, right);
    }
    return inputVector;
}

std::vector<int> Sort::SortEngine::SelectionSort(std::vector<int> inputVector)
{
    auto itr = inputVector.begin();
    while(itr != inputVector.end())
    {
        auto itr_min = itr;
        for(auto i = itr + 1; i != inputVector.end(); i++)
        {
            if(*i < *itr_min)
            {
                itr_min = i;
            }
        }
        std::iter_swap(itr, itr_min);
        itr++;
    }
    return inputVector;
}

int SortEngine::Partition(std::vector<int> &inputVector, int left, int right) {
    int pivotIndex = left + (right - left) / 2;
    int pivotValue = inputVector[pivotIndex];
    int i = left, j = right;
    int temp;
    while(i <= j) {
        while(inputVector[i] < pivotValue) {
            i++;
        }
        while(inputVector[j] > pivotValue) {
            j--;
        }
        if(i <= j) {
            temp = inputVector[i];
            inputVector[i] = inputVector[j];
            inputVector[j] = temp;
            i++;
            j--;
        }
    }
    return i;
}