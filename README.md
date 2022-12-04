Project \#3 Decision Tree Learning
----------------------------------

# Introduction

In this project you will work in groups of up to three to write a Python program to implement a classifier to learn the structure of data from a set of training examples. You will evaluate your classifier using the [congressional voting records dataset][votes], which lists the votes of members of the US House of Representatives on different issues and their classification as a Democrat or a Republican.

Your classifier will be in the form of a decision tree created from the training examples. The decision tree will then classify test examples as either democrat or republican and the results of the classification will be reported.  
To explore the effects of overfitting and pruning, you will also apply
&chi;<sup>2</sup> pruning to the learned tree and compare the results.

[votes]:https://archive.ics.uci.edu/ml/datasets/congressional+voting+records

# Data

Training and testing sets of the congressional voting records dataset are available in the project GitHub repository as CSV files: `house-dataset-train.csv` and `house-dataset-test.csv`. Additionally, there is
an attributes file: `house-dataset-attributes.txt` which lists each attribute on a separate line starting
with the attribute name and then the possible values for the attribute, e.g., the first line of the file is:
`response,republican,democrat`

Note that each attribute other than the response is a "Yes" or "No" vote, but some of the data is 
missing, which is represented by "?" For the purposes of this project, treat missing data as an additional 
attribute value.

The restaurant dataset from the textbook (R&N Figure 18.3) has also been included as `restaurant.csv` as well as a corresponding attributes file `restaurant-attributes.txt`. This is a much smaller dataset that should be useful for testing your classifier.

The `csv` Python library [https://docs.python.org/3/library/csv.html][csv]  is recommended for reading in the above data.

[csv]:https://docs.python.org/3/library/csv.html

# Requirements

Your program will implement the decision tree learning algorithm from the textbook with &chi;<sup>2</sup> pruning. You must write this all yourself, i.e., you *should not* use any machine learning or statistical packages in your implementation, with the exception of the statistical functions for &chi;<sup>l2</sup> testing from `scipy.stats.chi2`. If you are in doubt about a particular package, please ask.

Your program will be run with the command-line arguments shown below:

`python3 classifier.py <attributes> <training-set> <testing-set> <significance>`


The first argument specifies the attributes files (in the format specified above), the second argument specifies the training set (in the format specified above), the third argument specifies the testing set (in the format specified above), and the fourth argument specifies the significance level for &chi<sup>2</sup> pruning. If your program is not given a fourth command-line argument, the tree should be learned without the use of &chi;<sup>2</sup> pruning.

On the terminal, your program must output the following.
  1. For the training set and the test set.
  
     - Recognition rate (% correct).
     - A confusion matrix, which includes the number of occurrences for each combination of assigned class (rows) and actual class (columns). The main diagonal contains counts for correctly assigned examples, all remaining cells correspond to counts for different types of error.
    
  2. A summary of the learned decision tree.
  
     - Number of nodes and number of leaf (decision) nodes.
     - A printout of the tree. (Use indentation to show the depth of different nodes.)
     - Maximum, minimum, and average depth of root-to-leaf paths in the decision tree.
     - The printout of your tree and the corresponding summary should look like the following.
```
-- Printing Decision Tree --
Testing Patrons
    Branch Some
    Leaf with value: Yes
    Branch Full
    Testing Hungry
        Branch Yes
        Testing Type
            Branch French
            Leaf with value: Yes
            Branch Thai
            Testing Fri/Sat
                Branch No
                Leaf with value: No
                Branch Yes
                Leaf with value: Yes
            Branch Burger
            Leaf with value: Yes
            Branch Italian
            Leaf with value: No
        Branch No
        Leaf with value: No
    Branch None
    Leaf with value: No
Total Nodes: 12
Decision Nodes: 8
Maximum Depth: 4
Minimum Depth: 1
Average Depth of Root-to-Leaf: 2.625
```


## Writeup

Along with submitting your code, your group must also submit a 2–3 page writeup that contains the following:

  * Briefly describe your approach implementing the decision tree algorithm and &chi;<sup>2</sup> pruning.
  * Confusion matrices for congressional voting records dataset, both the training and test sets, for your unpruned tree and your tree pruned with a significance level of 5% or 1%.
  * A discussion and comparison of your results.

## Checkpoint

As a project checkpoint, you must schedule a time for your group to meet with me
to discuss your initial implementation and your plans for the project by Friday, December 2. Note that you should have at least the initial parts of your project implemented by this meeting (e.g., reading in the dataset, representing the tree, etc.) and should be prepared to discuss your plans for finishing the project. Failure to schedule and attend this meeting will result in a penalty on your project grade.

## Submission

Make sure to commit to your team's github repository as you make changes to your project. The project is due Friday, December 9 at 11:59 PM. A complete
submission consists of the following files.

  * Your writeup as a single PDF file, which must be named `project3.pdf`.
  * Your source code as `classifier.py`.
  * A short textfile that describes how to run your program as `readme.txt`.
  * Your discussion log as `discussion.txt`.

When you are ready to submit your assignment, create a "Release" on github. This will tag the commit
and make a downloadable archive of the state of the files. I will grade the most-recent release created
within the deadline (or late deadline when submitting late). Note that if you are using github throughout your
development process, you should only need to create your release once for the deadline, since your incremental
progress will be saved in the commit history.

## Grading

  * Correct implementation of the decision-tree learning algorithm and related code: 55 points.
  * Correct implementation of &chi;<sup>2</sup>-pruning algorithm: 15 points
  * Code clarity/efficiency and organization: 10 points
  * Writeup: 20 points

Programming Style: You will be graded
not only on whether your program works correctly, but also on
programming style, such as the use of informative names, good
comments, easily readable formatting, and a good balance between
compactness and clarity (e.g., do not define lots of unnecessary
variables). Create appropriate
functions for tasks that can be encapsulated.
