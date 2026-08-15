#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cassert>
#include <cmath>

bool isPrime(int n) {
    // Corner case
    if (n <= 1)
        return false;

    // Check from 2 to n/2
    for (int i = 2; i <= n / 2; i++)
        if (n % i == 0)
            return false;

    return true;
}

int maximumHeight(int n) {
    int result = 1;
    for (int i = 1; i <= n; ++i) {

        // Just checking whether ith level
        // is possible or not if possible
        // then we must have atleast
        // (i*(i+1))/2 elements in the
        // array
        long long y = (i * (i + 1)) / 2;

        // updating the result value
        // each time
        if (y <= n)
            result = i;

            // otherwise we have exceeded n value
        else
            break;
    }
    return result;
}

void triangle2(std::vector<int> *data, int n) {
    // Number of spaces
    int i, j, k = n;
    int start = 0;
    // Outer loop to handle number of rows
    // n in this case
    for (i = 1; i <= n; i++) {

        // Inner loop for columns
        for (j = 1; j <= n; j++) {

            // Condition to print star pattern
            if (j >= k) {
                std::cout << data->at(start) << " ";
                ++start;
            } else
                std::cout << "  ";
        }
        k--;
        std::cout << "\n";
    }
}

void removePrimeNumbers(std::vector<int> &data, int n) {
    for (int i = 0; i < data.size(); ++i) {
        if (isPrime(data.at(i))) { data[i] = -1; }
    }
}

void triangle(std::vector<int> *data, int n) {
    // number of spaces
    int k = 2 * n - 2;
    int start = 0;
    // Outer loop to handle number of rows
    // n in this case
    for (int i = 0; i < n; i++) {

        // Inner loop to handle number of columns
        // values changing acc. to outer loop
        for (int j = 0; j <= i; j++) {
            // Printing stars
            std::cout << data->at(start) << "\t";
            ++start;
        }

        // Ending line after each row
        std::cout << std::endl;
    }
}

int main() {
    std::ifstream fin("input_file33.txt");
    int rows;
    std::vector<int> data, result, temp;
    int element;
    while (fin >> element) {
        data.push_back(element);
        temp.push_back(element);
    }

    removePrimeNumbers(data, data.size());  // assigning -1 to prime numbers for eliminating them in the vector.
    rows = maximumHeight(data.size());         // finding row count for the input file

    std::cout<<"-----PYRAMID BEFORE OPERATION-----"<<std::endl;
    triangle(&data, rows);                      // before calculating max sum, print the pyramid.
    std::cout << std::endl;

    const int size = data.size();               // check if given input can be shaped as pyramid.
    const int tn = static_cast<int>(sqrt(2.0 * size));
    assert(tn * (tn + 1) == 2 * size);          // size should be a triangular number

    // walk backward by rows, replacing each element with max attainable therefrom
    for (int n = tn - 1; n > 0; --n) {   // n is size of row, note we do not process last row
        for (int k = (n * (n - 1)) / 2; k < (n * (n + 1)) / 2; ++k) { // from the start to the end of row
            if ((data[k + n] == -1 && data[k + n + 1] == -1))
                data[k] = -1;
            else if (data[k] != -1 && (data[k + n] != -1 || data[k + n + 1] != -1)) {
                data[k] += std::max(data[k + n], data[k + n + 1]);
            }
        }
    }


    std::cout<<"-----PYRAMID AFTER OPERATION-----"<<std::endl;
    triangle(&data, rows);          // after calculating max sum, print the pyramid.

    std::cout << "-----Maximum total: " << data[0] << "-----\n\n"; //print the maximum sum of given pyramid

    return 0;
}

