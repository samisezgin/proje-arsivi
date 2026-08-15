#pragma once
#include <queue>
#include <vector>
#include <mutex>

#define N_DEBUG 0 /** DEBUG OPTION - IF OPENED, PRINTS QUEUE SIZES, PROCESS TIMES, BEFORE AND AFTER PROCESS VECTORS*/

namespace Sort
{
	enum class SORT_TYPE : uint8_t
	{
		BUBBLE = 0u,
		QUICK = 1u,
		SELECTION = 2u
	};

	class SortEngine
	{
	public:
		SortEngine(std::queue<std::vector<int>> &inputQueue, SORT_TYPE sortType);
		void Process();

	private:
		SORT_TYPE mSortType;
		std::queue<std::vector<int>> *mInputQueue;

		static std::vector<int> BubbleSort(std::vector<int> &inputVector);
		static std::vector<int> QuickSort(std::vector<int> &inputVector, int left, int right);
		static std::vector<int> SelectionSort(std::vector<int> &inputVector);
		static int Partition(std::vector<int> &values, int left, int right);
	};
};
inline std::mutex input_queue_mutex; /** One time definition for the mutex object */