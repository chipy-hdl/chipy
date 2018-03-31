#!/usr/bin/env python3

from Chipy import *


with AddModule("gate_1"):
    clk, wen1, wen2 = AddInput("clk wen1 wen2")
    addr1, addr2 = AddInput("addr1 addr2", 2)
    rdata1, rdata2 = AddOutput("rdata1 rdata2", 3, async=True)
    wdata = AddInput("wdata", 3)

    mem = AddMemory("mem", 3, 4, posedge=clk)

    with If(wen1):
        mem[addr1].next = wdata

    with If(wen2):
        mem[addr2].next = wdata

    rdata1.next = mem[addr1]
    rdata2.next = mem[addr2]


with open("test003.v", "w") as f:
    print("""
//@ test-sat-equiv-bmc gold gate_1 5
""", file=f)

    WriteVerilog(f)

    print("""
module gold(
  input clk, wen1, wen2,
  input [1:0] addr1, addr2,
  output [2:0] rdata1, rdata2,
  input [2:0] wdata
);
  reg [2:0] mem [0:3];
  assign rdata1 = mem[addr1];
  assign rdata2 = mem[addr2];
  always @(posedge clk) begin
    if (wen1) mem[addr1] <= wdata;
    if (wen2) mem[addr2] <= wdata;
  end
endmodule
""", file=f)

