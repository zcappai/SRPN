import operator as op
stackNum = []
stackLim = 23 # 'stackNum' size
maxInt = 2147483647
minInt = -2147483648
# True = inputs are accepted, False = inputs NOT accepted
hashToggle = True
# Acceptable non-integer characters
accepted = ['r', 'd', '+', '-', '*', '/', '%', '=', '^', ' ', '#']
# Numbers for input of "r"
random = [1804289383, 846930886, 1681692777, 1714636915, 1957747793, 424238335, 719885386, 1649760492, 596516649, 1189641421, 1025202362, 1350490027, 783368690, 1102520059, 2044897763, 1967513926, 1365180540, 1540383426, 304089172, 1303455736, 35005211, 521595368]
# Current position in 'random' array
randPos = 0

# Returns number from 'random' array
def randNum():
  # Global variable to be changed within function
  global randPos
  # 'randPos' resets if it reaches end of 'random' array
  if(randPos == len(random)):
    randPos = 0
  randNum = random[randPos]
  randPos += 1
  return randNum

# Adds number to 'stackNum' if stack is NOT full
def stackAdd(number):
  if(len(stackNum) < stackLim):
    stackNum.append(number)
  # Prints error message if stack is full
  elif(len(stackNum) >= stackLim):
    print("Stack overflow.")

# Changes 'hashToggle' between True and False if input is "#"
def hash(user_input):
  # Global variable to be changed within function
  global hashToggle
  if(user_input == "#"):
    # 'hashToggle' changes to opposite value
    hashToggle = not hashToggle

# Checks one line expression for "#" and changes 'hashToggle'
def hashOneline(string, current_index):
  if(string[current_index] == "#"):
    # Only if "#" is at beginning or end of expression
    if(current_index == 0 and string[current_index + 1] == " "):
      hash(string[current_index])
    elif(current_index == len(string) - 1 and string[current_index - 1] == " "):
      hash(string[current_index])
    # Only if "#" is NOT at beginning or end of expression
    elif(current_index != 0 and current_index != len(string) - 1):
      if(string[current_index + 1] == " " and string[current_index - 1] == " "):
        hash(string[current_index])
      # Error message if no empty space before and after "#"
      else:
        print(f'Unrecognised operator or operand "{string[current_index]}".')
    elif(hashToggle == True):
        print(f'Unrecognised operator or operand "{string[current_index]}".')

# Handles saturation of integers
def saturation(integer):
  # Returns 'maxInt'(or 'minInt') if number is too high (or too low)
  if(integer > maxInt):
    return maxInt
  elif(integer < minInt):
    return minInt
  else:
    return integer

# Converts operator from string to usable function
def operation(x):
  # Returns operation function corresponding to input operator
  if(x == "+"):
    return op.add
  elif(x == "-"):
    return op.sub
  elif(x == "*"):
    return op.mul
  elif(x == "/"):
    return op.truediv
  elif(x == "%"):
    return op.mod
  elif(x == "^"):
    return op.pow

# Carries out all calculations for SRPN calculator
def calculation(x):
  # Variables to be stored for calculation
  val1 = 0
  val2 = 0
  op = operation(x) # Input operator
  # 'raised' is 1 if exception raised at 'val1' assignment, else 0
  raised = 0
  # If stack empty, error message printed
  try:
    val1 = int(stackNum.pop())
  except Exception:
    print("Stack underflow.")
    raised = 1
  # If stack empty after 1st 'pop()', error message printed
  try:
    val2 = int(stackNum.pop())
    # If dividing by 0, error message printed as operation cannot be done
    if(val1 == 0 and x == "/"):
      print("Divide by 0.")
      stackAdd(val2)
      stackAdd(val1)
    # If NOT dividing by 0, operation carried out
    else:
      result = int(op(val2, val1))
      result = saturation(result) # Handling saturation of 'result'
      stackAdd(result)
  except Exception:
    # Error message only if exception NOT raised for 'val1'
    if(raised != 1):
      stackAdd(val1)
      print("Stack underflow.")

# Processes each individual character of input
def srpnInput(char):
  # Changes 'hashToggle' for "#" input
  hash(char)
  if(hashToggle == True):
    # If stack NOT empty, "=" prints last number added
    if(char == "="):
      if(len(stackNum) != 0):
        print(peek(stackNum))
      elif(len(stackNum) == 0):
        print("Stack empty.")
    # Spaces and empty inputs are ignored
    elif(char == "" or char ==  " "):
      pass
    # Operation is carried out
    elif(char == "+" or char == "-" or char == "*" or char == "/" or char == "%" or char == "^"):
      calculation(char)
    elif(char == "d"):
      # If stack NOT empty, full stack printed
      if(len(stackNum) != 0):
        for num in stackNum:
          print(num)
      # If stack empty, minimum integer printed
      elif(len(stackNum) == 0):
        print(minInt)
    # Generates number from 'random' array
    elif(char == "r"):
      r = randNum()
      stackAdd(r)
    elif(type(int(char)) == int):
      stackAdd(char)

# Returns last number added to stack using stack length
def peek(stack):
  length = len(stack)
  return stack[length - 1]

# Processes input of expressions written on 1 line (e.g. 11+1+1+d)
def oneline(x):
  # Stores each digit of individual numbers
  currentNum = ""
  # Temporary local stack
  stackTempNum = []

  # Iterates through each character of one line expression
  for i in range(len(x)):
    # Changes 'hashToggle' for "#" input
    hashOneline(x, i)
    if(hashToggle == True):
      # Digits of number added to 'currentNum'
      if(x[i].isdigit() == True):
        currentNum += x[i]
        # If expression or number ends by next character, 'currentNum' processed and stored
        if(i == len(x) - 1 or x[i+1].isdigit() == False):
          srpnInput(currentNum)
          stackTempNum.append(currentNum)
          currentNum = ""
      # Operation is carried out. Output of "=" depends on previous character
      elif(x[i] == "+" or x[i] == "-" or x[i] == "*" or x[i] == "/" or x[i] == "%" or x[i] == "^" or (x[i] == "=" and x[i-1] == " ")):
        srpnInput(x[i])
      elif(x[i] == "=" and x[i-1] != " "):
        if(len(stackTempNum) != 0):
          print(peek(stackTempNum))
        elif(len(stackTempNum) == 0):
          print("Stack empty.")
      elif(x[i] == "d"):
        srpnInput(x[i])
        # For special case when "=" preceded by "d"
        if(len(stackNum) > 0):
          stackTempNum.append(peek(stackNum))
      # Number from 'random' array processed and stored
      elif(x[i] == "r"):
        r = randNum()
        srpnInput(r)
        stackTempNum.append(r)
      # If character NOT an accepted value within SRPN calculator, error message printed
      elif(x[i].isalpha() == True or x[i] not in accepted):
        print(f'Unrecognised operator or operand "{x[i]}".')

# Main set of statements that run the SRPN calculator
print("You can now start interacting with the SRPN calculator")
while True:
  console_input = input()
  # Tries to pass input to 'srpnInput()'
  try:
    srpnInput(console_input)
  # If input is expression/non-accepted character, input passed to 'oneline()' instead
  except:
    if(console_input.isdigit() == False and console_input not in accepted):
      oneline(console_input)