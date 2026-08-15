import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class InterviewQuestions {

    public static void main(String[] args) {
        //List<Integer> list = new ArrayList<>();
//        for (int i = 0; i < 323_232_323; i++) {
//            list.add(0);
//            list.add(1);
//        }
//
//        list.sort(Integer::compare);
//
//        System.out.println("Count of zeros is " + countZeros(list));


        List<Integer> list = Arrays.asList(0, 0, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6);
        System.out.println(countOccurrences(list, 6)); // çıktısı: 4


    }

    public static int countZeros(List<Integer> list) {
        int low = 0, high = list.size() - 1;
        while (low <= high) {
            int mid = (low + high) / 2;
            if (list.get(mid) == 0) {
                low = mid + 1; // 1'ler daha sağda
            } else {
                high = mid - 1; // 1 bulundu, sola git
            }
        }
        return low; // low, ilk 1'in index'idir
    }


    public static int countOccurrences(List<Integer> list, int target) {
        int first = findFirst(list, target);
        if (first == -1) return 0; // hiç yoksa
        int last = findLast(list, target);
        return last - first + 1;
    }

    private static int findFirst(List<Integer> list, int target) {
        int low = 0, high = list.size() - 1, result = -1;
        while (low <= high) {
            int mid = (low + high) / 2;
            if (list.get(mid) == target) {
                result = mid;
                high = mid - 1; // sola git, daha erkeni var mı
            } else if (list.get(mid) < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return result;
    }

    private static int findLast(List<Integer> list, int target) {
        int low = 0, high = list.size() - 1, result = -1;
        while (low <= high) {
            int mid = (low + high) / 2;
            if (list.get(mid) == target) {
                result = mid;
                low = mid + 1; // sağa git, daha sonrakine bak
            } else if (list.get(mid) < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return result;
    }


}
