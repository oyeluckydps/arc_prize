# Instructions for ARC Prize Solution
## Overview

This project aims to provide a solution for the ARC Prize contest, which involves solving pattern-based problems using artificial intelligence. Participants are tasked with developing algorithms that can interpret and transform input grids into corresponding output grids based on learned patterns and transformation rules. These problems test the AI's ability to generalize from a limited number of training examples and apply learned transformations to new, unseen test cases.
Object Types

The object_type module provides templates in the form of classes for all objects and abstractions required to solve ARC problems. The core classes include Cell, Grid, Pattern, Group, SuperGroup, and Constellation. These classes represent different levels of abstraction and complexity in the problem space.
Class Definitions

    Cell
        Represents a single cell in the grid.
        Defined as a tuple of three elements: (x, y, color), where x is the row, y is the column, and color is the cell's color (enumerated from 0 to 9).
        Example: (0, 0, 2) represents a cell at row 0, column 0, with color 2.

    Grid
        Represents the entire grid.
        A set of Cell objects.
        Must contain exactly one Cell for each unique combination of row and column in the grid dimensions.
        Example: Grid consisting of Cell objects that cover all positions in a 3x3 grid.

    Pattern
        An abstraction formed by a combination of Cell objects.
        Can be a subset of a Grid.
        Examples of patterns include squares, triangles, or continuous sets of cells of a single color.
        A single Cell can also be treated as a Pattern.

    Group
        A collection of Pattern objects.
        Examples: Multiple horizontal lines or repeated patterns following a specific rule.

    SuperGroup
        A collection of Group objects.
        Represents a higher level of abstraction.

    Constellation
        A collection of SuperGroup objects.
        Represents the highest level of abstraction in the problem space.

## Inheritance and Properties

    Each class (Cell, Pattern, Group, SuperGroup) can inherit from a higher abstraction level. For instance, a Cell can be a Pattern, and a single Pattern can also be a Group. So, it makes sense to provide a type cast for a Cell to a Pattern, and a Pattern to a Group, etc. Also a function for reducing a class to its lowest form is required. For example, if this function is provided an object of superGroup (a set of a single set of a single pattern (which is a set of multiple cells)), then the function should return an object of Pattern class as that is the lowest form of the provided object.

    All objects have a probability field, representing the raw occurrence probability in an unseen problem. This value must be between 0 and 1.
    
    All objects have another field for the properties that are applicable to the object of each of these class. For example, a Cell object has a color property, while a Pattern object may have number of cells in it as a property. Note that these properties are not necessarily unique to each class, and may be shared between classes. Furthermore, the properties are not property of the class in classical sense. Instead these are functions that when applied to an object of a class, return the value of the property.