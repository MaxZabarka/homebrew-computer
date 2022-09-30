const LOADS = {
  "000": null,
  "001": "AHigh",
  "010": "ALow",
  "011": "B",
  "100": "C",
  "101": "RAM",
};
const ENABLES = {
  "000": null,
  "001": "AHigh",
  "010": "ALow",
  "011": "B",
  "100": "C",
  "101": "RAM",
  "110": "IRHigh",
};

const JUMPS = {
  "0001": { zero: true, negative: true },
  "0010": { negative: true },
  "0011": { zero: true },
  "0100": { zero: false, negative: false },
  "0101": { negative: false },
  "0110": { carry: true },
  "0111": { carry: false },
  "1000": {},
};

const JUMP_NAMES = {
  "0001":"JLE",
  "0010":"JLT",
  "0011":"JEQ",
  "0100":"JGT",
  "0101":"JGE",
  "0110":"JC",
  "0111":"JNC",
  "1000":"JMP",
}

const EXPRESSIONS = {
"100110": "B+C",
"111110": "B-1",
"000000": "B+1",
"011000": "B-C",
"011010": "B-C-1",
};

module.exports = { ENABLES, LOADS, JUMPS, EXPRESSIONS, JUMP_NAMES };
