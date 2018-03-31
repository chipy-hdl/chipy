#!/usr/bin/env python3

from Chipy import *


def abc(addport, role):
    addport("a", 2)
    addport("b", 2)
    addport("c", 2)


with AddModule("gate_1"):
    clk = AddInput("clk")
    waddr, raddra, raddrb, raddrc = AddInput("waddr raddra raddrb raddrc", 2)
    inp = AddInput("in", abc)
    out = AddOutput("out", abc, async=True)

    mem = AddMemory("mem", abc, 4, posedge=clk)

    mem[waddr].next = inp

    out.a_.next = mem.a_[raddra]
    out.b_.next = mem.b_[raddrb]
    out.c_.next = mem.c_[raddrc]


with AddModule("gate_2"):
    clk = AddInput("clk")
    waddr, raddra, raddrb, raddrc = AddInput("waddr raddra raddrb raddrc", 2)
    inp = AddInput("in", abc)
    out = AddOutput("out", abc, async=True)

    mem = AddMemory("mem", abc, 4, posedge=clk)

    mem.a_[waddr].next = inp.a_
    mem.b_[waddr].next = inp.b_
    mem.c_[waddr].next = inp.c_

    tmp_a = AddReg("tmp_a", abc, async=True)
    tmp_b = AddReg("tmp_b", abc, async=True)
    tmp_c = AddReg("tmp_c", abc, async=True)

    tmp_a.next = mem[raddra]
    tmp_b.next = mem[raddrb]
    tmp_c.next = mem[raddrc]

    out.a_.next = tmp_a.a_
    out.b_.next = tmp_b.b_
    out.c_.next = tmp_c.c_


with open("test004.v", "w") as f:
    print("""
//@ test-sat-equiv-bmc gold gate_1 5
//@ test-sat-equiv-bmc gold gate_2 5
""", file=f)

    WriteVerilog(f)

    print("""
module gold(
  input clk,
  input [1:0] waddr, raddra, raddrb, raddrc,
  input [1:0] in__a, in__b, in__c,
  output [1:0] out__a, out__b, out__c,
);
  reg [1:0] mem_a [0:3];
  reg [1:0] mem_b [0:3];
  reg [1:0] mem_c [0:3];
  assign out__a = mem_a[raddra];
  assign out__b = mem_b[raddrb];
  assign out__c = mem_c[raddrc];
  always @(posedge clk) begin
    mem_a[waddr] <= in__a;
    mem_b[waddr] <= in__b;
    mem_c[waddr] <= in__c;
  end
endmodule
""", file=f)

