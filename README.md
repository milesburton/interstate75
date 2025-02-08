# 🌈 Micropython Interstate75 RGB Matrix Examples 🚦

## 📋 Overview

This repository contains a collection of Micropython code examples for driving RGB matrices using the Interstate75 framework on the Raspberry Pi Pico. These examples demonstrate various techniques, animations, and display methods for creating stunning visual effects with RGB matrix displays.

## 🛠 Prerequisites

### 💻 Hardware
- Raspberry Pi Pico
- Interstate75 RGB Matrix Framework
- RGB Matrix Display

### 💾 Software Requirements
- [Thonny IDE](https://thonny.org/) (Recommended Python IDE for MicroPython) 🐍
- MicroPython firmware for Raspberry Pi Pico

## 🚀 Getting Started

### 1. Install Thonny
1. Download Thonny from the official website: [https://thonny.org/](https://thonny.org/)
2. Install Thonny on your computer
3. Open Thonny and configure MicroPython
   - Go to Tools > Options > Interpreter
   - Select "MicroPython (Raspberry Pi Pico)"
   - Follow the on-screen instructions to install MicroPython firmware

### 2. Preparing Your Raspberry Pi Pico
- Ensure you have the latest MicroPython firmware installed
- Connect your Pico to your computer via USB
- Verify the Interstate75 framework is correctly set up

## 💡 Example Usage

### Basic Connection
```python
from interstate75 import Interstate75, DISPLAY_INTERSTATE75_64X64

# Initialize the display
display = Interstate75(DISPLAY_INTERSTATE75_64X64)
```

## 🔗 Helpful Resources
- [Pimoroni Interstate75 Documentation](https://shop.pimoroni.com/products/interstate-75)
- [MicroPython Official Website](https://micropython.org/)
- [Raspberry Pi Pico Documentation](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)
- [Miles Burton's Interstate75 GitHub Repository](https://github.com/milesburton/interstate75)

## 🤝 Contributing
Contributions are welcome! Please feel free to submit pull requests with:
- New example scripts
- Improvements to existing code
- Bug fixes
- Documentation enhancements

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

