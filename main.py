import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, filedialog, messagebox

from webbrowser import open_new_tab
from os import listdir, path, getcwd
from typing import Literal
from configparser import ConfigParser
from json import load

# Global Variables
APP_NAME: str = "NibPAD"
APP_DIMENSION: tuple = (1200, 500)  # (width, height)
APP_SETTINGS: str = "./settings.ini"
COLOR_PRI: str = "#19bc9b"
COLOR_SEC: str = "grey"  # 808080
PATH_ICON: str = "./icons"
with open('./contributors/contributors.json', 'r') as json_file:
    CONTRIBUTORS: dict = load(json_file)

FONT: dict = {
    "family"    : 'Consolas',
    "size"      : 12,
    "weight"    : 'normal',
    "slant"     : 'roman',
    "underline" : False,
    "overstrike": False
}
FILE_URL: str = ""
TEXT_MODIFIED: bool = False
CONFIG = ConfigParser()  # Loads user defined settings
CONFIG.read(APP_SETTINGS)

# Main Application
app = tk.Tk()

# App's Global Variables
_SCREEN_DIMENSION: tuple = (app.winfo_screenwidth(), app.winfo_screenheight())


# _FONT = font.Font(
#     family=CONFIG.get("EDITOR", "font"),
#     size=CONFIG.getint("EDITOR", "size"),
#     weight=CONFIG.get("EDITOR", "weight"),
#     slant=CONFIG.get("EDITOR", "slant"),
#     underline=CONFIG.getboolean("EDITOR", "underline"),
#     overstrike=CONFIG.getboolean("EDITOR", "overstrike")
# )


def _display_win_center(
        window: tk.Tk | tk.Toplevel,
        dimension: tuple[int, int],
        parent_dimension: tuple[int, int] | None
) -> str:
    """
    A function to display a window in the center of the screen.

    :param window: A Tkinter window or top level window object/widget.
    :type window: Tk() or Toplevel()
    :param dimension: Window's dimension in width, height.
    :type dimension: tuple(width: int, height: int)
    :param parent_dimension: Parent window's dimension over which the current window will be placed
    :type parent_dimension: tuple(width: int, height: int)
    :return: Tkinter accepted string of "WidthxHeight+X+Y" dimensions and coordination
    :rtype: str
    """
    if parent_dimension is None:
        _x_coordination = int((window.winfo_screenwidth() / 2) - (dimension[0] / 2))
        _y_coordination = int((window.winfo_screenheight() / 2) - (dimension[1] / 2))
    else:
        _x_coordination = int((parent_dimension[0] / 2) - (dimension[0] / 2))
        _y_coordination = int((parent_dimension[1] / 2) - (dimension[1] / 2))

    return f"{dimension[0]}x{dimension[1]}+{_x_coordination}+{_y_coordination}"


app.geometry(f'{APP_DIMENSION[0]}x{APP_DIMENSION[1]}')
app.wm_iconbitmap("./NibPAD.ico")
app.title(APP_NAME)  # + to be improved

# \\\ Main Menu         \\\\\\\\\\\\________________________________
app_menu = tk.Menu()

# - App icon
icon_app = tk.PhotoImage(file=f'{PATH_ICON}/NibPAD.png')

# - Menu icons
icon_files_menu = [file for file in listdir(f'{PATH_ICON}/menu/')]
icon_about, icon_acknowledge, icon_clear, icon_copy, icon_cut, icon_exit, icon_find, icon_help, icon_new, \
icon_open, icon_paste, icon_save, icon_save_as, icon_status_bar, icon_tool_bar \
    = [tk.PhotoImage(file=f'{PATH_ICON}/menu/{file}') for file in icon_files_menu]

# - Menu icons for THEME
icon_files_theme = [file for file in listdir(f'{PATH_ICON}/theme/')]
icon_theme_dark, icon_theme_light_default, icon_theme_light_plus, icon_theme_monokai, icon_theme_night_blue, \
icon_theme_red = [tk.PhotoImage(file=f'{PATH_ICON}/theme/{file}') for file in icon_files_theme]

# - Tool bar icons
icon_files_tool = [file for file in listdir(f'{PATH_ICON}/tool/')]
icon_align_center, icon_align_left, icon_align_right, icon_bold, icon_font_color, icon_font_size, \
icon_italic, icon_underline = [tk.PhotoImage(file=f'{PATH_ICON}/tool/{file}') for file in icon_files_tool]

# - About icons
icon_files_about = [file for file in listdir(f'{PATH_ICON}/about/')]
icon_cc, icon_creator, icon_github, icon_mail, icon_organization, icon_share, icon_telegram, icon_version, \
icon_website, icon_whatsapp = [tk.PhotoImage(file=f'{PATH_ICON}/about/{file}') for file in icon_files_about]

# - Contributors icons
icon_link = tk.PhotoImage(file=f'{PATH_ICON}/link.png')
icon_love = tk.PhotoImage(file=f'{PATH_ICON}/love.png')
icon_contributors = []  # stores contributors' logo from below for loop
for num, entry in enumerate(CONTRIBUTORS['thanks']):
    if entry['logo'] != "":
        # loads logo path from the contributors.json file
        globals()[f"icon{num}"] = tk.PhotoImage(file=f"./contributors{entry['logo']}")
    else:
        # sets default love icon for unavailable alias
        globals()[f"icon{num}"] = icon_love
    # updates the icon_contributors list with loaded logo variables
    icon_contributors.append(globals()[f"icon{num}"])


# - FILE menu functions
def new_file(event=None):
    global FILE_URL
    app_text_editor.delete(1.0, 'end')
    FILE_URL = ""
    app.title(f"untitled - {APP_NAME}")


def open_file(event=None):
    global FILE_URL
    FILE_URL = filedialog.askopenfilename(title="Select a file", initialdir=getcwd(),
                                          filetypes=(("Text Files (*.txt)", "*.txt"), ("All Files", "*.*")))
    try:
        with open(FILE_URL, 'r') as opened_file:
            app_text_editor.delete(1.0, 'end')
            app_text_editor.insert(1.0, opened_file.read())
            app.title(f"{path.basename(FILE_URL)} - {APP_NAME}")
    except FileNotFoundError:
        pass
    except:
        pass


def save_file(event=None):
    global FILE_URL
    try:
        text_content = app_text_editor.get(1.0, tk.END)

        if FILE_URL:
            with open(FILE_URL, 'w', encoding='utf-8') as file_to_save:
                file_to_save.write(text_content)
                # app.title(path.basename(FILE_URL))
                return True
        else:
            with filedialog.asksaveasfile(mode='w', defaultextension='*.txt',
                                          filetypes=(("Text Files (*.txt)", "*.txt"),
                                                     ("All Files", "*.*"))) as file_to_save:
                file_to_save.write(text_content)
                # app.title(path.basename(FILE_URL))
                return True
    except:
        return False


def save_as(event=None):
    try:
        with filedialog.asksaveasfile(mode='w', defaultextension='*.txt',
                                      filetypes=(("Text Files (*.txt)", "*.txt"),
                                                 ("All Files", "*.*"))) as file_to_save:
            file_to_save.write(app_text_editor.get(1.0, tk.END))
            # app.title(path.basename(str(file_to_save)))
            return True
    except:
        return False


def exit_app(event=None):
    global FILE_URL, TEXT_MODIFIED
    try:
        if TEXT_MODIFIED and len(app_text_editor.get(1.0, 'end-1c')) >= 1:
            msg = messagebox.askyesnocancel(title="Warning", message="Do you want to save the file?")
            if msg is True:
                if FILE_URL:
                    app.destroy() if save_file() else None
                else:
                    app.destroy() if save_as() else None
            elif msg is False:
                app.destroy()
            else:
                pass
        else:
            app.destroy()
    except:
        pass


# - FILE menu
file = tk.Menu(app_menu, tearoff=False)

# -- commands
file.add_command(label='  New', image=icon_new, compound=tk.LEFT, accelerator='Ctrl+N', command=new_file)
file.add_command(label='  Open', image=icon_open, compound=tk.LEFT, accelerator='Ctrl+O', command=open_file)
file.add_separator()


# - Find & Replace dialog box
def find_replace(event=None):
    dialog_box = tk.Toplevel(app)
    dialog_box.iconphoto(True, icon_find)
    dialog_box.title("Find & Replace")
    dialog_box.geometry('450x200+400+200')
    dialog_box.resizable(False, False)

    # Find function
    def find(e=None):
        what = find_entry_box.get()
        app_text_editor.tag_remove('match', 1.0, tk.END)
        match_found = 0
        if what:
            start_position = '1.0'
            while True:
                start_position = app_text_editor.search(what, start_position, tk.END)
                if not start_position:
                    messagebox.showinfo(title="Not Found",
                                        message=f"NO MATCH FOUND!\nSorry, your search query '{what}' is not found.")
                    return None
                end_position = f'{start_position}+{len(what)}c'
                app_text_editor.tag_add('match', start_position, end_position)
                match_found += 1
                start_position = end_position
                app_text_editor.tag_config('match', foreground='red', background='yellow')

    # Replace function
    def replace(e=None):
        what = find_entry_box.get()
        by_which = replace_entry_box.get()
        text_content = app_text_editor.get(1.0, tk.END)
        replaced_text_content = text_content.replace(what, by_which)
        app_text_editor.delete(1.0, tk.END)
        app_text_editor.insert(1.0, replaced_text_content)

    # Exit function
    def close(e=None):
        app_text_editor.tag_remove('match', 1.0, tk.END)
        dialog_box.destroy()

    # Label frame
    frame = ttk.LabelFrame(dialog_box, text='Find and Replace')
    frame.pack(pady=20, padx=10)

    # Find & Replace label
    ttk.Label(frame, text='Find what   ').grid(row=0, column=0, pady=8)
    ttk.Label(frame, text='Replace with').grid(row=1, column=0, pady=8)

    # Find and Replace entry boxes
    find_entry_box = ttk.Entry(frame, width=30)
    find_entry_box.grid(row=0, column=1, padx=20)
    find_entry_box.focus_set()
    find_entry_box.bind('<KeyRelease>', lambda e=None: find_button.configure(state='enabled') \
        if find_entry_box.get() else find_button.configure(state='disabled'))
    replace_entry_box = ttk.Entry(frame, width=30)
    replace_entry_box.grid(row=1, column=1, padx=20)
    replace_entry_box.bind('<KeyRelease>', lambda e=None: replace_button.configure(state='enabled') \
        if find_entry_box.get() and replace_entry_box.get() else replace_button.configure(state='disabled'))

    # Find & Replace button
    find_button = ttk.Button(frame, text="Find It", state="disabled", command=find)
    find_button.grid(row=2, column=1, pady=40, ipadx=5, padx=0, ipady=2)
    replace_button = ttk.Button(frame, text="Replace", state="disabled", command=replace)
    replace_button.grid(row=2, column=1, pady=20, ipadx=5, ipady=2)
    cancel_button = ttk.Button(frame, text="Cancel", command=close)
    cancel_button.grid(row=2, column=0, pady=20, ipadx=5, ipady=2)

    # Binds shortcut keys to the find dialog box
    dialog_box.bind('<Return>', find)
    dialog_box.bind('<Control-h>', replace)
    dialog_box.bind('<Escape>', close)

    dialog_box.protocol("WM_DELETE_WINDOW", close)
    dialog_box.mainloop()


file.add_command(label='  Save', image=icon_save, compound=tk.LEFT, accelerator='Ctrl+S', command=save_file)
file.add_command(label='  Save as', image=icon_save_as, compound=tk.LEFT, accelerator='Ctrl+Shift+S', command=save_as)
file.add_separator()

file.add_command(label='  Exit', image=icon_exit, compound=tk.LEFT, accelerator='Ctrl+W', command=exit_app)
# - EDIT menu functions


# - EDIT menu
edit = tk.Menu(app_menu, tearoff=False)

# -- commands
edit.add_command(label='  Copy', image=icon_copy, compound=tk.LEFT, accelerator='Ctrl+C',
                 command=lambda: app_text_editor.event_generate('<Control c>'))
edit.add_command(label='  Cut', image=icon_cut, compound=tk.LEFT, accelerator='Ctrl+X',
                 command=lambda: app_text_editor.event_generate('<Control x>'))
edit.add_command(label='  Paste', image=icon_paste, compound=tk.LEFT, accelerator='Ctrl+V',
                 command=lambda: app_text_editor.event_generate('<Control v>'))
edit.add_command(label='  Clear', image=icon_clear, compound=tk.LEFT, accelerator='Ctrl+Del',
                 command=lambda: app_text_editor.delete(1.0, tk.END))
edit.add_separator()
edit.add_command(label='  Find', image=icon_find, compound=tk.LEFT, accelerator='Ctrl+F', command=find_replace)

# - VIEW functions
show_toolbar = tk.BooleanVar()
show_statusbar = tk.BooleanVar()
show_toolbar.set(True)  # set default view to True
show_statusbar.set(True)  # set default view to True


def toggle_toolbar(event=None):
    global show_toolbar
    if show_toolbar:
        app_tool_bar.pack_forget()
        show_toolbar = False
    else:
        app_text_editor.pack_forget()
        app_status_bar.pack_forget()
        app_tool_bar.pack(side=tk.TOP, fill=tk.X)
        app_text_editor.pack(fill=tk.BOTH, expand=True)
        app_status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        show_toolbar = True


def toggle_statusbar(event=None):
    global show_statusbar
    if show_statusbar:
        app_status_bar.pack_forget()
        show_statusbar = False
    else:
        app_status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        show_statusbar = True


# - VIEW menu
view = tk.Menu(app_menu, tearoff=False)

# -- check buttons
view.add_checkbutton(label='  Tool bar', image=icon_tool_bar, compound=tk.LEFT,
                     onvalue=True, offvalue=False, variable=show_toolbar, command=toggle_toolbar)
view.add_checkbutton(label='  Status bar', image=icon_status_bar, compound=tk.LEFT,
                     onvalue=True, offvalue=False, variable=show_statusbar, command=toggle_statusbar)

# - THEME menu
theme = tk.Menu(app_menu, tearoff=False)

selected_color_scheme = tk.StringVar()  # to store user color scheme choice from radio buttons
color_icons = (
    # icon files for color schemes
    icon_theme_light_default,
    icon_theme_light_plus,
    icon_theme_dark,
    icon_theme_red,
    icon_theme_monokai,
    icon_theme_night_blue
)  # for easy access of color schemes icons within the radio button loop
color_schemes = {
    # "Color Scheme Name" : ('#foreground', '#background')
    "Light"     : ('#000000', '#ffffff'),
    "Light Plus": ('#212121', '#e8e8e8'),
    "Dark"      : ('#e6e6e6', '#1c1c1c'),
    "Red"       : ('#f0304a', '#facdd3'),
    "Monokai"   : ('#f08330', '#fadfca'),
    "Night Blue": ('#c7d9eb', '#08213b')
}  # color scheme dictionary


def theme_changer(predefined: tuple[str, str] | None = None):
    """
    Changes themes of the app.

    :param predefined: Last used theme.
    :type predefined: Tuple of foreground and background colors as tuple(str, str)
    :return: Nothing.
    :rtype: None
    """
    if predefined is None:
        text_color, background_color = color_schemes[selected_color_scheme.get()[2:]]
        # updates the settings file with the last user choice
        CONFIG.set("THEME", "foreground", text_color)
        CONFIG.set("THEME", "background", background_color)
        with open(APP_SETTINGS, "w") as file:
            CONFIG.write(file)
    else:
        text_color, background_color = predefined[0], predefined[1]

    app_text_editor.configure(foreground=text_color, background=background_color)


# -- radio buttons
for index, item in enumerate(color_schemes):
    theme.add_radiobutton(label="  " + item, image=color_icons[index], compound=tk.LEFT,
                          variable=selected_color_scheme, command=theme_changer)

# - HELP menu
help_option = tk.Menu(app_menu, tearoff=False)


# --commands
def about_app(event=None):
    about_window = tk.Toplevel(app)
    about_window.geometry(_display_win_center(about_window, (500, 320), (APP_DIMENSION[0], APP_DIMENSION[1])))
    about_window.resizable(False, False)
    about_window.overrideredirect(True)

    def close(e=None):
        app.attributes('-alpha', 1)
        about_window.destroy()

    frame = tk.Frame(about_window, bg="white")
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text=APP_NAME,
             font=("Arial Black", 22, "bold"), fg="grey", bg="#e8e8e8").pack(side=tk.TOP, fill=tk.BOTH, ipady=5)
    tk.Label(frame, image=icon_app, bg="white").pack(side=tk.LEFT)

    right_frame = tk.Frame(frame, bg="white")
    right_frame.pack(side=tk.RIGHT, ipadx=30)
    right_frame.columnconfigure(0, weight=1)
    right_frame.columnconfigure(1, weight=3)

    tk.Label(right_frame, bg="white", image=icon_version).grid(row=0, column=0, sticky="w")
    tk.Label(right_frame, bg="white", text="1.0.0").grid(row=0, column=1, sticky="w")
    tk.Label(right_frame, bg="white", image=icon_organization).grid(row=1, column=0, sticky="w")
    tk.Label(right_frame, bg="white", text="Passion-Lab Inc.").grid(row=1, column=1, sticky="w")
    tk.Label(right_frame, bg="white", text="Subhankar Samanta").grid(row=2, column=1, sticky="w")
    tk.Label(right_frame, bg="white", image=icon_creator).grid(row=2, column=0, sticky="w")
    tk.Label(right_frame, bg="white").grid(row=3, padx=1)
    tk.Label(right_frame, bg="white", image=icon_github).grid(row=4, column=0, sticky="w")
    tk.Label(right_frame, bg="white", cursor="hand2", text="@Passion-Lab").grid(row=4, column=1, sticky="w")
    tk.Label(right_frame, bg="white", image=icon_website).grid(row=5, column=0, sticky="w")
    tk.Label(right_frame, bg="white", cursor="hand2", text="github.com/nibpad.html").grid(row=5, column=1, sticky="w")
    tk.Label(right_frame, bg="white", image=icon_mail).grid(row=6, column=0, sticky="w")
    tk.Label(right_frame, bg="white", cursor="hand2", text="connect.subhankar@protonmail.com").grid(row=6, column=1,
                                                                                                    sticky="w")
    tk.Label(right_frame, bg="white", image=icon_whatsapp).grid(row=7, column=0, sticky="w")
    tk.Label(right_frame, bg="white", cursor="hand2", text="wa.me/...").grid(row=7, column=1, sticky="w")
    tk.Label(right_frame, bg="white", image=icon_telegram).grid(row=8, column=0, sticky="w")
    tk.Label(right_frame, bg="white", cursor="hand2", text="t.me/...").grid(row=8, column=1, sticky="w")

    about_window.bind('<Escape>', close)
    app.attributes('-alpha', 0.8)
    about_window.mainloop()


def acknowledgement(event=None):
    window = tk.Toplevel(app)
    window.geometry(_display_win_center(window, (600, 320), (APP_DIMENSION[0], APP_DIMENSION[1])))
    window.resizable(False, False)
    window.overrideredirect(True)

    def close(e=None):
        app.attributes('-alpha', 1)
        window.destroy()

    frame = tk.Frame(window, bg="white")
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Special Thanks!",
             font=("Arial Black", 22, "bold"), fg="grey", bg="white").grid(row=0, sticky="w", padx=30, pady=(20, 0))
    tk.Label(frame, text=f"Acknowledging theme who made possible for 'Passion-Lab' to bring the {APP_NAME}...",
             font=("Candara Light", 14), fg=COLOR_PRI, bg="white",
             wraplength=500, justify="left").grid(row=1, sticky="w", padx=30, pady=1)

    entry_frame = tk.Frame(frame, borderwidth=1, bg="white",
                           highlightcolor=COLOR_PRI, highlightbackground=COLOR_PRI, highlightthickness=1)
    # entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=30, pady=20)
    entry_frame.grid(row=2, pady=20, padx=30, sticky="ew")

    buttons = []
    for i, thank in enumerate(CONTRIBUTORS['thanks']):
        # reduces url length if defined total length exceeds
        total_len = 70
        if len(thank['for']) + len(thank['to']) + len(thank['url']) > total_len:
            total_len -= (len(thank['for']) + len(thank['to']))
            url_text = thank['url'][:total_len] + "..."
        else:
            url_text = thank['url']

        # frames for rows each entry
        globals()[f"row{i}"] = tk.Frame(entry_frame, background="white")
        globals()[f"row{i}"].pack(side=tk.TOP, fill=tk.X)

        # labels for each row
        tk.Label(globals()[f"row{i}"], image=icon_contributors[i], fg="grey", bg="white").pack(side=tk.LEFT)
        tk.Label(globals()[f"row{i}"], text=f"{thank['to']}", fg="black", bg="white").pack(side=tk.LEFT)
        tk.Label(globals()[f"row{i}"], text=f"({thank['for']})", fg="darkgrey", bg="white").pack(side=tk.LEFT)
        globals()[f"button{i}"] = tk.Label(globals()[f"row{i}"], image=icon_link, fg="grey", bg="white", cursor="hand2")
        globals()[f"button{i}"].pack(side=tk.LEFT)
        # globals()[f"button{i}"].bind("<Button-1>", lambda e=None: open_new_tab(thank['url']))
        buttons.append([globals()[f"button{i}"], thank['url']])
        tk.Label(globals()[f"row{i}"], text=f"{url_text}", fg="grey", bg="white", cursor="hand2").pack(side=tk.LEFT)

    # TODO: Functions should be improved to open specific link on a specific button
    # link opener events
    for button in buttons:
        pass
        # button[0].bind("<Button-1>", lambda e=None: window.clipboard_append(button[1]))

    window.bind('<Escape>', close)
    app.attributes('-alpha', 0.8)
    window.mainloop()


# -- options
help_option.add_command(label="  About NibPAD", image=icon_about, compound=tk.LEFT, command=about_app, accelerator="F1")
help_option.add_command(label="  Acknowledgement", image=icon_acknowledge, compound=tk.LEFT, command=acknowledgement,
                        accelerator="")

# - cascade menus
app_menu.add_cascade(label='File', menu=file)
app_menu.add_cascade(label='Edit', menu=edit)
app_menu.add_cascade(label='View', menu=view)
app_menu.add_cascade(label='Themes', menu=theme)
app_menu.add_cascade(label="Help", menu=help_option)

# \\\ Toolbar           \\\\\\\\\\\\________________________________
app_tool_bar = ttk.Frame(app)
app_tool_bar.pack(side=tk.TOP, fill=tk.X)

# - FONT STYLES
fonts_available = sorted(tk.font.families())  # a tuple of all fonts in the system
selected_font_family = tk.StringVar()  # to store user selected font family

# -- combobox
font_box = ttk.Combobox(app_tool_bar, width=30, textvariable=selected_font_family, state='readonly')
font_box['value'] = fonts_available
font_box.current(fonts_available.index(FONT['family']))  # set default font style to 'Consolas' indexed
font_box.grid(row=0, column=0, padx=7, pady=2)

# - FONT SIZE
selected_font_size = tk.IntVar()  # use to store user selected font size

# --combobox
font_size_box = ttk.Combobox(app_tool_bar, width=5, textvariable=selected_font_size)
font_size_box['values'] = tuple(range(8, 101))  # font sizes manually added
font_size_box.current(font_size_box['values'].index(str(FONT['size'])))  # set default font size from FONT
font_size_box.grid(row=0, column=1, padx=7, pady=2)

# - FONT BOLD
# -- button
font_bold = ttk.Button(app_tool_bar, image=icon_bold)
font_bold.grid(row=0, column=2, padx=7, pady=2)

# - FONT ITALIC
# -- button
font_italic = ttk.Button(app_tool_bar, image=icon_italic)
font_italic.grid(row=0, column=3, padx=7, pady=2)

# - FONT UNDERLINE
# -- button
font_underline = ttk.Button(app_tool_bar, image=icon_underline)
font_underline.grid(row=0, column=4, padx=7, pady=2)

# - FONT COLOR
# -- button
font_color = ttk.Button(app_tool_bar, image=icon_font_color)
font_color.grid(row=0, column=5, padx=7, pady=2)

# - ALIGN LEFT
# -- button
align_left = ttk.Button(app_tool_bar, image=icon_align_left)
align_left.grid(row=0, column=6, padx=7, pady=2)

# - ALIGN CENTER
# -- button
align_center = ttk.Button(app_tool_bar, image=icon_align_center)
align_center.grid(row=0, column=7, padx=7, pady=2)

# - ALIGN RIGHT
# -- button
align_right = ttk.Button(app_tool_bar, image=icon_align_right)
align_right.grid(row=0, column=8, padx=7, pady=2)

# \\\ Text Editor       \\\\\\\\\\\\________________________________
# app_text_editor = tk.Text(app, wrap='word', font=(FONT['family'], FONT['size'], FONT['weight']))
app_text_editor = tk.Text(app, wrap='word', font=font.Font(
    family=FONT['family'],
    size=FONT['size'],
    weight=FONT['weight'],
    slant=FONT['slant'],
    underline=FONT['underline']
))
app_text_editor.focus_set()  # for autofocus
app_text_editor.pack(fill=tk.BOTH, expand=True)

# - SCROLL BAR
text_editor_scroll_bar = tk.Scrollbar(app_text_editor)
text_editor_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_editor_scroll_bar.config(command=app_text_editor.yview)
app_text_editor.config(yscrollcommand=text_editor_scroll_bar.set)

# \\\ Status Bar        \\\\\\\\\\\\________________________________
app_status_bar = tk.Frame(app)
app_status_bar.pack(side=tk.BOTTOM, fill=tk.X)

writing_statistics = tk.Label(app_status_bar, text="Characters: 0 | Words: 0")
writing_statistics.pack(side=tk.LEFT)


def status_bar_update(event=None):
    # any mandatory argument requirement should be included on the function to bind it with
    global TEXT_MODIFIED

    if app_text_editor.edit_modified():
        TEXT_MODIFIED = True
        characters = app_text_editor.get(1.0, 'end-1c')  # get text from 1st to last index excluding newline char
        writing_statistics.configure(text=f'Characters: {len(characters)} | Words: {len(characters.split())}')

    app_text_editor.edit_modified(False)


app_text_editor.bind('<<Modified>>', status_bar_update)


# \\\ Toolbar Func      \\\\\\\\\\\\________________________________

def font_style(event=None,
               which: Literal["family", "size", "weight", "slant", "underline", "overstrike"] = ...,
               predefined: tuple[str, int, str, str, bool, bool] | None = None):
    global FONT
    print(FONT, "\n")
    text_editor_current_font_properties = tk.font.Font(font=app_text_editor['font']).actual()

    if predefined is not None:
        FONT['family'], FONT['size'], FONT['weight'], FONT['slant'], FONT['underline'], \
            FONT['overstrike'] = predefined
    else:
        match which:
            case "family":
                FONT['family'] = selected_font_family.get()
                CONFIG.set("EDITOR", "family", selected_font_family.get())
            case "size":
                FONT['size'] = selected_font_size.get()
                CONFIG.set("EDITOR", "size", str(selected_font_size.get()))
            case "weight":
                FONT['weight'] = "bold" if FONT['weight'] == "normal" else "normal"
                CONFIG.set("EDITOR", "weight", FONT['weight'])
            case "slant":
                FONT['slant'] = "italic" if FONT['slant'] == "roman" else "roman"
                CONFIG.set("EDITOR", "slant", FONT['slant'])
            case "underline":
                FONT['underline'] = True if FONT['underline'] is not True else False
                CONFIG.set("EDITOR", "underline", str(FONT['underline']))
            case "overstrike":
                FONT['overstrike'] = True if FONT['overstrike'] is not True else False
                CONFIG.set("EDITOR", "overstrike", str(FONT['overstrike']))

        with open(APP_SETTINGS, "w") as file:
            CONFIG.write(file)

    app_text_editor.configure(font=font.Font(
        font=FONT['family'], size=FONT['size'], weight=FONT['weight'], slant=FONT['slant'],
        underline=FONT['underline'], overstrike=FONT['overstrike']
    ))


font_box.bind('<<ComboboxSelected>>',
              lambda event=None: app_text_editor.configure(font=(selected_font_family.get(),
                                                                 selected_font_size.get(), FONT['weight'])))
# font_size_box.bind('<<ComboboxSelected>>',
#                    lambda event=None: app_text_editor.configure(font=(selected_font_family.get(),
#                                                                       selected_font_size.get(), FONT['weight'])))
font_size_box.bind('<<ComboboxSelected>>', lambda event=None: font_style(which="size"))

def toggle_font_style(_arg):
    """
    Use to toggle font styles of the text box.

    :param _arg: 'bold', 'italic', 'underline'
    :type _arg: str
    :return: Makes text style to be bold, italic or underline
    :rtype: None
    """

    global FONT
    text_editor_current_font_properties = tk.font.Font(font=app_text_editor['font']).actual()
    if _arg == 'bold':
        FONT['weight'] = 'bold' if text_editor_current_font_properties['weight'] == 'normal' else 'normal'
        # app_text_editor.configure(font=(selected_font_family.get(), selected_font_size.get(), FONT['weight']))
    if _arg == 'italic':
        FONT['slant'] = 'italic' if text_editor_current_font_properties['slant'] == 'roman' else 'normal'
        # app_text_editor.configure(font=(selected_font_family.get(), selected_font_size.get(), FONT['slant']))
    if _arg == 'underline':
        FONT['underline'] = 'underline' if text_editor_current_font_properties['underline'] == 0 else 'normal'

    app_text_editor.configure(font=(
        selected_font_family.get(),
        selected_font_size.get(),
        FONT['weight'] if _arg == 'bold' else FONT['slant'] if _arg == 'italic' else FONT['underline'])
    )


font_bold.configure(command=lambda: toggle_font_style('bold'))
font_italic.configure(command=lambda: toggle_font_style('italic'))
font_underline.configure(command=lambda: toggle_font_style('underline'))


def font_color_chooser():
    _foreground = tk.colorchooser.askcolor()
    app_text_editor.configure(fg=_foreground[1]) if _foreground is not None else None


font_color.configure(command=font_color_chooser)


def text_alignment(_arg):
    """
    Use to set text alignment.

    :param _arg: left, right or center
    :type _arg: str
    :return: Makes entered text to be left, center or right aligned
    :rtype: None
    """

    text_content = app_text_editor.get(1.0, 'end')
    app_text_editor.tag_config(
        _arg,
        justify=tk.LEFT if _arg == 'left' else tk.CENTER if _arg == 'center' else tk.RIGHT
    )
    app_text_editor.delete(1.0, 'end')
    app_text_editor.insert(tk.INSERT, text_content, _arg)


align_left.configure(command=lambda: text_alignment('left'))
align_center.configure(command=lambda: text_alignment('center'))
align_right.configure(command=lambda: text_alignment('right'))

# Runs last applied functions
# - applies last used Theme on program startup
theme_changer(predefined=(CONFIG.get("THEME", "foreground"), CONFIG.get("THEME", "background")))
font_style(predefined=(
    CONFIG.get("EDITOR", "family"), CONFIG.getint("EDITOR", "size"), CONFIG.get("EDITOR", "weight"),
    CONFIG.get("EDITOR", "slant"), CONFIG.getboolean("EDITOR", "underline"), CONFIG.getboolean("EDITOR", "overstrike")
))
# - applies last used Theme on program startup

# Attaches main menu to the application
app.config(menu=app_menu)

# Binds shortcut keys to the respective functions
app.bind('<Control-n>', new_file)
app.bind('<Control-o>', open_file)
app.bind('<Control-s>', save_file)
app.bind('<Control-Shift-S>', save_as)
app.bind('<Control-w>', exit_app)
app.bind('<Control-Delete>', lambda event=None: app_text_editor.delete(1.0, tk.END))
app.bind('<Control-f>', find_replace)
app.bind('<F1>', about_app)
app.bind('<Control-b>', lambda event=None: toggle_font_style('bold'))
app.bind('<Control-i>', lambda event=None: toggle_font_style('italic'))
app.bind('<Control-u>', lambda event=None: toggle_font_style('underline'))
app.bind('<Control-l>', lambda event=None: text_alignment('left'))
app.bind('<Control-e>', lambda event=None: text_alignment('center'))
app.bind('<Control-r>', lambda event=None: text_alignment('right'))

app.protocol("WM_DELETE_WINDOW", exit_app)  # app exit button function
app.mainloop()
