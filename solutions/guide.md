# Guide to Obtaining Codes

This will be a guide on how and where to obtain the codes required for
submission for the Synacor Challenge

## 1st Code

The first code can be found just by reading the [`arch-spec`](../arch-spec),
in the **hints** section.

## 2nd Code

The second code is obtainable once the implementations for the `halt`, `out`
and `noop` operations are defined. Then, running the included binary with
our virtual machine will yield the code along with a message:

```shell
Welcome to the Synacor Challenge!
Please record your progress by putting codes like
this one into the challenge website: ************

```

## 3rd Code
The next code can only be obtained by implementing all operations defined in
the **opcode listing** section of the [`arch-spec`](../arch-spec), with the
exception of the `in` operation. Running the binary at this stage will also
display the following, in addition to the previous message:

```shell
Executing self-test...

self-test complete, all tests pass
The self-test completion code is: ************
```

## 4th Code
This is where things become interesting, as immediately after providing the
third code, the binary reveals itself to be a **text-based adventure game**,
where we can make choices according to the options provided.

From here on, since user input is necessary to continue, the `in` operation
has to be implemented as well. The fourth code can be obtained by providing
the following as input:

```shell
take tablet
use tablet
```

## 5th and 6th Code
Continuing on from the previous code, the next 2 codes are also obtainable by
simply playing the game, i.e. traversing the dungeon by making the correct
choices, with a touch of puzzle solving.

For posterity, the commands/inputs required to complete this stage are included
for reference and can be found [here](./dungeon.txt).

## 7th Code
Personally, this is by far the most difficult part of the challenge, and the way
it is hinted at is quite clever as well, with the following snippet lying in a
`strange book` found in the previous section.

```
...
The second destination, however, is predicted to require a very specific
energy level in the eighth register.  The teleporter must take great care to
confirm that this energy level is exactly correct before teleporting its user!

... you will need to extract the confirmation algorithm, reimplement it on more
powerful hardware, and optimize it....

Then, set the eighth register to this value, activate the teleporter, and
bypass the confirmation mechanism. ...
```

From the hint provided, it looks as though we need to modify the value
within the 8th register in some manner, then using the teleporter will allow us
to proceed. At first I tried tracing the instructions performed on activating
the teleporter but that got me nowhere. I have to admit, at this point I looked
at several solutions by others, but even then I was having some trouble wrapping
my head around the problem.   

With no other option, I decided to decompile the binary and take a peek at the
[source byte instructions](../data/bin_source.asm), a step which was detailed
to some degree in all the solutions I looked at. The 8th register(r7 in examples),
it turns out was only referenced 4 times in the whole file, and the following
snippet was what affected the teleporter:

```asm
6027:  JT   r0    6035              # if r0 != 0 jump to 6035, else 
6030:  ADD  r0    r1    1           # r0 = r1 + 1
6034:  RET                          
6035:  JT   r1    6048              # if r1 != 0 jump to 6048, else
6038:  ADD  r0    r0    32767       # r0 = (r0 - 1) mod 32768
6042:  SET  r1    r7                # r1 = r7
6045:  CALL 6027                    
6047:  RET                          
6048:  PUSH r0                      # append r0 to stack 
6050:  ADD  r1    r1    32767       # r1 = (r1 - 1) mod 32768
6054:  CALL 6027                    
6056:  SET  r1    r0                # r1 = r0
6059:  POP  r0                      # pop from stack and assign to r0
6061:  ADD  r0    r0    32767       # r0 = (r0 - 1) mod 32768
6065:  CALL 6027             
6067:  RET
```

The instruction calling this function is shown below:
```asm
5483:  SET  r0    4                 # r0 = 4
5486:  SET  r1    1                 # r1 = 1
5489:  CALL 6027                    # call function beginning at 6027
5491:  EQ   r1    r0    6           # if r0 == 6, set r1 = 1, else r1 = 0
5495:  JF   r1    5579              # if r1 == 0 jump to 5579
5498:  PUSH r0   
5500:  PUSH r1   
5502:  PUSH r2  
```
From this snippet, it looks like `r0` and `r1` will be set as `4` and `1` respectively
before calling the function shown above. After that function returns, if `r0`
equals `6`, `r1` will be set to `1`, otherwise it will be `0`. Finally, if `r1`
is `0`, the code will jump to 5579, which is what presumably happens for all
inputs except the correct one. Thus, the aim is to make `r0` equal to `6` which
will allow the code to continue to instruction 5498

The solutions I read all referenced the Ackermann function, but I decided to
circumvent that part by forcing `r0` to be `6` by altering the instructions
`5483` and `5486`. As seen in the partial pseudocode for the function at `6027`:

```python
def func():
    if r0 == 0:
        r0 = r1 + 1
        return
    else:
        if r1 == 0:
            r0 = (r0 - 1) mod 32768
            r1 = r7
            func()
            return
    // --snip--
```

Observe that the shortest path to return from this function is within the first
`if` branch, where `r0` is `0` initially and will be set to `r1 + 1` before
returning. Thus, if we manually set `r0` to `0` and `r1` as `5`, `r0` will be
`6` after calling the function, which allows us to continue to the next section.

I added a command to change these values before using the teleporter called
`rewire teleporter` which can be used whenever the virtual machine is
expecting input, but this is best used only once it is needed to avoid
unexpected side effects. Again, probably not the solution the creators
intended, but I will take a deeper look at other solutions if time permits.
 
**TLDR:** this section requires us to manually manipulate the values within
the binary before using the teleporter, and the following snippet should do
the trick, assuming all steps are followed to collect the previous codes.

```
rewire teleporter
use teleporter
```

## 8th Code

TODO
