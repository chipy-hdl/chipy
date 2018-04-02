#!/usr/bin/env python3

from chipy import *


def rgbdata(addport, role):
    addport("red", 8)
    addport("green", 8)
    addport("blue", 8)

def graydata(addport, role):
    addport("gray", 8)

def rgb2gray(indata):
    rgbsum = Sig(indata.red_, 10) + Sig(indata.green_, 10) + Sig(indata.blue_, 10)
    return Bundle(gray_=(rgbsum >> 1) - (rgbsum >> 3) - (rgbsum >> 4))


with AddModule("gate_1"):
    clk = AddInput("clk")
    inp = AddPort("in", Stream(rgbdata), "sink")
    out = AddPort("out", Stream(graydata), "source")

    inp.ready_.next = inp.valid_ & (~out.valid_ | out.ready_)

    with If(out.ready_):
        out.valid_.next = 0

    with If(inp.ready_):
        out.data_.next = rgb2gray(inp.data_)
        out.valid_.next = 1

    AddAsync(inp.ready_)
    AddFF(out.regs(), posedge=clk)


with AddModule("gate_2"):
    ports = AddPort("", Module("gate_1").intf(), "child")
    inst = AddInst("inst", Module("gate_1"))
    Connect([ports, inst])


with open("test002.v", "w") as f:
    print("""
//@ test-sat-equiv-induct gold gate_1 5
//@ test-sat-equiv-induct gold gate_2 5
""", file=f)

    WriteVerilog(f)

    print("""
module gold(
  input clk,

  input [7:0] in__data__red,
  input [7:0] in__data__green,
  input [7:0] in__data__blue,
  input in__valid,
  output in__ready,

  output reg [7:0] out__data__gray,
  output reg out__valid,
  input out__ready
);
  assign in__ready = in__valid && (!out__valid || out__ready);
  wire [9:0] rgbsum = in__data__red + in__data__green + in__data__blue;
  wire [7:0] gray = (rgbsum >> 1) - (rgbsum >> 3) - (rgbsum >> 4);

  always @(posedge clk) begin
    if (out__ready) begin
      out__valid <= 0;
    end
    if (in__ready) begin
      out__data__gray <= gray;
      out__valid <= 1;
    end
  end
endmodule
""", file=f)
