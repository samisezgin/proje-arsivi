/*
 *                  Sami Sezgin
 *                  13.08.2021
 *                  RESULTS:
 *                  13 18 12 17 1 11 0 11 2 18
 *                  13 1 12 0 7 0 11 4 15 5
 *
 *
 */

#include <cstdlib>
#include <ctime>
#include <iostream>
#include <array>

template <int size_>
std::array<int , size_> genRand(int range)
{
    std::array<int , size_> arr;                    // create returning array
    srand((unsigned)time(0));           // declaration of random seed
    arr[0] = (rand() % range);                      // getting first random number
    for(int i = 1 ; i < size_ ; ++i)
    {
        do{
            arr[i] = (rand() % range);              // getting next random numbers
        }while( abs(arr[i - 1] - arr[i]) < 5);  // condition of the question
    }
    return arr;
}

int main() {
    auto result = genRand<10>(20);      // passing value of size

    for(int r : result)
        std::cout << r << " ";                // printing out the array

    return 0;
}