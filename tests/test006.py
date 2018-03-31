#!/usr/bin/env python3

from Chipy import *


with AddModule("gate_1"):
    sel = AddInput("sel", 2)
    din = AddInput("din", 32)
    dout = AddOutput("dout", 32, async=True)

    dout.next = 0

    with Switch(sel):
        with Case(0):
            dout[15:0].next = din[31:16]
            dout[31:16].next = din[15:0]
        with Case(1):
            dout[1].next = din[30]
            dout[7].next = ~din[20]
            dout[din[3:0]].next = din[din[7:4]]
        with Case(2):
            dout[10 + din[3:0], +5].next = din[10 + din[7:4], -5]
        with Case(3):
            dout[10 + din[3:0], -5].next = din[10 + din[7:4], +5]


with open("test006.v", "w") as f:
    print("""
//@ test-sat-equiv-comb gold gate_1
""", file=f)

    WriteVerilog(f)

    print("""
module gold(
  input [1:0] sel,
  input [31:0] din,
  output reg [31:0] dout
);
  always @* begin
    dout = 0;
    case (sel)
      0: begin
        {dout[15:0], dout[31:16]} = din;
      end
      1: begin
        dout[1] = din[30];
        dout[7] = ~din[20];
        dout[din[3:0]] = din[din[7:4]];
      end
      2: begin
        dout[10 + din[3:0] +: 5] = din[10 + din[7:4] -: 5];
      end
      3: begin
        dout[10 + din[3:0] -: 5] = din[10 + din[7:4] +: 5];
      end
    endcase
  end
endmodule
""", file=f)

