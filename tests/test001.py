#!/usr/bin/env python3

from chipy import *


with AddModule("gate_1"):
    clk = AddInput("clk")
    reverse_order = AddInput("reverse_order")
    concat_mode = AddInput("concat_mode")
    a, b = AddInput("a b", 32)
    out = AddOutput("out", 32, posedge=clk)

    with If(concat_mode):
        with If(reverse_order):
            out.next = Concat([b[15:0], a[15:0]])
        with Else:
            out.next = Concat([a[15:0], b[15:0]])
    with Else:
        with If(reverse_order):
            out.next = b - a
        with Else:
            out.next = a - b


with AddModule("gate_2"):
    clk = AddInput("clk")
    reverse_order = AddInput("reverse_order")
    concat_mode = AddInput("concat_mode")
    a, b = AddInput("a b", 32)
    out = AddOutput("out", 32, posedge=clk)

    aa, bb = AddReg("aa bb", 32, async=True)

    with If(reverse_order):
        aa.next = b
        bb.next = a
    with Else:
        aa.next = a
        bb.next = b

    with If(concat_mode):
        out.next = Concat([aa[15:0], bb[15:0]])
    with Else:
        out.next = aa - bb


with AddModule("gate_3"):
    clk = AddInput("clk")
    reverse_order = AddInput("reverse_order")
    concat_mode = AddInput("concat_mode")
    a, b = AddInput("a b", 32)
    out = AddOutput("out", 32, posedge=clk)

    aa, bb = AddReg("aa bb", 32, async=True)

    Concat([aa, bb]).next = Concat([a, b])
    with If(reverse_order):
        Concat([aa, bb]).next = Concat([b, a])

    Assign(out, Cond(concat_mode, Concat([aa[15:0], bb[15:0]]), aa - bb))


with AddModule("gate_4"):
    clk = AddInput("clk")
    reverse_order = AddInput("reverse_order")
    concat_mode = AddInput("concat_mode")
    a, b = AddInput("a b", 32)
    out = AddOutput("out", 32, posedge=clk)

    with Switch(Concat([concat_mode, reverse_order])):
        with Case(0b00): out.next = a - b
        with Case(0b01): out.next = b - a
        with Case(0b10): out.next = Concat([a[15:0], b[15:0]])
        with Case(0b11): out.next = Concat([b[15:0], a[15:0]])


with open("test001.v", "w") as f:
    print("""
//@ test-sat-equiv-induct gold gate_1 5
//@ test-sat-equiv-induct gold gate_2 5
//@ test-sat-equiv-induct gold gate_3 5
//@ test-sat-equiv-induct gold gate_4 5
""", file=f)

    WriteVerilog(f)

    print("""
module gold(clk, reverse_order, concat_mode, a, b, out);
  input clk, reverse_order, concat_mode;
  input [31:0] a, b;
  output reg [31:0] out;

  always @(posedge clk) begin
    case ({concat_mode, reverse_order})
        2'b 00: out <= a - b;
        2'b 01: out <= b - a;
        2'b 10: out <= {a[15:0], b[15:0]};
        2'b 11: out <= {b[15:0], a[15:0]};
    endcase
  end
endmodule
""", file=f)
