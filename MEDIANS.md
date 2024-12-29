# Introduction
Given a sample coverage file for the entire human genome, calculate the median coverage value.
It is assumed that the coverage is per-base, and there is only coverage value for each base.

## Sample input file
```
# sample_1.txt
12
73
48
18
94
112
...
```

## Methodology
Consider `num_items` number of data items. There are several ways of obtaining the median from this dataset.
1. The data can be loaded into memory and sorted to create a list data structure. 
Then get the item at index ~ `num_items/2`. 
2. Quickselect is a more performant way to determine the `kth` smallest value in a dataset. But this involves 
storing data in partitions, which takes up a lot of memory.

Both of these are memory-intensive. Since there are 3.2G data points, these solutions may not work (depending on 
how much memory is available).

There are alternative approaches e.g.
1. Keep a smaller amount of data in memory at a time. Then there are algorithms which involve parsing the coverage
file multiple times to arrive at the median value. Because of these multiple iterations, 
the time complexity will be larger.
2. Do an external merge sort. This involves splitting the data into multiple files on the disk. 
Sort the data in each file. Then use a divide-and-conquer algorithm to get the median(e.g. a k-way merge). 
This will require disk space for storage, and multiple read/writes to the disk. 
3. If you have access to multiple servers, tasks can be split across these, with some merge algorithm at the end.

A combination of these can be used. You have to balance for
- Time Complexity
- Amount of data held in memory at a time
- Disk Storage space
- Overhead for read/writes

The following are an outline of some ways to solve the problem.

**Example 1:**
Parse the coverage file, and track variables - `num_items`, `min`, `max`. 
You can also calculate the median index from this.
1. Choose a value considerably smaller than `num_items`, say `100`. 
2. Now, consider buckets as `min ... min+100, min+101 ... min+200` etc. There will be a sub-file for each bucket. 
There will be `num_items/100` files. Each file has at most `100` items.
3. Parse the file again. For each item, determine which bucket it should be in, and write it to the corresponding file.
4. Sort the data in each file. 
5. Iterate across values in the sorted files in order. You have the median index, so you know when that index location
is reached.
Alternatively you could track the number of items in each file. So you can calculate the file in which the median will 
be present, and iterate over the items in just that file until you reach the median index.

This approach works best for data which approximates a normal distribution. Else file sizes will vary.


**Example 2:**
1. Pick a chunk size , say `10 Mb`. 
2. Parse the coverage file, and split the data into `k` sub-files each with `10 Mb` data. While parsing, record `num_items`.
You can calculate the median index from this.
3. Sort each file. 
4. Now the files need to be merged in a sorted fashion. There are several ways of doing this.
E.g. Get the smallest value from each of the sub-files at a time. So each time you parse, you have `k` values. 
Determine the smallest item in these `k` values, and pop that value from the file it came from.
5. Repeat this till the number of items popped is equal to the median index, which gives you the median value.

**Example 3:**
This is a combination of median-of-medians and partitioning.
In the below, you are calculating the median on a smaller numbers of items. You can use either sorting, or quickselect.
1. Parse the coverage file, and split it into `x` sub-files, each with at most `n` items.
2. For each sub-file, determine it's median.
3. Use the median from each sub-file to create a list of medians.
4. Calculate the median of this list. This is an 'approximate median (say `ap`)' - a good guess for a median value.
5. Parse the file again, and create 2 sub-files(say `f1` and `f2`) from it. File `f1` will contain values <= `ap`,
and file `f2` has values > `ap`.
6. The files have `n1`, and `n2` numbers of items.
  - If `n1` is equal to the median index, you are done. 
  - If `n1` is greater than the median index, then for the next step, you will use the file `f1`. 
  - Else you will use file `f2`. Note that instead of median index, you will be looking for the (`median index - n1`)th item. 
  - Repeat steps 1-6 until you locate the median.

**Example 4:**
This will use a list `l` of the largest `x` items in the dataset.
1. Parse the coverage file while updating `l`.
2. The smallest item in `l` is the `x` largest element in the dataset, say `pivot`.
3. Create a new `l`. Parse again, this time the items in `l` have to be less than `pivot`
4. Continue until the numbers of items dropped have reached the median index.

I have included a pseudocode implementation of this. It is incomplete, and will not run, but it gives a rough idea
of an implementation. (See [code](./src/calculate_median_top_x.py) here)





