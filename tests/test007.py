#!/usr/bin/env python3

from chipy import *


with AddModule("gate_1"):
    sel = AddInput("sel", 5)
    a, b = AddInput("a b", 8)
    y = AddOutput("y", 8, async=True)

    with Switch(sel):
        with Case( 0): y.next = -a
        with Case( 1): y.next = ~a
        with Case( 2): y.next = a + b
        with Case( 3): y.next = a - b
        with Case( 4): y.next = a << b
        with Case( 5): y.next = a >> b
        with Case( 6): y.next = a & b
        with Case( 7): y.next = a | b
        with Case( 8): y.next = a ^ b
        with Case( 9): y.next = a < b
        with Case(10): y.next = a <= b
        with Case(11): y.next = a == b
        with Case(12): y.next = a != b
        with Case(13): y.next = a >= b
        with Case(14): y.next = a > b
        with Case(15): y.next = a.reduce_and()
        with Case(16): y.next = a.reduce_or()
        with Case(17): y.next = a.reduce_xor()
        with Case(18): y.next = a.logic()
        with Case(19): y.next = Repeat(4, a[b[2:0]])
        with Default: y.next = 0


with open("test007.v", "w") as f:
    print("""
//@ test-sat-equiv-comb gold gate_1
""", file=f)

    WriteVerilog(f)

    print("""
module gold(
  input [4:0] sel,
  input [7:0] a, b,
  output reg [7:0] y
);
  always @* begin
    case (sel)
       0: y = -a;
       1: y = ~a;

       2: y = a + b;
       3: y = a - b;
       4: y = a << b;
       5: y = a >> b;
       6: y = a & b;
       7: y = a | b;
       8: y = a ^ b;

       9: y = a < b;
      10: y = a <= b;
      11: y = a == b;
      12: y = a != b;
      13: y = a >= b;
      14: y = a > b;

      15: y = &a;
      16: y = |a;
      17: y = ^a;
      18: y = !!a;

      19: y = {4{a[b[2:0]]}};

      default: y = 0;
    endcase
  end
endmodule
""", file=f)
