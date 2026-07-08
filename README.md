=====Temperature Monitor and CPU Cooler Simulation=====

This project is a graphical application built with Pygame that demonstrates:

  -GUI with tabs – a two-tab interface for temperature control and information display.

  -Object-oriented programming – a CpuCooler class that renders a cooler as lines (cross or polygon).

  -Animation – continuous rotation of the cooler around its center.


Features
  Tab 1: Control

  -A slider (Scale) from 30 to 90 degrees simulating CPU temperature.

  -A text label showing the current temperature value.

  Tab 2: Information

  -Large display of the current temperature.

  -Color-coded status messages: Low, Normal, Elevated, Critical Overheat.

  Tab 3: Cooler

  -Visual display of a rotating CPU cooler.

  -Two shape modes: cross (two intersecting lines) and polygon (hexagon).

  -Buttons to switch between shapes.

  -Continuous rotation with adjustable speed.

==Project Structure==

├── README.md          

└── main.py       

===Usage===

Click on a tab to switch between views.

Drag the slider on the "Control" tab to change the temperature.

On the "Cooler" tab, click the "Cross" or "Polygon" button to change the cooler shape.

The cooler rotates continuously while the tab is active.

Implementation Details
The CpuCooler class stores position, size, color, shape type, and current rotation angle.

Rotation is performed by updating the angle on each frame (rotate() method) and recalculating line endpoints or polygon vertices.

The GUI is built entirely with Pygame primitives (rectangles, lines, text rendering) without external UI libraries.
