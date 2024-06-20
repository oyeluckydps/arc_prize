# Machine Instructions for ARC Prize Solution

## Steps and Tasks

1. **Define Core Classes**
    - Define the following classes: `Cell`, `Grid`, `Pattern`, `Group`, `SuperGroup`, and `Constellation`.
    - Each class should have the necessary properties and methods.

2. **Inheritance and Properties**
    - Implement inheritance for the classes where applicable.
    - Add a probability field to each class.
    - Add a field for properties applicable to each class.

3. **Type Casting and Reduction Functions**
    - Provide type casting functions to cast a class to its higher abstraction level.
    - Implement a function to reduce a class to its lowest form.

4. **Grid Validation Logic**
    - Ensure that for each value in the combination of `i` and `j` where `0 <= i <= max(Cell_x)` and `0 <= j <= max(Cell_y)`, there must be one and only one cell in the `self.cells` list.
