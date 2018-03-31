#!/usr/bin/env python3

from Chipy import *


with AddModule("gate_1"):
    clk = AddInput("clk")
    addr1, addr2, din = AddInput("addr1 addr2 din", 2)
    dout = AddOutput("dout", 8, async=True)

    mem1, mem2 = AddMemory("mem1 mem2", 4, 4, posedge=clk)

    mem1[addr1][addr2].next = din[1]
    mem2[addr1][addr2].next = din[0]

    dout.next = Concat([mem1[addr1], mem2[addr2]])


with open("test005.v", "w") as f:
    print("""
//@ test-sat-equiv-bmc gold gate_1 5
""", file=f)

    WriteVerilog(f)

    print("""
module gold(
  input clk,
  input [1:0] addr1, addr2, din,
  output [7:0] dout
);
  reg [3:0] mem1 [0:3];
  reg [3:0] mem2 [0:3];
  assign dout = {mem1[addr1], mem2[addr2]};
  always @(posedge clk) begin
    mem1[addr1][addr2] <= din[1];
    mem2[addr1][addr2] <= din[0];
  end
endmodule
""", file=f)
