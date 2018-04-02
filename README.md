
Chipy -- Constructing Hardware In PYthon
========================================

Chipy is a single-file python module for generating digital hardware. Chipy
provides a simple and clean API for writing Verilog code generators. Structural
and behavioral circuit modelling is supported.


A Simple Example
================

The following is a simple Chipy example design:

```python
    from Chipy import *

    with AddModule("ADD_OR_SUB_DEMO"):
        clk = AddInput("CLK")
        sub = AddInput("SUB")
        a, b = AddInput("A B", 32)
        out = AddOutput("OUT", 32, posedge=clk)

        with If(sub):
           out.next = a - b
        with Else:
           out.next = a + b

    with open("demo.v", "w") as f:
        WriteVerilog(f)
```

The `AddModule` function adds a new module to the design and return it. To
add elements to a module, create a `with <module>: ...` block and call the
corresponding `Add...` functions from within that block.

Many functions and expressions in Chipy code return a *signal*. E.g.
`AddInput(..)`, `AddOutput(..)`, or `a + b` in the above code. Some
signals are *registers*, which just means that they can be assigned
to, either by calling `Assign(<assignee>, <value>)` or by assigning
to the `.next` attribute, as demonstrated in the code above.

Registers also need a synchronisation element, such as a FF, assigned to them.
This can either be done by calling functions such as `AddFF(..)`, or in simple
cases using keyword arguments such as `posedge=<clk_signal>` when creating
the register itself.

Registers that are not assigned a value and/or do not have a synchronization
element will cause a runtime error in `WriteVerilog`.

Finally assignments can be conditional, enabling behavioral modelling. This is
done by putting the assignments in blocks such as `with If(..): ...` or
`with Else:`.

Here is a different version of the design, demonstrating some of the variations
mentioned so far:

```python
    from Chipy import *

    with AddModule("ADD_OR_SUB_DEMO"):
        clk = AddInput("CLK")
        sub = AddInput("SUB")
        a, b = AddInput("A B", 32)
        out = AddOutput("OUT", 32)

        with If(sub):
           Assign(out, a - b)
        with Else:
           Assign(out, a + b)

	AddFF(out, posedge=clk)

    with open("demo.v", "w") as f:
        WriteVerilog(f)
```

Chipy Reference Manual
======================

Chipy maintains a global design state that contains a set of (Verilog/RTL)
modules and a stack of design contexts. The Chipy `Add*` functions are used to
add elements to the design in memory. Chipy APIs that are used with the Python
`with` statement are used to maintain the stack of design contexts. The current
context determines for example to which module a new instance or wire should be
added. So for example, the `AddInput` function does not have a parameter that
tells it to which module to add a new input port. Instead the input port is
added to the module referenced to by the current context.


Creating modules and generating Verilog
---------------------------------------

### AddModule(name)

This function adds a new module to the design. The module created by this function
is returned. A Python `with` block using a Chipy module as argument is used to
create a new Chipy context that can be used to add elements to the module. For
example, the following will create a new module `demo` with an input port `clk`:

```python
    demo_mod = AddModule("demo")

    with demo_mod:
        AddInput("clk")
```

### Module(name=None)

This functions looks up the module with the specified name. If no such module
is found, `None` is returned. If the name parameter is omitted then the module
referenced by the current context is returned.

### WriteVerilog(f)

This function write the current design to the specified file handle. The file
has to be opened first using for example the Python `open` function:

```python
    with open("demo.v", "w") as f:
        WriteVerilog(f)
```

### ResetDesign()

This function resets the global Chipy state, e.g. for when multiple designs are
created from one Python script.


Adding inputs and outputs
-------------------------

### AddInput(name, type=1)

This function adds a new input port to the current module. The new signal is
returned. If name contains more than one white-space separated token, then
multiple ports are created at once and a list is returned. For example:

```python
    with AddModule("demo"):
        clk, a, b = AddInput("clk a b")
```

The `type` argument specifies the width of the new signal. A negative number
denotes a signed signal, i.e. the value `5` would be used to create an unsigned
5 bit wide signal, and the value `-5` would be used to create a signed 5 bit
wide signal.

Instead of an integer, an *interface* (see below) can be passed as `type` for
the new signal. In that case multiple input ports are generated, as specified by
the interface, and a *bundle* (see blow) of those signals is returned.

### AddOutput(name, type=1, posedge=None, negedge=None, nodefault=False, async=False)

Like `AddInput`, but adds and output port. The signals returned by this functions
are *registers*, i.e. they have a `.next` member that can be assigned to.

The keyword arguments `posedge`, `negedge`, and `nodefault` cause `AddOuput` to
automatically call `AddFF` (see below) on the generated registers. Similarly,
`async=True` causes `AddOuput` to call `AddAsync` (see below) on the generated
registers.

Registers and synchronization elements
--------------------------------------

### AddReg(name, type=1, posedge=None, negedge=None, nodefault=False, async=None)
### AddFF(signal, posedge=None, negedge=None, nodefault=False)
### AddAsync(signal)
### Assign(lhs, rhs)

Signals and expessions
----------------------

### Sig(arg, width=None)
### Sig Operators
### Cond(cond, if\_val, else\_val)
### Concat(args)
### Repeat(num, sig)

Bundles
-------

### Bundle(arg=None, \*\*kwargs)
### Bundle.add(self, name, member)
### Bundle.get(name)
### Bundle.regs() and Bundle.regs()
### Bundle.keys(), Bundle.values(), Bundle.items()
### Zip(bundles, recursive=False)
### Module.bundle(self, prefix="")

Interfaces
----------

### AddPort(name, type, role, posedge=None, negedge=None, nodefault=False, async=None)
### Module.intf(self, prefix="")
### Stream(data\_type, last=False, destbits=0)

Memories
--------

### AddMemory(name, type, depth, posedge=None, negedge=None)
### Memory read and write
### Memory bundles

Hierarchical Designs
--------------------

### AddInst(name, type)
### Connect(sigs)

Behavioral Modelling
--------------------

### If, ElseIf, Else
### Switch, Case, Default

Todos
=====

- Complete documentation
- More testcases / examples
- Improved error reporting
- Bundles: flat, unflat, Map, concat
- Verilog Primitive Inst
- Backbox modules
- Label(name, sig)

License
=======

Chipy -- Constructing Hardware In PYthon

Copyright (C) 2016  Clifford Wolf <clifford@clifford.at>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
