def parse(message):
  values = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty":  50, "sixty":  60, "seventy": 70, "eighty": 80, "ninety": 90
  }
  
  scales = {
    "hundred": 100,
    "thousand": 1000,
    "million": 1000000
  }

  tokens = message.strip().lower().split()
  
  if not tokens or (tokens[0] not in values and tokens[0] not in scales):
    return -1
  
  ret = 0
  curr = 0
  i = 0

  while i < len(tokens):
    token = tokens[i]

    if token in values:
      curr += values[token]
      i += 1
    elif token in scales:
      curr *= scales[token]

      # if the multiplier is hundreds, it can still have more
      # that can be added to current, ex 'one hundred and fifty'
      # but, if it's not hundred, then it can be added
      # because other multis finalise the 'section' of numbers.
      if token != "hundred":
        ret += curr
        curr = 0
      
      i += 1
    elif token == "and":
      i += 1
    else:
      break

  ret += curr
  return ret