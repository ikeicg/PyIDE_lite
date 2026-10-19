# PyIDE_lite

A small IDE with its own language toolchain for a tiny subset of Python: a lexer, a parser, an interpreter, and an optimizing compiler that targets a stack-based virtual machine. The editor has syntax highlighting, error underlining and a console.

The language covers:
- Assignment statements
- `print(...)`, including `print(memory)` to show every variable
- Arithmetic with operator precedence and parentheses (`+ - * / **`)
- Comments

Not supported: unary operators (`-3`), strings, conditions, loops and functions.

## How it works

```
source ─► Lexer ─► Parser ─► syntax tree ─► Interpreter                 (walks the tree)
                                         └► Optimizer ─► bytecode ─► VM (stack machine)
```

- **Lexer and parser** (`components/`): the grammar is in `components/grammar.txt`. Errors report the line, column and a message, and the editor underlines the line.
- **Optimizer** (`compiler.py`): removes assignments to variables that are never read.
- **Bytecode**: a few opcodes (`LOAD_CONST`, `LOAD_NAME`, `STORE_NAME`, `BINARY_*`, `PRINT`), written to `bytecode.txt` and executed by a stack machine.

Example programs are in `pycodes/`.

## Demo

![Screenshot (239)](https://github.com/ikeicg/PyIDE_lite/assets/125681815/8665a96f-ba1e-45b9-9835-2caf64adfde3)

![Screenshot (240)](https://github.com/ikeicg/PyIDE_lite/assets/125681815/b74cfa46-0a7f-419b-a919-dbf628ebbaea)

![Screenshot (241)](https://github.com/ikeicg/PyIDE_lite/assets/125681815/5649afaa-340f-4132-bae4-ff87f887b6b7)
