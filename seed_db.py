# seed_db.py
import sqlite3

conn = sqlite3.connect("problems.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        status TEXT CHECK(status IN ('new','inprogress','done')) DEFAULT 'new',
        skip_until DATETIME NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
""")

# Seed test array data entries
sample_problems = [
    # --- 1 & 2. LINEAR & BINARY SEARCH ---
    ("Two Sum", "https://leetcode.com/problems/two-sum/"),
    ("Binary Search", "https://leetcode.com/problems/binary-search/"),
    ("Search Insert Position", "https://leetcode.com/problems/search-insert-position/"),
    ("First Bad Version", "https://leetcode.com/problems/first-bad-version/"),
    ("Peak Index in a Mountain Array", "https://leetcode.com/problems/peak-index-in-a-mountain-array/"),
    ("Find Peak Element", "https://leetcode.com/problems/find-peak-element/"),
    ("Search in Rotated Sorted Array", "https://leetcode.com/problems/search-in-rotated-sorted-array/"),
    ("Search in Rotated Sorted Array II", "https://leetcode.com/problems/search-in-rotated-sorted-array-ii/"),
    ("Find Minimum in Rotated Sorted Array", "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/"),
    ("Find First and Last Position of Element in Sorted Array", "https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/"),
    ("Search a 2D Matrix", "https://leetcode.com/problems/search-a-2d-matrix/"),
    ("Koko Eating Bananas", "https://leetcode.com/problems/koko-eating-bananas/"),
    ("Capacity To Ship Packages Within D Days", "https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/"),
    ("Find the Smallest Divisor Given a Threshold", "https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/"),
    ("Median of Two Sorted Arrays", "https://leetcode.com/problems/median-of-two-sorted-arrays/"),

    # --- 3. HASHSET ---
    ("Contains Duplicate", "https://leetcode.com/problems/contains-duplicate/"),
    ("Intersection of Two Arrays", "https://leetcode.com/problems/intersection-of-two-arrays/"),
    ("Happy Number", "https://leetcode.com/problems/happy-number/"),
    ("Longest Consecutive Sequence", "https://leetcode.com/problems/longest-consecutive-sequence/"),
    ("Jewels and Stones", "https://leetcode.com/problems/jewels-and-stones/"),
    ("Unique Number of Occurrences", "https://leetcode.com/problems/unique-number-of-occurrences/"),
    ("Find All Numbers Disappeared in an Array", "https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/"),
    ("First Missing Positive", "https://leetcode.com/problems/first-missing-positive/"),
    ("Design HashSet", "https://leetcode.com/problems/design-hashset/"),
    ("Subarray Sums Divisible by K", "https://leetcode.com/problems/subarray-sums-divisible-by-k/"),
    ("Continuous Subarray Sum", "https://leetcode.com/problems/continuous-subarray-sum/"),
    ("Path Sum III", "https://leetcode.com/problems/path-sum-iii/"),
    ("Distribute Candies", "https://leetcode.com/problems/distribute-candies/"),

    # --- 4. HASHMAPS ---
    ("Valid Anagram", "https://leetcode.com/problems/valid-anagram/"),
    ("Two Sum II - Input Array Is Sorted", "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/"),
    ("Group Anagrams", "https://leetcode.com/problems/group-anagrams/"),
    ("Intersection of Two Arrays II", "https://leetcode.com/problems/intersection-of-two-arrays-ii/"),
    ("Isomorphic Strings", "https://leetcode.com/problems/isomorphic-strings/"),
    ("Word Pattern", "https://leetcode.com/problems/word-pattern/"),
    ("Find All Anagrams in a String", "https://leetcode.com/problems/find-all-anagrams-in-a-string/"),
    ("Top K Frequent Elements", "https://leetcode.com/problems/top-k-frequent-elements/"),
    ("Sort Characters By Frequency", "https://leetcode.com/problems/sort-characters-by-frequency/"),
    ("Subarray Sum Equals K", "https://leetcode.com/problems/subarray-sum-equals-k/"),
    ("Design HashMap", "https://leetcode.com/problems/design-hashmap/"),
    ("Ransom Note", "https://leetcode.com/problems/ransom-note/"),
    ("Insert Delete GetRandom O(1)", "https://leetcode.com/problems/insert-delete-getrandom-o1/"),
    ("Majority Element", "https://leetcode.com/problems/majority-element/"),

    # --- 5. ARRAYS - SLIDING WINDOW & TWO POINTER ---
    ("Move Zeroes", "https://leetcode.com/problems/move-zeroes/"),
    ("Squares of a Sorted Array", "https://leetcode.com/problems/squares-of-a-sorted-array/"),
    ("Remove Duplicates from Sorted Array", "https://leetcode.com/problems/remove-duplicates-from-sorted-array/"),
    ("Remove Duplicates from Sorted Array II", "https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/"),
    ("3Sum", "https://leetcode.com/problems/3sum/"),
    ("3Sum Closest", "https://leetcode.com/problems/3sum-closest/"),
    ("4Sum", "https://leetcode.com/problems/4sum/"),
    ("Container With Most Water", "https://leetcode.com/problems/container-with-most-water/"),
    ("Trapping Rain Water", "https://leetcode.com/problems/trapping-rain-water/"),
    ("Best Time to Buy and Sell Stock", "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"),
    ("Maximum Subarray", "https://leetcode.com/problems/maximum-subarray/"),
    ("Maximum Product Subarray", "https://leetcode.com/problems/maximum-product-subarray/"),
    ("Product of Array Except Self", "https://leetcode.com/problems/product-of-array-except-self/"),
    ("Minimum Size Subarray Sum", "https://leetcode.com/problems/minimum-size-subarray-sum/"),
    ("Longest Substring Without Repeating Characters", "https://leetcode.com/problems/longest-substring-without-repeating-characters/"),
    ("Longest Repeating Character Replacement", "https://leetcode.com/problems/longest-repeating-character-replacement/"),
    ("Permutation in String", "https://leetcode.com/problems/permutation-in-string/"),
    ("Minimum Window Substring", "https://leetcode.com/problems/minimum-window-substring/"),
    ("Sliding Window Maximum", "https://leetcode.com/problems/sliding-window-maximum/"),
    ("Fruit Into Baskets", "https://leetcode.com/problems/fruit-into-baskets/"),
    ("Max Consecutive Ones III", "https://leetcode.com/problems/max-consecutive-ones-iii/"),
    ("Subarrays with K Different Integers", "https://leetcode.com/problems/subarrays-with-k-different-integers/"),

    # --- 6. MATRICES ---
    ("Set Matrix Zeroes", "https://leetcode.com/problems/set-matrix-zeroes/"),
    ("Spiral Matrix", "https://leetcode.com/problems/spiral-matrix/"),
    ("Spiral Matrix II", "https://leetcode.com/problems/spiral-matrix-ii/"),
    ("Rotate Image", "https://leetcode.com/problems/rotate-image/"),
    ("Word Search", "https://leetcode.com/problems/word-search/"),
    ("Search a 2D Matrix II", "https://leetcode.com/problems/search-a-2d-matrix-ii/"),
    ("Diagonal Traverse", "https://leetcode.com/problems/diagonal-traverse/"),
    ("Valid Sudoku", "https://leetcode.com/problems/valid-sudoku/"),
    ("Pacific Atlantic Water Flow", "https://leetcode.com/problems/pacific-atlantic-water-flow/"),
    ("Number of Islands", "https://leetcode.com/problems/number-of-islands/"),
    ("Surrounded Regions", "https://leetcode.com/problems/surrounded-regions/"),
    ("Maximal Square", "https://leetcode.com/problems/maximal-square/"),

    # --- 7. BIT MANIPULATION ---
    ("Single Number", "https://leetcode.com/problems/single-number/"),
    ("Single Number II", "https://leetcode.com/problems/single-number-ii/"),
    ("Number of 1 Bits", "https://leetcode.com/problems/number-of-1-bits/"),
    ("Counting Bits", "https://leetcode.com/problems/counting-bits/"),
    ("Reverse Bits", "https://leetcode.com/problems/reverse-bits/"),
    ("Missing Number", "https://leetcode.com/problems/missing-number/"),
    ("Sum of Two Integers", "https://leetcode.com/problems/sum-of-two-integers/"),
    ("Bitwise AND of Numbers Range", "https://leetcode.com/problems/bitwise-and-of-numbers-range/"),
    ("Power of Two", "https://leetcode.com/problems/power-of-two/"),
    ("Subsets", "https://leetcode.com/problems/subsets/"),
    ("Add Binary", "https://leetcode.com/problems/add-binary/"),

    # --- 8. STRINGS ---
    ("Valid Palindrome", "https://leetcode.com/problems/valid-palindrome/"),
    ("Valid Palindrome II", "https://leetcode.com/problems/valid-palindrome-ii/"),
    ("Longest Palindromic Substring", "https://leetcode.com/problems/longest-palindromic-substring/"),
    ("Palindromic Substrings", "https://leetcode.com/problems/palindromic-substrings/"),
    ("Reverse String", "https://leetcode.com/problems/reverse-string/"),
    ("Reverse Words in a String", "https://leetcode.com/problems/reverse-words-in-a-string/"),
    ("Longest Common Prefix", "https://leetcode.com/problems/longest-common-prefix/"),
    ("String to Integer (atoi)", "https://leetcode.com/problems/string-to-integer-atoi/"),
    ("Implement strStr()", "https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/"),
    ("Multiply Strings", "https://leetcode.com/problems/multiply-strings/"),
    ("Zigzag Conversion", "https://leetcode.com/problems/zigzag-conversion/"),
    ("Encode and Decode Strings", "https://leetcode.com/problems/encode-and-decode-strings/"),

    # --- 9. LINKED LIST ---
    ("Reverse Linked List", "https://leetcode.com/problems/reverse-linked-list/"),
    ("Reverse Linked List II", "https://leetcode.com/problems/reverse-linked-list-ii/"),
    ("Merge Two Sorted Lists", "https://leetcode.com/problems/merge-two-sorted-lists/"),
    ("Linked List Cycle", "https://leetcode.com/problems/linked-list-cycle/"),
    ("Linked List Cycle II", "https://leetcode.com/problems/linked-list-cycle-ii/"),
    ("Remove Nth Node From End of List", "https://leetcode.com/problems/remove-nth-node-from-end-of-list/"),
    ("Reorder List", "https://leetcode.com/problems/reorder-list/"),
    ("Palindrome Linked List", "https://leetcode.com/problems/palindrome-linked-list/"),
    ("Intersection of Two Linked Lists", "https://leetcode.com/problems/intersection-of-two-linked-lists/"),
    ("Copy List with Random Pointer", "https://leetcode.com/problems/copy-list-with-random-pointer/"),
    ("Add Two Numbers", "https://leetcode.com/problems/add-two-numbers/"),
    ("Merge k Sorted Lists", "https://leetcode.com/problems/merge-k-sorted-lists/"),
    ("Reverse Nodes in k-Group", "https://leetcode.com/problems/reverse-nodes-in-k-group/"),
    ("LRU Cache", "https://leetcode.com/problems/lru-cache/"),
    ("LFU Cache", "https://leetcode.com/problems/lfu-cache/"),

    # --- 10. STACKS ---
    ("Valid Parentheses", "https://leetcode.com/problems/valid-parentheses/"),
    ("Min Stack", "https://leetcode.com/problems/min-stack/"),
    ("Evaluate Reverse Polish Notation", "https://leetcode.com/problems/evaluate-reverse-polish-notation/"),
    ("Generate Parentheses", "https://leetcode.com/problems/generate-parentheses/"),
    ("Daily Temperatures", "https://leetcode.com/problems/daily-temperatures/"),
    ("Online Stock Span", "https://leetcode.com/problems/online-stock-span/"),
    ("Car Fleet", "https://leetcode.com/problems/car-fleet/"),
    ("Largest Rectangle in Histogram", "https://leetcode.com/problems/largest-rectangle-in-histogram/"),
    ("Implement Queue using Stacks", "https://leetcode.com/problems/implement-queue-using-stacks/"),
    ("Decode String", "https://leetcode.com/problems/decode-string/"),
    ("Asteroid Collision", "https://leetcode.com/problems/asteroid-collision/"),
    ("Remove All Adjacent Duplicates In String II", "https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/"),

    # --- 11. SORTING (BUBBLE, SELECTION, INSERTION, CYCLIC, MERGE, QUICK) ---
    # Cyclic Sort (High-yield Interview Patterns)
    ("Find the Duplicate Number", "https://leetcode.com/problems/find-the-duplicate-number/"),
    ("Find All Duplicates in an Array", "https://leetcode.com/problems/find-all-duplicates-in-an-array/"),
    ("Set Mismatch", "https://leetcode.com/problems/set-mismatch/"),
    
    # Merge / Quick / Bucket Sort Logic & Fundamentals
    ("Sort an Array", "https://leetcode.com/problems/sort-an-array/"),
    ("Merge Intervals", "https://leetcode.com/problems/merge-intervals/"),
    ("Insert Interval", "https://leetcode.com/problems/insert-interval/"),
    ("Non-overlapping Intervals", "https://leetcode.com/problems/non-overlapping-intervals/"),
    ("Kth Largest Element in an Array", "https://leetcode.com/problems/kth-largest-element-in-an-array/"),
    ("Top K Frequent Words", "https://leetcode.com/problems/top-k-frequent-words/"),
    ("Sort Colors", "https://leetcode.com/problems/sort-colors/"),
    ("Meeting Rooms II", "https://leetcode.com/problems/meeting-rooms-ii/"),
    ("K Closest Points to Origin", "https://leetcode.com/problems/k-closest-points-to-origin/")
]

conn.executemany("INSERT INTO problems (name, url) VALUES (?, ?)", sample_problems)
conn.commit()
conn.close()
print("Database initialized and populated with basic sample dataset.")