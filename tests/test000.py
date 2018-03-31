#!/usr/bin/env python3

from Chipy import *


with AddModule("gate_1"):
    clk = AddInput("clk")
    submode = AddInput("submode")
    a, b = AddInput("a b", 32)
    out = AddOutput("out", 32, posedge=clk)

    with If(submode):
        out.next = a - b
    with Else:
        out.next = a + b


with AddModule("gate_2"):
    clk = AddInput("clk")
    submode = AddInput("submode")
    a, b = AddInput("a b", 32)
    out = AddOutput("out", 32)
    
    AddFF(out, posedge=clk)

    with If(submode):
        out.next = a - b
    with Else:
        out.next = a + b


with AddModule("gate_3"):
    AddInput("clk")
    AddInput("submode")
    AddInput("a b", 32)
    AddOutput("out", 32)
    
    AddFF(Sig("out"), posedge=Sig("clk"))

    with If(submode):
        Assign(Sig("out"), Sig("a") - Sig("b"))
    with Else:
        Assign(Sig("out"), Sig("a") + Sig("b"))


with AddModule("gate_4"):
    clk = AddInput("clk")
    submode = AddInput("submode")
    a, b = AddInput("a b", 32)
    out = AddOutput("out", 32, posedge=clk)
    out.next = Cond(submode, a - b, a + b)


with open("test000.v", "w") as f:
    print("""
//@ test-sat-equiv-induct gold gate_1 5
//@ test-sat-equiv-induct gold gate_2 5
//@ test-sat-equiv-induct gold gate_3 5
//@ test-sat-equiv-induct gold gate_4 5
""", file=f)

    WriteVerilog(f)

    print("""
module gold(clk, submode, a, b, out);
  input clk, submode;
  input [31:0] a, b;
  output reg [31:0] out;

  always @(posedge clk) begin
    if (submode)
        out <= a - b;
    else
        out <= a + b;
  end
endmodule
""", file=f)

