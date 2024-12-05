# File Renamer

File renamer is a python script which helps the users when they want to organise their files following a naming convention.

## Installation

Download or clone this repo

```bash
git clone https://github.com/georgipetkov18/file-renamer.git
```

1) Using the python file
- Make sure you have python installed on your machine

```bash
python --version
```

- Run the script

```bash
python renamer.py
```

2) Using the executable file
- Just start the exe file

## Usage

Three options will be displayed

```bash
0.Exit
1.Basic Rename - rename files using your input and incrementing a counter afterwards
2.Pattern Based Rename - rename files based on an input pattern
```

Click the one which works the best for you by simply entering the number before the option in the terminal and clicking enter. Then follow the instructions. If the pattern based rename is selected one can use &lt;c&gt; sequence inside the name to sepcify the place where the variable part lies. Furthermore, one can use a number inside the &lt;c&gt; container to specify how many digits they want the newly generated sequence to be, e.g. &lt;c:d4&gt; will generate 4 digits and if the current number has fewer digits then it will be prepended with zeros.
