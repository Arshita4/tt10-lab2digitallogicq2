# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Test case 1: All zeros (special case)
    dut._log.info("Test case 1: All zeros")
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0xF0, f"Expected 0xF0, got {dut.uo_out.value}"

    # Test case 2: First '1' at bit 15 (MSB)
    dut._log.info("Test case 2: First '1' at bit 15")
    dut.ui_in.value = 0b10000000  # Bits [15:8]
    dut.uio_in.value = 0b00000000  # Bits [7:0]
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 15, f"Expected 15, got {dut.uo_out.value}"

    # Test case 3: First '1' at bit 8
    dut._log.info("Test case 3: First '1' at bit 8")
    dut.ui_in.value = 0b00000000  # Bits [15:8]
    dut.uio_in.value = 0b10000000  # Bits [7:0]
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 8, f"Expected 8, got {dut.uo_out.value}"

    # Test case 4: First '1' at bit 0 (LSB)
    dut._log.info("Test case 4: First '1' at bit 0")
    dut.ui_in.value = 0b00000000  # Bits [15:8]
    dut.uio_in.value = 0b00000001  # Bits [7:0]
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0, f"Expected 0, got {dut.uo_out.value}"

    # Test case 5: First '1' at bit 12
    dut._log.info("Test case 5: First '1' at bit 12")
    dut.ui_in.value = 0b00010000  # Bits [15:8]
    dut.uio_in.value = 0b00000000  # Bits [7:0]
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 12, f"Expected 12, got {dut.uo_out.value}"

    # Test case 6: First '1' at bit 7
    dut._log.info("Test case 6: First '1' at bit 7")
    dut.ui_in.value = 0b00000001  # Bits [15:8]
    dut.uio_in.value = 0b00000000  # Bits [7:0]
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 7, f"Expected 7, got {dut.uo_out.value}"

    # Test case 7: All ones
    dut._log.info("Test case 7: All ones")
    dut.ui_in.value = 0b11111111  # Bits [15:8]
    dut.uio_in.value = 0b11111111  # Bits [7:0]
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 15, f"Expected 15, got {dut.uo_out.value}"
    
