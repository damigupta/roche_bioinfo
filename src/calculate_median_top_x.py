# TODO handle duplicate coverage values and other edge cases

class Solution:
    median_index=0
    is_odd=True

    def set_median_index(self,arr_len):
        # calculate index of median value

        if not self.median_index:
            if arr_len % 2 == 1:  # Odd length
                self.is_odd=True
                self.median_index = arr_len // 2
            else:  # Even length
                self.is_odd = False
                self.median_index = arr_len// 2 - 1

    def get_median(self, file):
        # size of list of maximal items
        chunk=2

        num_removed = 0
        num_items=0
        
        # get the number of lines in the file
        with open(file) as f:
            for _ in f:
                num_items +=1


        pivot=float('inf')
        self.set_median_index(num_items)

        # TODO handle chunk size if it is greater than than num_items
        
        while True:
            # read file
            with open(file) as f:
                # array which will hold a list of maximal items
                largest = []
                # TODO handle chunk size - the maximal array should not contain any values less than the median
                for line in f:
                    coverage = int(line.strip())

                    # minimum value in maximal list
                    if coverage < pivot:
                        if largest:
                            min_largest=min(largest)
                        else:
                            min_largest=0

                        # logic to maintain the array of top x(chunk) items in the data
                        if len(largest) < chunk or coverage >= min_largest:
                            if len(largest) > chunk-1:
                                largest.sort()
                                if len(largest) > 1 and not coverage in largest:
                                    largest.remove(largest[0])
                            largest.append(coverage)
                            largest.sort()

            num_removed += len(largest)
            if self.is_odd:
                if num_removed == self.median_index + 1:
                    # TODO index might not be 0 if there are duplicate values
                    median = largest[0]
                    print(f"Median is {median}")
                    break
            else:
                if num_removed == self.median_index + 2:
                    # TODO index might not be 0 if there are duplicate values
                    median = (largest[0] + largest[1]) / 2
                    print(f"Median is {median}")
                    break
            # for the next iteration, only consider items less than those in this maximal array
            pivot = min(largest)


if __name__ == '__main__':
    filename= "../data/sample_1.txt"
    sln=Solution()
    sln.get_median(filename)

