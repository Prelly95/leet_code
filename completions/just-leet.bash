# Bash tab-completion for the leet-code justfile.
#
# Completes recipe names, and completes problem names for the `run` and `edit`
# recipes so you can `just run <TAB>` through the problem set.
#
# Install (add to ~/.bashrc, at the end so it registers after bash-completion):
#   source /home/patrick/Projects/python_playground/leet_code/completions/just-leet.bash
#
# Registering a completion for `just` here stops bash-completion's lazy loader
# from replacing it with just's built-in completion (which can't complete
# recipe arguments). In other repos it still completes recipe names via
# `just --summary`; the problem-name completion is simply empty there.

_just_leet_complete() {
    local cur recipe i
    cur="${COMP_WORDS[COMP_CWORD]}"

    # The recipe is the first non-flag word after `just`, before the cursor.
    recipe=""
    for ((i = 1; i < COMP_CWORD; i++)); do
        case "${COMP_WORDS[i]}" in
            -*) ;;  # skip flags like --justfile
            *)
                recipe="${COMP_WORDS[i]}"
                break
                ;;
        esac
    done

    # No recipe yet -> complete the recipe name itself.
    if [ -z "$recipe" ]; then
        mapfile -t COMPREPLY < <(compgen -W "$(just --summary 2>/dev/null)" -- "$cur")
        return 0
    fi

    # Recipes that take a problem name as their argument.
    case "$recipe" in
        run | debug | edit)
            mapfile -t COMPREPLY < <(compgen -W "$(just _problems 2>/dev/null)" -- "$cur")
            ;;
        *)
            COMPREPLY=()
            ;;
    esac
    return 0
}

complete -F _just_leet_complete just
