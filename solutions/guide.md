# Guide to Obtaining Codes

This will be a simple guide to how and where to obtain the codes required for
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

## 5th Code to 8th Code

TODO
