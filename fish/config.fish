if status is-interactive
    # Commands to run in interactive sessions can go here
end

set -g fish_greeting '"don'\''t listen to everybody, you should pick very specific people that you listen to."
-diinki'


bind pagedown accept-autosuggestion
bind pageup accept-autosuggestion

starship init fish | source

alias v nvim
alias n nvim
alias vi nvim
alias ecex exocortex

function reboot
  sudo reboot
end

function poweroff
  sudo reboot
end

fish_add_path /home/aknu/.spicetify
