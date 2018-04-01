#!/usr/bin/env python3

from chipy import *


with AddModule("gate_1"):
    clk = AddInput("clk")
    out = AddOutput("out", 32, posedge=clk, initial=18)
    out.next = out + 1


with AddModule("gate_2"):
    clk = AddInput("clk")
    out = AddOutput("out", 32)
    AddFF(out, posedge=clk, initial=18)
    out.next = out + 1


with open("test008.v", "w") as f:
    print("""
//@ test-sat-equiv-induct gold gate_1 5
//@ test-sat-equiv-induct gold gate_2 5
""", file=f)

    WriteVerilog(f)

    print("""
module gold(clk, out);
  input clk;
  output reg [31:0] out;
  initial begin
    out = 18;
  end
  always @(posedge clk) begin
    out <= out + 1;
  end
endmodule
""", file=f)
