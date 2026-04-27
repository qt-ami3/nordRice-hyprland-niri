### Disclaimer!

Because of the volitile and unique nature of a users Zen browser config, aswell as safety concerns, I will not be including a guide or any files to my Zen config. However, achieving a similar look is possible with minimal effort;

Go to zen browser settings; and search "color" change the website appearence to dark and set website contrast to custon. Under custom, select manage colors;

    Text: #d8dee9
    Background: #2e3440
    Unvisited Links: #81a1c1
    Visited Links: #b48ead

Because I cannot guarentee the rights to any of the wallpapers used, you will need to find and configure your own.
    
    https://github.com/linuxdotexe/nordic-wallpapers/tree/master/wallpapers

Next type about:config into the url-bar, search for zen.theme.gradient.show-custom-colorsand set it to "true".

    Right click your tab-bar.
    At the bottom click on edit theme.
    Click on custom color.
    Click the plus icon under custom.
    add #2e3440
    Repeat first three steps it the color picker closed
    And click on plus button next to the colored rectangle.

If you wanna go the extra mile install Sine Mods and install the Nebula mod and Zen Custom URL Bar.

other utilities such as btop and nvim are trivial to install and not usefull to everyone following this README so I will leave them out, know that btop includes a set of themes by default with a nord theme and the nvchad mod for nvim has the same thing with space->t->h.

### Programs used
zen-browser, fish, fastfetch, hyprland or niri, kitty, legcord(The custom discord used in screen-shots.), starship, and waybar.

To install:

Omit niri or hyprland depending on what you plan on using.

legcord has an appimage at: https://github.com/Legcord/Legcord/releases/tag/v1.2.4

Arch based - ```sudo pacman -S fish fastfetch hyprland kitty starship waybar``` **for arch the best way to install legcord is using the arch user repository, this is beyond the scope of this README. Please refer to the yay installation guide; https://github.com/Jguer/yay**

ubuntu based **Not recommended** - **legcord had a .deb file at github.com/Legcord/Legcord/releases, hyprland & niri is not in any stable repo. ```sudo apt install fish fastfetch kitty waybar && curl -sS https://starship.rs/install.sh | sh && cd Downloads/ && sudo apt install ./<downloaded-file>.deb``` 

fedora based - ```sudo dnf install fish fastfetch hyprland kitty starship waybar && sudo dnf copr enable yalter/niri && sudo dnf install niri```

gentoo based - ```sudo emerge -av app-shells/fish app-misc/fastfetch x11-terms/kitty app-shells/starship gui-apps/waybar && sudo eselect repository enable guru && sudo emaint sync -r guru && sudo emerge -av gui-wm/hyprland``` **replace gui-wm/hyprland with gui-wm/niri for niri**

### Backing up your config

Before starting config, its best practice to backup your existing .config directory;

```cd && mkdir bak && cp -rf .config bak/```

If you are curious or not in the know;

    cd Is used to navigate through folders in the Linux terminal, but alone it just returns you to your user directory.
    
    mkdir bak Makes a folder labeled bak in the current folder.
    
    && Tells the shell this is the start of a new command.
    
    cp -rf .config bak/ Copies the .config folder into the bak folder with with the arguments r for recursive and f for folder: copy -recursivefolder folderToCopy directoryToReceive.

To restore your backup;

```cd && rm -rf .config && cp -rf bak/.config/ /home/yourUserName/```

rm is remove and uses the same argument flags as cp. If you are unsure of your user name, enter "whoami" into the terminal.

### Configuration

Legcord is actually a special case because you need to edit the quickcss with the associated file provided under the "vencord" settings and upload/select both the nord and nordic themes under legcord.

I cannot foresee the edge cases most systems might run into having been a rice tailor made for my Thinkpad x1 yoga gen 6. With that said, the main pressure point is going to be in the hyprland and niri config file's resolution settings and scaling.

as far as general UX is concerned here is the software utilized which will need to be installed or reworked depending on your system;

    - powerprofilesctl daemon for the power-mode toggle.
    - pamixer for the volume controls.
    - swww-daemon or awww-daemon for the wallpaper.
    
### Credits:

- waybar [diinki-retrofuture](https://github.com/diinki/diinki-retrofuture) (MIT License)

- Maple Mono [maple-font](https://github.com/subframe7536/maple-font) (SIL Open Font License)

- Wofi Nord Theme [alxndr15/wofi-nord-theme](https://github.com/alxndr13/wofi-nord-theme) (MIT License)

- NvChad [NvChad/NvChad](https://github.com/NvChad/NvChad) (GPL-3.0 license)

- starship.toml [geoffjay/starship.toml](https://gist.github.com/geoffjay/363e3b6414d651303a2b1bec1319d936) (ISC license)
