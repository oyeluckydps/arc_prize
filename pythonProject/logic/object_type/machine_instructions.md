# Machine Instructions for ARC Prize Solution

## Overview

This document outlines the steps and tasks to be taken to achieve the objectives mentioned in the `instructions.md` file for the ARC Prize contest solution.

## Steps and Tasks

1. **Define Core Classes**
    - Define the following classes: `Cell`, `Grid`, `Pattern`, `Group`, `SuperGroup`, and `Constellation`.
    - Each class should have the necessary properties and methods as described in the `instructions.md` file.

2. **Inheritance and Properties**
    - Implement inheritance for the classes where applicable.
    - Add a probability field to each class, representing the raw occurrence probability in an unseen problem.
    - Add a field for properties applicable to each class. These properties should be functions that return the value of the property when applied to an object of the class.

3. **Type Casting and Reduction Functions**
    - Provide type casting functions to cast a class to its higher abstraction level.
    - Implement a function to reduce a class to its lowest form.

4. **Pattern Segregation**
    - Implement functions to segregate patterns/shapes from a given 2D numpy matrix.

5. **Matrix Handling**
    - Implement functions to convert lists to matrices and matrices to lists.

6. **Grid Validation Logic**
    - Ensure that for each value in the combination of `i` and `j` where `0 <= i <= max(Cell_x)` and `0 <= j <= max(Cell_y)`, there must be one and only one cell in the `self.cells` list.

## Detailed Tasks

### Define Core Classes

- **Cell**
    - Represents a single cell in the grid.
    - Defined as a tuple of three elements: (x, y, color), where x is the row, y is the column, and color is the cell's color (enumerated from 0 to 9).

- **Grid**
    - Represents the entire grid.
    - A set of `Cell` objects.
    - Must contain exactly one `Cell` for each unique combination of row and column in the grid dimensions.

- **Pattern**
    - An abstraction formed by a combination of `Cell` objects.
    - Can be a subset of a `Grid`.

- **Group**
    - A collection of `Pattern` objects.

- **SuperGroup**
    - A collection of `Group` objects.

- **Constellation**
    - A collection of `SuperGroup` objects.

### Inheritance and Properties

- Implement inheritance for the classes where applicable.
- Add a probability field to each class.
- Add a field for properties applicable to each class.

### Type Casting and Reduction Functions

- Provide type casting functions to cast a class to its higher abstraction level.
- Implement a function to reduce a class to its lowest form.

### Pattern Segregation

- Implement functions to segregate patterns/shapes from a given 2D numpy matrix.

### Matrix Handling

- Implement functions to convert lists to matrices and matrices to lists.

