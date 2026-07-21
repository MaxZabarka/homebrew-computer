# Multiplication, recursion, and other missing instructions

This is my favorite chapter, because it is where the constraints stop being limitations and start being puzzles. The machine has no multiply, no divide, no right shift, no status register, no hardware stack, and an ALU half as wide as its addresses. Real programs need all of those things. Every one of them is rebuilt in software, and each rebuild is a small, satisfying algorithm. Let me show you the collection.

## Shifting by adding

Start with the smallest trick. The C `<<` operator needs a left shift, and the 74181 (4-bit ALU slice) has no shifter. But look at the expression menu from chapter 6: `B+B`. Adding a number to itself doubles it, and doubling is a shift left by one. So `x << n` compiles to a loop that runs n times, executing `B = (B+B)` each pass. The translator emits a little counted loop with its own label for every shift. Shifting by four costs four additions. Slow? Absolutely. Correct, and made of nothing but an adder? Also yes, and that trade should feel familiar by now.

## Multiplication, three ways

`tests/` contains three multiplication algorithms, all in plain C, because multiply has to be a function on this machine. They make a nice little ladder of sophistication.

`iterative_mult.c` is multiplication the way you first learned it, as repeated addition:

```c
int mult(int a, int b) {
    int sum = 0;
    while (a) {
        sum = sum + b;
        a = a - 1;
    }
    return sum;
}
```

`recursive_mult.c` is the same idea folded into recursion: `x * y` is `x + x * (y - 1)`, with `y == 0` returning 0. It exists mostly to prove a point, which is that recursion on this machine is real enough to lean on, and we will see below why that is earned.

`fast_mult.c` is the one with an actual idea in it, shift-and-add, the binary version of the long multiplication you did in school:

```c
int mult(int x, int y)
{
    int sum;
    int i = 8;
    while (i)
    {
        i = i - 1;
        if ((y << i) & 0b10000000)
        {
            sum = sum + x;
        }
        x = x << 1;
    }
    return sum;
}
```

Walk one bit at a time through y, and wherever there is a 1, add the appropriately doubled copy of x. Eight iterations always, instead of up to 255, and every operation in it, the shifts, the AND, the adds, is something chapter 6's menu actually offers. School method, base 2, running on 1960s silicon.

And notice the comment I left in the real file: `sum` is deliberately never initialized, because the initialization would not fit in the 1KB ROM alongside everything else. If that byte of RAM happens to be nonzero, the program is wrong. It usually is zero, and the program usually works, and the test suite has a special mode that fills RAM with garbage precisely to catch this kind of sin. This is what programming against a 1KB budget actually feels like.

Division never made it in at all. There is no `/` anywhere in the test suite; by the time multiplication worked three ways, division by repeated subtraction would have been more of the same lesson, and ROM space was better spent elsewhere.

## Comparisons, when flags evaporate

C says `a < b` is an expression with a value, 1 or 0. Chapter 6 said the flags live for exactly one instruction and vanish. So how do you materialize a comparison into a byte you can store? You branch on it immediately, and let the two branches write the answer:

```text
    (B-C), JLT        subtract, jump to TRUE if negative
    push 0            fell through: not less
    JMP DONE
TRUE:
    push 1
DONE:
```

The translator generates this diamond, with fresh labels, for every single `<`, `>`, `==`, `!=`, `<=`, `>=` in your program. Six C characters, a dozen instructions. The one-instruction compare-and-jump from chapter 7 is what keeps this expansion this small; without the free jump riding on the subtract, it would be worse.

## Adding numbers wider than the ALU

Pointers are 16 bits and the ALU is 8. To add, say, an array index to a base pointer, the translator does what you do on paper when a column overflows: add the low bytes, and if that overflowed, carry a one into the high column. The carry flag is the "if that overflowed", and the free conditional jump is the "carry the one":

```text
    B = low(base), C = low(index)
    RAM = (B+C)          add low bytes, carry flag set or not
    (B+C), JNC skip      no carry? skip the fix-up
    B = high(result)
    RAM = (B+1)          carry the one
skip:
    ...
```

That `JNC skip` hopping over an increment is the entire mechanism behind every 16-bit add on this machine, including the pointer math hiding inside every `arr[i]` your C program writes (remember, the parser turned those into pointer additions back in chapter 9).

## Recursion with no hardware stack

The machine has no push instruction, no pop instruction, no stack pointer register. The VM builds the entire function-call world out of one byte of RAM (the stack pointer at address 0) and discipline. When the translator expands `call fib 1`, it pushes a return address (two bytes, because addresses are 16 bits), pushes the caller's LOCAL and ARGUMENT pointer bytes, repoints those pointers for the callee, and jumps. `return` walks it all back: fetches the return address into scratch bytes, writes the return value over the arguments, cuts the stack, restores the caller's pointers, and jumps through the saved address.

The reason recursion works is worth stating plainly, because nothing in the hardware suggests it should: every call pushes the caller's context onto the same stack the data lives on, so ten nested calls are ten stacked frames, each knowing how to restore the one beneath it. `fib(8)` calls `fib(7)` calls `fib(6)`, and the stack in the debugger visibly staircases up and back down. The return labels are numbered (`RETURNfib1`, `RETURNfib2`) so every call site is distinct, and a bootstrap plants the first frame by setting the stack pointer to 9 and calling `main`.

![The emulator running recursive fib, stack frames growing and shrinking](../media/emulator-run.gif)

Every algorithm in this chapter compiles to nothing but moves, ten ALU expressions, and jumps through A. That is the whole vocabulary, and it turns out to be enough for C. The remaining chapters are about the machinery that turns this story into bytes and pictures: the assembler, and the two emulators.

Next: [The assembler](12-the-assembler.md)
