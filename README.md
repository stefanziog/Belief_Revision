# Belief_Revision
Implementation of the second assignment for the course Introduction to Artificial Intelligence. Code compiles and runs on python 3.10 and a macOS system. 

# Requirements
Run the following statement to install all the requirements: 

```python
pip install -r requirements.txt
```

# How to run the code
Run the following command to execute the belief revision: 

```python
python cli.py
```

Available Actions Are: 

```
1. Display Belief Base: to print the belief base 
2. Add to Base: to add a belief to the belief base
3. Clear Base: to clear the belief base
4. Check entailment: to check if a belief is true or false in the belief base
5. Quit: to quit the program
```

The following operators can be used: 

```
& : and
| : or
>> : implies
<> : biconditional
~ : not
```

# How to run the tests
```python
python test.py

