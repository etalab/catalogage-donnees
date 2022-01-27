#!/bin/sh -eu
# Credits: https://ops.tips/gists/shell-prefix-output-of-commands/

# Usage: ./colorize_prefix.sh prefix color command
# Eg:
#   ./colorize_prefix.sh [client] 3 "npm run dev"

# NOTE: Linux only
# See: https://linuxtidbits.wordpress.com/2008/08/11/output-color-on-bash-scripts/
# TODO: replace with ANSI color codes (more interoperable)?
color () { echo $(tput setaf $1)$2$(tput sgr0); }

# script ... preserves color output
# See: https://stackoverflow.com/a/3515296
script -q /dev/null bash -c "$3" | sed -u "s/^/$(color $2 $1) /"