import gi
import uinput
import time
import os
import configparser
import subprocess

os.environ['GDK_BACKEND'] = 'x11'

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib


key_mapping = {uinput.KEY_ESC: "Esc", uinput.KEY_1: "1", uinput.KEY_2: "2", uinput.KEY_3: "3", uinput.KEY_4: "4", uinput.KEY_5: "5", uinput.KEY_6: "6",
    uinput.KEY_7: "7", uinput.KEY_8: "8", uinput.KEY_9: "9", uinput.KEY_0: "0", uinput.KEY_MINUS: "-", uinput.KEY_EQUAL: "=",
    uinput.KEY_BACKSPACE: "Backspace", uinput.KEY_TAB: "Tab", uinput.KEY_Q: "Q", uinput.KEY_W: "W", uinput.KEY_E: "E", uinput.KEY_R: "R",
    uinput.KEY_T: "T", uinput.KEY_Y: "Y", uinput.KEY_U: "U", uinput.KEY_I: "I", uinput.KEY_O: "O", uinput.KEY_P: "P",
    uinput.KEY_LEFTBRACE: "[", uinput.KEY_RIGHTBRACE: "]", uinput.KEY_ENTER: "Enter", uinput.KEY_LEFTCTRL: "Ctrl_L", uinput.KEY_A: "A",
    uinput.KEY_S: "S", uinput.KEY_D: "D", uinput.KEY_F: "F", uinput.KEY_G: "G", uinput.KEY_H: "H", uinput.KEY_J: "J", uinput.KEY_K: "K",
    uinput.KEY_L: "L", uinput.KEY_SEMICOLON: ";", uinput.KEY_APOSTROPHE: "'", uinput.KEY_GRAVE: "`", uinput.KEY_LEFTSHIFT: "Shift_L",
    uinput.KEY_BACKSLASH: "\\", uinput.KEY_Z: "Z", uinput.KEY_X: "X", uinput.KEY_C: "C", uinput.KEY_V: "V", uinput.KEY_B: "B",
    uinput.KEY_N: "N", uinput.KEY_M: "M", uinput.KEY_COMMA: ",", uinput.KEY_DOT: ".", uinput.KEY_SLASH: "/", uinput.KEY_RIGHTSHIFT: "Shift_R",
    uinput.KEY_KPENTER: "Enter", uinput.KEY_LEFTALT: "Alt_L", uinput.KEY_RIGHTALT: "Alt_R", uinput.KEY_SPACE: "Space", uinput.KEY_CAPSLOCK: "CapsLock",
    uinput.KEY_F1: "F1", uinput.KEY_F2: "F2", uinput.KEY_F3: "F3", uinput.KEY_F4: "F4", uinput.KEY_F5: "F5", uinput.KEY_F6: "F6",
    uinput.KEY_F7: "F7", uinput.KEY_F8: "F8", uinput.KEY_F9: "F9", uinput.KEY_F10: "F10", uinput.KEY_F11: "F11", uinput.KEY_F12: "F12",
    uinput.KEY_SCROLLLOCK: "ScrollLock", uinput.KEY_PAUSE: "Pause", uinput.KEY_INSERT: "Insert", uinput.KEY_HOME: "Home",
    uinput.KEY_PAGEUP: "PgUp", uinput.KEY_DELETE: "Del", uinput.KEY_END: "End", uinput.KEY_PAGEDOWN: "PgDn",
    uinput.KEY_RIGHT: "→", uinput.KEY_LEFT: "←", uinput.KEY_DOWN: "↓", uinput.KEY_UP: "↑", uinput.KEY_NUMLOCK: "NumLock",
    uinput.KEY_RIGHTCTRL: "Ctrl_R", uinput.KEY_LEFTMETA:"Super_L", uinput.KEY_RIGHTMETA:"Super_R",
    uinput.KEY_PRINT:"PrtSc"}

class VirtualKeyboard(Gtk.Window):
    def __init__(self):
        super().__init__(title="Virtual Keyboard", name="toplevel")

        self.set_border_width(0)
        self.set_resizable(True)
        self.set_keep_above(True)
        self.set_modal(False)
        self.set_focus_on_map(False)
        self.set_can_focus(False)
        self.set_accept_focus(False)
        self.width=0
        self.height=0

        self.CONFIG_DIR = os.path.expanduser("~/.config/vboard")
        self.CONFIG_FILE = os.path.join(self.CONFIG_DIR, "settings.conf")
        self.config = configparser.ConfigParser()

        #using windows osk colors as default
        self.bg_color = "26, 26, 26"  # background color
        self.opacity="1.0"
        self.bt_color = "51, 51, 51"  # button color
        self.text_color="201, 201, 201" #text color
        self.highlight_color="1, 116, 215" #highlight color when pressing down on something
        self.border_color="26, 26, 26" #border of the button
        self.border_width="2.0"
        self.border_radius="0.0"
        self.padding_padding="5.0"
        self.read_settings()

        self.modifiers = {
            uinput.KEY_LEFTSHIFT: False,
            uinput.KEY_RIGHTSHIFT: False,
            uinput.KEY_LEFTCTRL: False,
            uinput.KEY_RIGHTCTRL: False,
            uinput.KEY_LEFTALT: False,
            uinput.KEY_RIGHTALT: False,
            uinput.KEY_LEFTMETA: False,
            uinput.KEY_RIGHTMETA: False
        }
        self.colors = [
            ("SteamOS Button", "13,21,29"),
            ("SteamOS Text", "252,252,252"),
            ("SteamOS Highlight", "1,1,0"),
            ("SteamOS Border + BG", "31,38,46"),
            ("Windows 10 Button", "51,51,51"),
            ("Windows 10 Text", "201,201,201"),
            ("Windows 10 Highlight", "1,116,215"),
            ("Windows 10 Border + BG", "26,26,26"),
            ("GBoard Button", "255,254,254"),
            ("GBoard Text", "17,17,17"),
            ("GBoard Highlight", "27, 114, 231"),
            ("GBoard Border + BG", "232, 236, 239"),
            ("Black", "0,0,0"),
            ("Red", "255,0,0"),
            ("Pink", "255,105,183"),
            ("White", "255,255,255"),
            ("Green", "0,255,0"),
            ("Blue", "0,0,110"),
            ("Gray", "128,128,128"),
            ("Dark Gray", "64,64,64"),
            ("Orange", "255,165,0"),
            ("Yellow", "255,255,0"),
            ("Purple", "128,0,128"),
            ("Cyan", "0,255,255"),
            ("Teal", "0,128,128"),
            ("Brown", "139,69,19"),
            ("Gold", "255,215,0"),
            ("Silver", "192,192,192"),
            ("Turquoise", "64,224,208"),
            ("Magenta", "255,0,255"),
            ("Olive", "128,128,0"),
            ("Maroon", "128,0,0"),
            ("Indigo", "75,0,130"),
            ("Beige", "245,245,220"),
            ("Lavender", "230,230,250")

        ]
        if (self.width!=0):
            self.set_default_size(self.width, self.height)

        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.buttons=[]
        self.row_buttons=[]
        self.color_combobox = Gtk.ComboBoxText()
        self.text_color_combobox = Gtk.ComboBoxText()
        self.highlight_color_combobox = Gtk.ComboBoxText()
        self.border_color_combobox = Gtk.ComboBoxText()
        self.bt_color_combobox = Gtk.ComboBoxText()
        # Set the header bar as the titlebar of the window
        self.set_titlebar(self.header)
        self.create_settings()

        grid = Gtk.Grid()  # Use Grid for layout
        grid.set_row_homogeneous(True)  # Allow rows to resize based on content
        grid.set_column_homogeneous(True)  # Columns are homogeneous
        grid.set_margin_start(float(self.padding_padding))
        grid.set_margin_end(float(self.padding_padding))
        grid.set_margin_bottom(float(self.padding_padding))
        grid.set_row_spacing(float(self.padding_padding))
        grid.set_column_spacing(float(self.padding_padding))
        grid.set_name("grid")
        self.add(grid)
        self.apply_css()
        self.device = uinput.Device(list(key_mapping.keys()))

        # Define rows for keys
        rows = [
            ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Home", "End", "Del" ],
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace" ],
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
            ["CapsLock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
            ["Shift_L", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "PgUp", "↑", "PgDn"],
            ["Ctrl_L","Super_L", "Alt_L", "Space", "PrtSc", "Shift_R", "←", "↓", "→"]
        ]

        # Create each row and add it to the grid
        for row_index, keys in enumerate(rows):
            self.create_row(grid, row_index, keys)


    def create_settings(self):
        self.create_button("☰", self.change_visibility,callbacks=1)
        self.create_button("+", self.change_opacity,True,2)
        self.create_button("Opacity:")
        self.create_button( f"{self.opacity}")
        self.create_button("-", self.change_opacity, False,2)
        self.color_combobox.append_text("Change Background")
        self.color_combobox.set_active(0)
        self.color_combobox.connect("changed", self.change_color)
        self.color_combobox.set_name("combobox")
        self.header.add(self.color_combobox)
        self.bt_color_combobox.append_text("Change Button Color")
        self.bt_color_combobox.set_active(0)
        self.bt_color_combobox.connect("changed", self.bt_change_color)
        self.bt_color_combobox.set_name("combobox")
        self.header.add(self.bt_color_combobox)
        self.text_color_combobox.append_text("Change Text Color")
        self.text_color_combobox.set_active(0)
        self.text_color_combobox.connect("changed", self.change_text_color)
        self.text_color_combobox.set_name("combobox")
        self.header.add(self.text_color_combobox)
        self.highlight_color_combobox.append_text("Change Highlight Color")
        self.highlight_color_combobox.set_active(0)
        self.highlight_color_combobox.connect("changed", self.change_highlight_color)
        self.highlight_color_combobox.set_name("combobox")
        self.header.add(self.highlight_color_combobox)
        self.border_color_combobox.append_text("Change Border Color")
        self.border_color_combobox.set_active(0)
        self.border_color_combobox.connect("changed", self.change_border_color)
        self.border_color_combobox.set_name("combobox")
        self.header.add(self.border_color_combobox)
        self.create_button("+", self.change_border_width,True,2)
        self.create_button("Border Width:")
        self.create_button( f"{self.border_width}")
        self.create_button("-", self.change_border_width, False,2)
        self.create_button("+", self.change_border_radius,True,2)
        self.create_button("Border Radius:")
        self.create_button( f"{self.border_radius}")
        self.create_button("-", self.change_border_radius, False,2)
        self.create_button("+", self.change_padding_padding,True,2)
        self.create_button("Padding:")
        self.create_button( f"{self.padding_padding}")
        self.create_button("-", self.change_padding_padding, False,2)
        

        for label, color in self.colors:
            self.color_combobox.append_text(label)
            self.text_color_combobox.append_text(label)
            self.bt_color_combobox.append_text(label)
            self.highlight_color_combobox.append_text(label)
            self.border_color_combobox.append_text(label)

    def on_resize(self, widget, event):
        self.width, self.height = self.get_size()  # Get the current size after resize



    def create_button(self, label_="", callback=None, callback2=None, callbacks=0):
        button= Gtk.Button(label=label_)
        button.set_name("headbar-button")
        if callbacks==1:
            button.connect("clicked", callback)
        elif callbacks==2:
            button.connect("clicked", callback, callback2)

        if label_==self.opacity:
            self.opacity_btn=button
            self.opacity_btn.set_tooltip_text("opacity")

        if label_==self.border_width:
            self.border_width_btn=button
            self.border_width_btn.set_tooltip_text("border width")

        if label_==self.border_radius:
            self.border_radius_btn=button
            self.border_radius_btn.set_tooltip_text("border radius")

        if label_==self.padding_padding:
            self.padding_padding_btn=button
            self.padding_padding_btn.set_tooltip_text("keyboard padding")

        self.header.add(button)
        self.buttons.append(button)

    def change_visibility(self, widget=None):
        for button in self.buttons:
            if button.get_label()!="☰":
                button.set_visible(not button.get_visible())
        self.color_combobox.set_visible(not self.color_combobox.get_visible())
        self.bt_color_combobox.set_visible(not self.bt_color_combobox.get_visible())
        self.text_color_combobox.set_visible(not self.text_color_combobox.get_visible())
        self.highlight_color_combobox.set_visible(not self.highlight_color_combobox.get_visible())
        self.border_color_combobox.set_visible(not self.border_color_combobox.get_visible())

    def bt_change_color (self, widget):
        label=self.bt_color_combobox.get_active_text()
        for label_ , color_ in self.colors:
            if label_==label:
                self.bt_color = color_
        self.apply_css()

    def change_color (self, widget):
        label=self.color_combobox.get_active_text()
        for label_ , color_ in self.colors:
            if label_==label:
                self.bg_color = color_
        self.apply_css()

    def change_text_color(self, widget):
        label = self.text_color_combobox.get_active_text()
        for label_ , color_ in self.colors:
            if label_==label:
                self.text_color = color_
        self.apply_css()

    def change_highlight_color(self, widget):
        label = self.highlight_color_combobox.get_active_text()
        for label_ , color_ in self.colors:
            if label_==label:
                self.highlight_color = color_
        self.apply_css()

    def change_border_color(self, widget):
        label = self.border_color_combobox.get_active_text()
        for label_ , color_ in self.colors:
            if label_==label:
                self.border_color = color_
        self.apply_css()

    def change_opacity(self,widget, boolean):
        if (boolean):
            self.opacity = str(round(min(1.0, float(self.opacity) + 0.01),2))
        else:
            self.opacity = str(round(max(0.0, float(self.opacity) - 0.01),2))
        self.opacity_btn.set_label(f"{self.opacity}")
        self.apply_css()

    def change_border_width(self,widget, boolean):
        if (boolean):
            self.border_width = str(round(min(999, float(self.border_width) + 0.5),2))
        else:
            self.border_width = str(round(max(0, float(self.border_width) - 0.5),2))
        self.border_width_btn.set_label(f"{self.border_width}")
        self.apply_css()

    def change_border_radius(self,widget, boolean):
        if (boolean):
            self.border_radius = str(round(min(999, float(self.border_radius) + 0.5),2))
        else:
            self.border_radius = str(round(max(0, float(self.border_radius) - 0.5),2))
        self.border_radius_btn.set_label(f"{self.border_radius}")
        self.apply_css()

    def change_padding_padding(self,widget, boolean):
        if (boolean):
            self.padding_padding = str(round(min(999, float(self.padding_padding) + 0.5),2))
        else:
            self.padding_padding = str(round(max(0, float(self.padding_padding) - 0.5),2))
        self.padding_padding_btn.set_label(f"{self.padding_padding}")
        self.apply_css()

    def apply_css (self):
        provider = Gtk.CssProvider()


        css = f"""
        headerbar {{
            background-color: rgba({self.bg_color}, {self.opacity});
            border: 0px;

        }}

        headerbar button{{
            min-width: 40px;
            min-height: 40px;
            padding: 0px;
            border: 0px;
            border-radius: {self.border_radius}px;
            


        }}

        headerbar button label{{
        color: rgb({self.text_color});

        }}

        #headbar-button, #combobox button.combo {{
            background-image: none;
        }}

        #toplevel {{
            background-color: rgba({self.bg_color}, {self.opacity});




        }}

        #grid button label{{
            color: rgb({self.text_color});


        }}

        #grid button {{
                    border: {self.border_width}px solid rgba({self.border_color}, {self.opacity}) ;
                    background-image: none;
                    border-radius: {self.border_radius}px;

                }}

        button {{
            background-color: rgba({self.bt_color}, {self.opacity});
            color:rgb({self.text_color});

        }}

       #grid button:hover {{
            border: {self.border_width}px solid rgba({self.border_color}, {self.opacity});
            background-color: rgba({self.highlight_color}, {self.opacity});
            border-radius: {self.border_radius}px;
        }}

       tooltip {{
            color: white;
            padding: 5px;
        }}

       #combobox button.combo  {{

            color: rgb({self.text_color});
            padding: 5px;
        }}


        """

        try:
            provider.load_from_data(css.encode("utf-8"))
        except GLib.GError as e:
            print(f"self.bg_color: {self.bg_color}")
            print(f"self.text_color: {self.text_color}")
            print(f"CSS Error: {e.message}")
        Gtk.StyleContext.add_provider_for_screen(self.get_screen(), provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def create_row(self, grid, row_index, keys):
        col = 0  # Start from the first column
        width=0


        for key_label in keys:
            key_event = next((key for key, label in key_mapping.items() if label == key_label), None)
            if key_event:
                if key_label in ("Shift_R", "Shift_L", "Alt_L", "Alt_R", "Ctrl_L", "Ctrl_R", "Super_L", "Super_R"):
                    button = Gtk.Button(label=key_label[:-2])
                else:
                    button = Gtk.Button(label=key_label)
                button.connect("clicked", self.on_button_click, key_event)
                self.row_buttons.append(button)
                if key_label == "Space": width=12
                elif key_label == "Shift_R" : width=4
                elif key_label == "CapsLock": width=3
                elif key_label == "Shift_L" : width=4
                elif key_label == "Backspace": width=4
                elif key_label == "\\" : width=4
                elif key_label == "Enter": width=5
                elif key_label == "Del": width=1
                elif key_label == "Esc": width=1
                else: width=2

                grid.attach(button, col, row_index, width, 1)
                col += width  # Skip 4 columns for the space button

    def update_label(self, show_symbols):
        button_positions = [(16, "` ~"), (17, "1 !"), (18, "2 @"), (19, "3 #"), (20, "4 $"), (21, "5 %"), (22, "6 ^"), (23, "7 &"), (24, "8 *"), (25, "9 ("), (26, "0 )")
        , (27, "- _"), (28, "= +"),(41,"[ {"), (42,"] }"), (43,"\\ |"), (54, "; :"), (55, "' \""), (65, ", <"), (66, ". >"), (67, "/ ?"),
        (57, "Shift *SHIFT"), (76, "Shift *SHIFT")]

        for pos, label in button_positions:
            label_parts = label.split()  
            if show_symbols:
                self.row_buttons[pos].set_label(label_parts[1])
            else:
                self.row_buttons[pos].set_label(label_parts[0])

    def meta_update_label(self, capital):
        button_positions = [(72, "Super *SUPER")]

        for pos, label in button_positions:
            label_parts = label.split()  
            if capital:
                self.row_buttons[pos].set_label(label_parts[1])
            else:
                self.row_buttons[pos].set_label(label_parts[0])

    def alt_update_label(self, capital):
        button_positions = [(73, "Alt *ALT")]

        for pos, label in button_positions:
            label_parts = label.split()  
            if capital:
                self.row_buttons[pos].set_label(label_parts[1])
            else:
                self.row_buttons[pos].set_label(label_parts[0])

    def ctrl_update_label(self, capital):
        button_positions = [(71, "Ctrl *CTRL")]

        for pos, label in button_positions:
            label_parts = label.split()  
            if capital:
                self.row_buttons[pos].set_label(label_parts[1])
            else:
                self.row_buttons[pos].set_label(label_parts[0])

    def get_caps(self):
      try:
        output = subprocess.check_output(["xset", "q"], universal_newlines=True)
        for line in output.splitlines():
          if "Caps Lock:" in line:
            return "on" in line  # Returns True if "on", False if "off"
      except subprocess.CalledProcessError:
        return False

    def capslock_update_label(self):
        button_positions = [(44, "CapsLock *CAPSLOCK")]

        for pos, label in button_positions:
            label_parts = label.split()  
            if self.get_caps():
                self.row_buttons[pos].set_label(label_parts[1])
            else:
                self.row_buttons[pos].set_label(label_parts[0])

    def on_button_click(self, widget, key_event):
        # If the key event is one of the modifiers, update its state and return.
        #print(f"[DEBUG]: {key_event}")
        if key_event in self.modifiers:
            self.modifiers[key_event] = not self.modifiers[key_event]
            if(self.modifiers[uinput.KEY_LEFTSHIFT]==True and self.modifiers[uinput.KEY_RIGHTSHIFT]==True):
                self.modifiers[uinput.KEY_LEFTSHIFT]=False
                self.modifiers[uinput.KEY_RIGHTSHIFT]=False
            if(self.modifiers[uinput.KEY_LEFTSHIFT]==True or self.modifiers[uinput.KEY_RIGHTSHIFT]==True):
                self.update_label(True)
            else:
                self.update_label(False)
            if(self.modifiers[uinput.KEY_LEFTMETA]==True or self.modifiers[uinput.KEY_RIGHTMETA]==True):
                self.meta_update_label(True)
            else:
                self.meta_update_label(False)
            if(self.modifiers[uinput.KEY_LEFTALT]==True or self.modifiers[uinput.KEY_RIGHTALT]==True):
                self.alt_update_label(True)
            else:
                self.alt_update_label(False)
            if(self.modifiers[uinput.KEY_LEFTCTRL]==True or self.modifiers[uinput.KEY_RIGHTCTRL]==True):
                self.ctrl_update_label(True)
            else:
                self.ctrl_update_label(False)
            return
        # For a normal key, press any active modifiers.
        for mod_key, active in self.modifiers.items():
            if active:
                self.device.emit(mod_key, 1)

        # Emit the normal key press.
        self.device.emit(key_event, 1)
        #time.sleep(0.05)
        self.device.emit(key_event, 0)
        self.update_label(False)
        # Release the modifiers that were active.
        for mod_key, active in self.modifiers.items():
            if active:
                self.device.emit(mod_key, 0)
                self.modifiers[mod_key] = False
                self.meta_update_label(False)
                self.alt_update_label(False)
                self.ctrl_update_label(False)
        #if key_event == uinput.KEY_CAPSLOCK:
        self.capslock_update_label() #and check our caps lock symbol


    def read_settings(self):
        # Ensure the config directory exists
        try:
            os.makedirs(self.CONFIG_DIR, exist_ok=True)
        except PermissionError:
            print("Warning: No permission to create the config directory. Proceeding without it.")

        try:
            if os.path.exists(self.CONFIG_FILE):
                self.config.read(self.CONFIG_FILE)
                self.bg_color = self.config.get("DEFAULT", "bg_color", fallback="26,26,26")
                self.opacity = self.config.get("DEFAULT", "opacity", fallback="1.0" )
                self.bt_color = self.config.get("DEFAULT", "bt_color", fallback="51, 51, 51")
                self.text_color = self.config.get("DEFAULT", "text_color", fallback="201, 201, 201")
                self.highlight_color = self.config.get("DEFAULT", "highlight_color", fallback="1, 116, 215")
                self.border_color = self.config.get("DEFAULT", "border_color", fallback="26, 26, 26")
                self.border_width = self.config.get("DEFAULT", "border_width", fallback="2.0")
                self.border_radius = self.config.get("DEFAULT", "border_radius", fallback="0.0")
                self.padding_padding = self.config.get("DEFAULT", "padding_padding", fallback="5.0")
                self.width=self.config.getint("DEFAULT", "width" , fallback=0)
                self.height=self.config.getint("DEFAULT", "height", fallback=0)
                print(f"background: rgba: {self.bg_color}, {self.opacity}")
                print(f"text: rgba: {self.text_color}, {self.opacity}")

        except configparser.Error as e:
            print(f"Warning: Could not read config file ({e}). Using default values.")



    def save_settings(self):

        self.config["DEFAULT"] = {"bg_color": self.bg_color, "opacity": self.opacity, "bt_color": self.bt_color, "text_color": self.text_color, "highlight_color": self.highlight_color, "border_color": self.border_color, "border_width": self.border_width, "border_radius": self.border_radius, "padding_padding": self.padding_padding, "width": self.width, "height": self.height}

        try:
            with open(self.CONFIG_FILE, "w") as configfile:
                self.config.write(configfile)

        except (configparser.Error, IOError) as e:
            print(f"Warning: Could not write to config file ({e}). Changes will not be saved.")


if __name__ == "__main__":
    win = VirtualKeyboard()
    win.connect("destroy", Gtk.main_quit)
    win.connect("destroy", lambda w: win.save_settings())
    win.show_all()
    win.connect("configure-event", win.on_resize)
    win.change_visibility()
    Gtk.main()
