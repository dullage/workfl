![PyPI](https://img.shields.io/pypi/v/workfl.svg)

# workfl

***Workf**low Markup **L**anguage*

## Introduction

workfl is a lightweight markup language for simple workflow diagrams. It's designed to be quick to write and easy to read.

Example:

```workfl
A
B
D

A
C
D
```

![Example](https://raw.githubusercontent.com/Dullage/workfl/master/docs/example.png)

You can try it out for yourself at [workfl.ws](https://workfl.ws).

The workfl python package can convert workfl markup into dictionaries of nodes and connections. There is also a method to export the workflow into [mermaid](https://mermaidjs.github.io/) syntax.

## Installation

`pip install workfl`

## Usage
```python
import workfl

markup = "A\nB"
flow = workfl.ws(markup)

print(flow.nodes)  # A dictionary of nodes
print(flow.connections)  # A dictionary of connections

mermaid = flow.to_mermaid()
print(mermaid)
```

By default `to_mermaid()` will render a chart flowing from Top to Bottom. This can be changed by declaring a `direction` e.g. `to_mermaid(direction="LR")` (Left to Right). There are 4 options:

| Option | Direction |
| -- | -- |
| TB | Top to Bottom (Default) |
| BT | Bottom to Top |
| LR | Left to Right |
| RL | Right to Left |

## Syntax

A full guide can be found here <https://workfl.ws/?help=true>.

## To Do

* Test scripts.
