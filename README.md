#Finding Frequent Item sets

In this Project there is implementation of 3 different algorithms to find frequent item-sets namely <strong>Park-Chen-Yu (PCY), Multi-Stage hashing and Toivonen</strong>. The transactions will be given as an input file-<em>input.txt</em>.

###Problem 1: PCY Algorithm and Execution

Implementing PCY algorithm using a single hash and print all frequent item sets. Each letter(alphabet) is assigned a value. The hash function calculates the sum of the values for pairs and so on and takes the mod with respect to the bucket size.

<strong>Input Parameters:</strong>

1. <em>Input.txt</em>: This is the input file containing all transactions. Each line corresponds to a transaction. Each transaction has items that are comma separated. 

2. <em>Support</em>: Integer that defines the minimum count to qualify as a frequent itemset.

3. <em>Bucket size</em>: This is the size of the hash table.

<strong>Output</strong>: The output contains the frequent itemsets generated in each pass sorted lexicographically. It contains information about the memory usage during each pass over the data along with the hash buckets and their counts (Assume each count takes 4 bytes).

<strong>Note: </strong>In PCY the counts for pairs are stored in form of Triples (e.g. count of pair (“a”,”b”) is stored as (“a”, ”b”, <count>) and it uses 12 bytes.). Similarly, frequent itemsets of size 3 will be stored in form of quadruples taking 16 bytes and so on. The counts in the buckets can vary depending on the hashing function used. So do not try to match this with the output files provided. Also, while finding frequent pairs you should hash all the possible pairs but in finding frequent itemsets of size >= 3, as you know the frequent itemsets of size-1 you can use those and hash only those itemsets whose all possible subsets of size-1 are frequent.

<strong>Sample Output: </strong> <a href="https://github.com/NandanNayak/Finding-Frequent-Item-Sets/blob/master/sample_output_pcy.txt">sample_output_pcy.txt</a>

A sample solutions is shown below.

<strong>Sample 1:</strong>

Executing code:<em><strong>python nayak_nandan_pcy.py input2.txt 3 20</strong>

<strong>Output</strong>

memory for item counts: 48

memory for hash table counts for size 2 itemsets: 80

{0: 0, 1: 2, 2: 0, 3: 2, 4: 2, 5: 3, 6: 2, 7: 1, 8: 1, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0}

frequent item sets of size 1 :  [['e']]
<p>
</p>
<p>
</p>
PASS : 2

memory for frequent itemsets of size 1 : 8

bitmap size : 20

frequent item sets of size 2 :  []</em>
<p> </p>
<p> </p>

Here for the 1st pass we show the memory used for the item counts, hash table counts, hash_buckets with their counts and frequent itemsets found respectively. As there are no frequent itemsets of size 2, we do not output anything for subsequent passes.


###Problem 2: Multi-Stage Algorithm

Implementingthe Multi-Stage algorithm to generate frequent itemsets. There are two stages using two different hashing functions for finding frequent itemsets of each size. Usng hashing functions which are independent of each other. Both the hashes will have the same number of buckets. Also while finding frequent pairs, all the possible pairs are hashed but the frequent itemsets of size >= 3, as we know the frequent itemsets of size-1. The counts in the buckets can vary depending on the hashing function used. 

Input parameters are same as above. For output please follow the format shown below:

<strong>Sample Output: </strong> <a href="https://github.com/NandanNayak/Finding-Frequent-Item-Sets/blob/master/sample_output_multistage.txt">sample_output_multistage.txt</a>

<strong>Sample 1:</strong>

Executing code:<em><strong>python nayak_nandan_multistage.py input2.txt 2 20</strong></em>

<strong>Output</strong>
<em>

<p>memory for item counts: 48

memory for hash table 1 counts for size 2 itemsets: 80

{0: 0, 1: 2, 2: 0, 3: 2, 4: 2, 5: 3, 6: 2, 7: 1, 8: 1, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0}

Frequent itemsets of size 1 :  [['a'], ['d'], ['e']]</p>



<p>memory for frequent itemsets of size 1 : 24

bitmap 1 size: 20

memory for hash table 2 counts for size 2 itemsets: 80

{0: 0, 1: 2, 2: 0, 3: 2, 4: 2, 5: 3, 6: 2, 7: 1, 8: 1, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0}

bitmap 2 size: 20

memory for candidates counts of size 2 : 36

memory for hash table 1 counts for size 3 itemsets: 80

{0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 2, 7: 1, 8: 2, 9: 2, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0}

Frequent itemsets of size 2 :  [['a', 'e'], ['d', 'e']]</p>



<p>memory for frequent itemsets of size 2 : 24

bitmap 1 size: 20

memory for hash table 2 counts for size 3 itemsets: 80

{0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 2, 7: 1, 8: 2, 9: 2, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0}

bitmap 2 size: 20

memory for candidates counts of size 3 : 0

memory for hash table 1 counts for size 4 itemsets: 80

{0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 1, 10: 1, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18:  0, 19: 0}</em></p>


###Problem 3: Toivonen Algorithm
Implementing the Toivonen algorithm to generate frequent itemsets. For this algorithm we have used a sample size of less than 60% of your entire dataset. Also a simple Apriori algorithm is implemented with the random sample set. After Checking for negative borders, the algorithm is executed again with a different sample set ifrequired till there are no negative borders that have frequency > support.

<strong>Note:</strong> The number of iterations might differ in your output depending on the random sample which is generated.

<strong>Input Parameters:</strong>

1. Input.txt: This is the input file containing all transactions. Each line corresponds to a transaction. Each transaction has items that are comma separated. Use toivonen_test.txt to test this algorithm.

2. Support: Integer that defines the minimum count to qualify as a frequent itemset.

Executing code: <strong><em>python nayak_nandan_toivonen.py toivonen_test.txt 20</em></strong>

<strong>Output:</strong>
<em>

Line 1 (number of iterations performed)

Line 2 (fraction of transactions used)

Line 3 onwards (frequent itemsets lexicographically sorted)</em>

<strong>Sample Output: </strong> <a href="https://github.com/NandanNayak/Finding-Frequent-Item-Sets/blob/master/sample_output_toivonen.txt">sample_output_toivonen.txt</a>


