#!/usr/bin/env python3

from chipy import *


with AddModule("gate_1"):
    clk = AddInput("clk")
    out = AddOutput("out", 1, posedge=clk)
    o32 = AddOutput("out32", 32, initial=123456789, posedge=clk)
    out.next = Sig(1, 1)
    o32.next = o32

with AddModule("gate_2"):
    clk = AddInput("clk")
    out = AddOutput("out", 1, posedge=clk)
    o32 = AddOutput("out32", 32, async=True)
    out.next = ~Sig(0, 1)
    o32.next = 123456789


with open("test009.v", "w") as f:
    print("""
//@ test-sat-equiv-bmc gold gate_1 5
//@ test-sat-equiv-bmc gold gate_2 5
""", file=f)

    WriteVerilog(f)

    print("""
module gold(clk, out, out32);
  input clk;
  output reg out;
  output reg [31:0] out32;
  always @(posedge clk) begin
    out <= 1;
    out32 <= 123456789;
  end
endmodule
""", file=f)
