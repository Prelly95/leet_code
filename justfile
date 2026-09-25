# LeetCode practice tasks. Run `just` to see this list.
# Tab-completion for problem names: see completions/just-leet.bash.

# Show available recipes
default:
    @just --list --unsorted

# Run one problem's tests (tab-completes), or all problems if none given
run problem='':
    @uv run leet.py run {{problem}}

# Scaffold a new problem folder
init name:
    @uv run leet.py init {{name}}

# Import a problem from its LeetCode URL (stub + examples)
add url:
    @uv run leet.py add {{url}}

# Run one problem without catching errors (mirrors the F5 debug config)
debug problem:
    @uv run leet.py debug {{problem}}

# List scaffolded problems
list:
    @uv run leet.py list

# Open a problem's solution in $EDITOR (tab-completes)
edit problem:
    @${EDITOR:-vi} problems/{{problem}}/{{problem}}.py

# (internal) problem names, one per line — used by tab completion
_problems:
    @find problems -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null | sort
