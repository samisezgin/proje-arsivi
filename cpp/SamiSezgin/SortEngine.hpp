#include <queue>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <array>
#include <thread>
//#include <unistd.h>
namespace Sort
{
	enum SORT_TYPE { BUBBLE = 0, QUICK = 1, SELECTION = 2 };
	class SortEngine
	{
	public:
		SortEngine(std::queue<std::vector<int>> *inputQueue, SORT_TYPE sortType);
		void Process();
	private:
		std::vector<int> BubbleSort(std::vector<int> inputVector);
		std::vector<int> QuickSort(std::vector<int> &inputVector,int left,int right);
        std::vector<int> SelectionSort(std::vector<int> inputVector);

		SORT_TYPE mSortType;
		std::queue<std::vector<int>> *mInputQueue;
		static int Partition(std::vector<int> &values, int left, int right);
	};
}