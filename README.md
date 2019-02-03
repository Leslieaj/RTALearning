# RTALearning

A prototype tool on learning Real-time automata.

### Overview

This tool is dedicated to learning Real-time automata (RTAs) which is a subclass of Timed automata with only one clock that resets at every transition. In 1987, Dana Angluin introduced the $L^*$ Algorithm for learning regular sets from queries and counterexamples. The tool implement an Angluin-style active learning algorithm on RTAs.

### Installation & Usage

#### Prerequisite

- Python 2.7.*

- enum module

  ```shell
   pip2 install --upgrade pip2 enum34
  ```

#### Installation

- Just download.

It's a pure Python program. (We have test it on Ubuntu 16.04 64bit.)

#### Usage

For example

```shell
python2 learnrta.py test_automata/a.json
```

- `learnrta.py` is the main file of the program.

- The target RTA is stored in a JSON file, in this example, `a.json` . The details are as follows.

  ```json
  {
      "name": "A",
      "s": ["1", "2"],
  	"sigma": ["a", "b"],
  	"tran": {
  		"0": ["1", "b", "[2,4)", "1"],
  		"1": ["1", "a", "(5,7)", "2"],
  		"2": ["2", "b", "[0,+)", "2"]
  	},
  	"init": "1",
  	"accept": ["2"]
  }
  ```

  - "name" : the name of the target RTA;
  - "s" : the set of the name of states (locations);
  - "sigma" : the alphabet;
  - "tran" : the set of transitions in the following form:
    - transition id : [name of the source state, action, guard, name of the target state]

  - "init" : the name of initial state (location);
  - "accept" : the set of the name of accepting states.

#### Output

- Every real-time observation table during the learning process;
- If we learn the target RTA successfully, then the finial CRTA will be printed on the terminal. Additionally, the total time, the size of $S$, the size of $R$, the size of $E$, the number of equivalence query, and the number of membership query will also be given. (Due to randomness in the algorithm, total time and such above numbers may be different even you run the same example.)
- If we did not learn the target RTA, we print "Error! Learning Failed." on the terminal.