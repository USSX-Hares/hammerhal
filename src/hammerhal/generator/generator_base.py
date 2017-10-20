import datetime
import threading
import time
from io import BytesIO

import PIL
from PIL import Image, ImageTk
from logging import getLogger

from tkinter import Tk, filedialog

import clr
clr.AddReference("System.Windows.Forms")
import System
from System.Windows.Forms import Form, Application

class GeneratorBase():
    generator_type = None
    attached_class = None

    update_timeout = 0

    __update_requested = False
    __update_on_cooldown = False

    base = None
    compiler = None
    form = None

    all_modules = None


    # Controls
    SplitterControl = None
    previewPictureBox = None
    previewLabel = None
    moduleSelectorTabControl = None

    generatorMenuStrip = None;
    fileToolStripMenuItem = None;
    newToolStripMenuItem = None;
    openToolStripMenuItem = None;
    saveToolStripMenuItem = None;
    saveAsToolStripMenuItem = None;
    closeToolStripMenuItem = None;
    compileToolStripMenu = None;
    refreshToolStripMenuItem = None;
    compileToolStripMenuItem = None;
    compileAsToolStripMenuItem = None;

    logger = None

    def __init__(self):
        self.__init_compiler()
        self.__init_form()
        # self.__init_modules()
        self.new()



    def __init_compiler(self):
        self.compiler = self.attached_class()

        _logger_name = "hammerhal.generator.{type}_generator".format \
        (
            type = self.generator_type,
        )
        self.logger = getLogger(_logger_name)

        self.logger.info("Compiler object created: {0}".format(self.compiler))
        self.compiler.create()


    def __init_form(this):
        this.form = Form()

        this.SplitterControl = System.Windows.Forms.SplitContainer()
        this.previewPictureBox = System.Windows.Forms.PictureBox()
        # this.previewPictureBox = System.Windows.Forms.Label()
        this.previewLabel = System.Windows.Forms.Label()
        this.moduleSelectorTabControl = System.Windows.Forms.TabControl()
        ((System.ComponentModel.ISupportInitialize)(this.SplitterControl)).BeginInit()
        this.SplitterControl.Panel1.SuspendLayout()
        this.SplitterControl.Panel2.SuspendLayout()
        this.SplitterControl.SuspendLayout()
        ((System.ComponentModel.ISupportInitialize)(this.previewPictureBox)).BeginInit()
        this.moduleSelectorTabControl.SuspendLayout()
        this.form.SuspendLayout()

        #
        # SplitterControl
        #
        this.SplitterControl.Dock = System.Windows.Forms.DockStyle.Fill
        this.SplitterControl.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
        this.SplitterControl.Location = System.Drawing.Point(0, 24);
        this.SplitterControl.Name = "SplitterControl"

        #
        # SplitterControl.Panel1
        #
        this.SplitterControl.Panel1.Controls.Add(this.previewPictureBox)
        this.SplitterControl.Panel1.Controls.Add(this.previewLabel)
        this.SplitterControl.Panel1.Resize += System.EventHandler(this.previewPanel_Resize);

        #
        # SplitterControl.Panel2
        #
        this.SplitterControl.Panel2.Controls.Add(this.moduleSelectorTabControl)
        this.SplitterControl.Size = System.Drawing.Size(679, 502)
        this.SplitterControl.SplitterDistance = 441
        this.SplitterControl.TabIndex = 0

        #
        # previewPictureBox
        #
        this.previewPictureBox.Location = System.Drawing.Point(3, 35)
        this.previewPictureBox.Name = "previewPictureBox"
        this.previewPictureBox.Size = System.Drawing.Size(431, 460)
        this.previewPictureBox.TabIndex = 1
        this.previewPictureBox.TabStop = False

        #
        # previewLabel
        #
        this.previewLabel.Anchor = \
            System.Windows.Forms.AnchorStyles.Top \
            | System.Windows.Forms.AnchorStyles.Left \
            | System.Windows.Forms.AnchorStyles.Right
        this.previewLabel.Location = System.Drawing.Point(3, 9)
        this.previewLabel.Name = "previewLabel"
        this.previewLabel.Size = System.Drawing.Size(431, 23)
        this.previewLabel.TabIndex = 0
        this.previewLabel.Text = "Preview:"
        this.previewLabel.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        #
        # moduleSelectorTabControl
        #
        this.moduleSelectorTabControl.Dock = System.Windows.Forms.DockStyle.Fill
        this.moduleSelectorTabControl.Location = System.Drawing.Point(0, 0)
        this.moduleSelectorTabControl.Name = "moduleSelectorTabControl"
        this.moduleSelectorTabControl.SelectedIndex = 0
        this.moduleSelectorTabControl.Size = System.Drawing.Size(230, 498)
        this.moduleSelectorTabControl.TabIndex = 0
        #
        # GeneratorForm
        #
        this.form.AutoScaleDimensions = System.Drawing.SizeF(6.0, 13.0)
        this.form.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        this.form.ClientSize = System.Drawing.Size(679, 502)
        this.form.Controls.Add(this.SplitterControl)
        this.form.Name = "GeneratorForm"
        this.form.Text = "{type} Generator".format(type=this.generator_type.capitalize())
        this.form.FormClosing += this.GeneratorForm_FormClosing;

        this.SplitterControl.Panel1.ResumeLayout(False)
        this.SplitterControl.Panel2.ResumeLayout(False)
        ((System.ComponentModel.ISupportInitialize)(this.SplitterControl)).EndInit()
        this.SplitterControl.ResumeLayout(False)
        ((System.ComponentModel.ISupportInitialize)(this.previewPictureBox)).EndInit()
        this.moduleSelectorTabControl.ResumeLayout(False)
        this.form.ResumeLayout(False)

        this._add_menu()


    def _add_menu(this):

        this.generatorMenuStrip = System.Windows.Forms.MenuStrip();

        #
        # generatorMenuStrip
        #
        this.generatorMenuStrip.Location = System.Drawing.Point(0, 0);
        this.generatorMenuStrip.Name = "generatorMenuStrip";
        this.generatorMenuStrip.Size = System.Drawing.Size(663, 24);
        this.generatorMenuStrip.TabIndex = 2;
        this.generatorMenuStrip.Text = "generatorMenuStrip";

        this.__add_menu_file();
        this.__add_menu_compile();
        this.form.Controls.Add(this.generatorMenuStrip);
    def __add_menu_file(this):

        this.fileToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem();
        this.newToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem();
        this.openToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem();
        this.saveToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem();
        this.saveAsToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem();
        this.closeToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem();

        #
        # fileToolStripMenuItem
        #
        this.fileToolStripMenuItem.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
        [
            this.newToolStripMenuItem,
            this.openToolStripMenuItem,
            this.saveToolStripMenuItem,
            this.saveAsToolStripMenuItem,
            this.closeToolStripMenuItem,
        ]));
        this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
        this.fileToolStripMenuItem.Size = System.Drawing.Size(37, 20);
        this.fileToolStripMenuItem.Text = "File";

        #
        # newToolStripMenuItem
        #
        this.newToolStripMenuItem.Name = "newToolStripMenuItem";
        this.newToolStripMenuItem.ShortcutKeys = System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.N;
        this.newToolStripMenuItem.Size = System.Drawing.Size(186, 22);
        this.newToolStripMenuItem.Text = "New";
        this.newToolStripMenuItem.Click += System.EventHandler(this.newToolStripMenuItem_Click);

        #
        # openToolStripMenuItem
        #
        this.openToolStripMenuItem.Name = "openToolStripMenuItem";
        this.openToolStripMenuItem.ShortcutKeys = System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.O;
        this.openToolStripMenuItem.Size = System.Drawing.Size(186, 22);
        this.openToolStripMenuItem.Text = "Open";
        this.openToolStripMenuItem.Click += System.EventHandler(this.openToolStripMenuItem_Click);

        #
        # saveToolStripMenuItem
        #
        this.saveToolStripMenuItem.Name = "saveToolStripMenuItem";
        this.saveToolStripMenuItem.ShortcutKeys = System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.S;
        this.saveToolStripMenuItem.Size = System.Drawing.Size(186, 22);
        this.saveToolStripMenuItem.Text = "Save";
        this.saveToolStripMenuItem.Click += System.EventHandler(this.saveToolStripMenuItem_Click);

        #
        # saveAsToolStripMenuItem
        #
        this.saveAsToolStripMenuItem.Name = "saveAsToolStripMenuItem";
        this.saveAsToolStripMenuItem.ShortcutKeys = System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.Shift | System.Windows.Forms.Keys.S;
        this.saveAsToolStripMenuItem.Size = System.Drawing.Size(186, 22);
        this.saveAsToolStripMenuItem.Text = "Save As";
        this.saveAsToolStripMenuItem.Click += System.EventHandler(this.saveAsToolStripMenuItem_Click);

        #
        # closeToolStripMenuItem
        #
        this.closeToolStripMenuItem.Name = "closeToolStripMenuItem";
        this.closeToolStripMenuItem.ShortcutKeys = System.Windows.Forms.Keys.Alt | System.Windows.Forms.Keys.F4;
        this.closeToolStripMenuItem.Size = System.Drawing.Size(186, 22);
        this.closeToolStripMenuItem.Text = "Close";
        this.closeToolStripMenuItem.Click += System.EventHandler(this.closeToolStripMenuItem_Click);

        this.generatorMenuStrip.Items.Add(this.fileToolStripMenuItem);
    def __add_menu_compile(this):

        this.compileToolStripMenu = System.Windows.Forms.ToolStripMenuItem();
        this.refreshToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem();
        this.compileToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem();
        this.compileAsToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem();

        #
        # compileToolStripMenu
        #
        this.compileToolStripMenu.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
        [
            this.refreshToolStripMenuItem,
            this.compileToolStripMenuItem,
            this.compileAsToolStripMenuItem,
        ]));
        this.compileToolStripMenu.Name = "compileToolStripMenu";
        this.compileToolStripMenu.Size = System.Drawing.Size(64, 20);
        this.compileToolStripMenu.Text = "Compile";

        #
        # compileToolStripMenuItem
        #
        this.refreshToolStripMenuItem.Name = "refreshToolStripMenuItem";
        this.refreshToolStripMenuItem.ShortcutKeys = System.Windows.Forms.Keys.F5;
        this.refreshToolStripMenuItem.Size = System.Drawing.Size(159, 22);
        this.refreshToolStripMenuItem.Text = "Refresh";
        this.refreshToolStripMenuItem.Click += System.EventHandler(this.refreshToolStripMenuItem_Click);

        #
        # compileToolStripMenuItem
        #
        this.compileToolStripMenuItem.Name = "compileToolStripMenuItem";
        this.compileToolStripMenuItem.ShortcutKeys = System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.E;
        this.compileToolStripMenuItem.Size = System.Drawing.Size(159, 22);
        this.compileToolStripMenuItem.Text = "Compile";
        this.compileToolStripMenuItem.Click += System.EventHandler(this.compileToolStripMenuItem_Click);

        #
        # compileAsToolStripMenuItem
        #
        this.compileAsToolStripMenuItem.Name = "compileAsToolStripMenuItem";
        this.compileAsToolStripMenuItem.Size = System.Drawing.Size(159, 22);
        this.compileAsToolStripMenuItem.Text = "Compile...";
        this.compileAsToolStripMenuItem.Click += System.EventHandler(this.compileAsToolStripMenuItem_Click);

        this.generatorMenuStrip.Items.Add(this.compileToolStripMenu);

    def __init_modules(self):
        self.compiler.compile()

        self.moduleSelectorTabControl.Controls.Clear()
        self.all_modules = [ (index, self.compiler.initialized_modules[index].module_name) for index in sorted(self.compiler.initialized_modules)]
        for index, module_name in self.all_modules:
            try:
                module_tab = self.compiler.initialized_modules[index].create_generator_tab(self.__update_command)
            except NotImplementedError:
                self.logger.warning("Module {name} not implemented".format(name=module_name))
            else:
                self.moduleSelectorTabControl.Controls.Add(module_tab)

    def update_preview(self):
        if (self.__update_on_cooldown):
            self.logger.debug("Update on cooldown")

            if (not self.__update_requested):
                self.logger.debug("Update scheduled")
                self.__update_requested = True
            else:
                self.logger.debug("Update already scheduled")

        else:
            thr = threading.Thread(target=self.__update_command, args=(), kwargs={ })
            thr.start()

    def __update_command(self):
        self.__update_on_cooldown = True
        _start = datetime.datetime.now()

        self.logger.debug("Preview update: starting")

        imagefile = BytesIO()
        if not (self.compiler.compiled):
            self.logger.warning("Preview update: compile unsuccessful, cannot update preview")
        else:
            self.logger.debug("Preview update: calculation new size")
            _w, _h = self.compiler.compiled.size
            _cont_w, _cont_h = (self.previewPictureBox.Parent.Width - 6, self.previewPictureBox.Parent.Height - 38)
            _scale = min(_cont_w / _w, _cont_h / _h)
            _new_w, _new_h = (int(_w * _scale), int(_h * _scale))
            _x, _y = ( (_cont_w - _new_w) // 2 + 3, (_cont_h - _new_h) // 2 + 35)
            self.logger.debug("Preview update: resizing image")
            _image = self.compiler.compiled.resize((_new_w, _new_h), PIL.Image.ANTIALIAS)
            _image.save(imagefile, format='PNG')
            _bytes = imagefile.getvalue()
            _bytearr = System.Array[System.Byte](_bytes)
            self.logger.debug("Preview update: sending bytes to the picture box")
            mstr = System.IO.MemoryStream(_bytearr);
            self.previewPictureBox.Image = System.Drawing.Image.FromStream(mstr);
            self.logger.debug("Preview update: resizing picture box ({0} -> {1})".format((self.previewPictureBox.Width, self.previewPictureBox.Height), (_new_w, _new_h)))
            self.previewPictureBox.Width = _new_w
            self.previewPictureBox.Height = _new_h
            self.logger.debug("Preview update: relocating picture box ({0} -> {1})".format((self.previewPictureBox.Left, self.previewPictureBox.Top), (_x, _y)))
            self.previewPictureBox.Left = _x
            self.previewPictureBox.Top = _y
            _time = datetime.datetime.now()
            self.logger.debug("Preview update: done. Time spent: {0}ms".format((_time - _start).total_seconds() * 1000))

        thr = threading.Thread(target=self.__delayed_update, args=(), kwargs={ })
        thr.start()

    def __delayed_update(self):
        time.sleep(self.update_timeout)

        self.__update_on_cooldown = False
        if (self.__update_requested):
            self.__update_command()
            self.__update_requested = False


    # ==================================
    # Events
    # ==================================

    def previewPanel_Resize(self, sender, e):
        self.update_preview()

    def newToolStripMenuItem_Click(self, sender, e):
        self.new()
    def openToolStripMenuItem_Click(self, sender, e):
        root = Tk()
        root.withdraw()

        file = filedialog.askopenfilename(initialdir=self.compiler.raw_directory, defaultextension=".json", filetypes=(("JSON Files", "*.json"),))
        root.destroy()
        if (not file):
            return
        self.open(file)
    def saveToolStripMenuItem_Click(self, sender, e):
        self.save()
    def saveAsToolStripMenuItem_Click(self, sender, e):
        root = Tk()
        root.withdraw()

        file = filedialog.asksaveasfilename(initialdir=self.compiler.raw_directory, defaultextension=".json", filetypes=(("JSON Files", "*.json"),))
        root.destroy()
        if (not file):
            return
        self.save(file);
    def closeToolStripMenuItem_Click(self, sender, e):
        self.close();

    def refreshToolStripMenuItem_Click(self, sender, e):
        self.refresh()
    def compileToolStripMenuItem_Click(self, sender, e):
        self.compile()
    def compileAsToolStripMenuItem_Click(self, sender, e):
        root = Tk()
        root.withdraw()

        file = filedialog.asksaveasfilename(initialdir=self.compiler.output_directory, defaultextension=".png", filetypes=(("PNG images", "*.png"),("JPEG images", "*.jpg")))
        root.destroy()
        if (not file):
            return
        self.compile(file)

    def GeneratorForm_FormClosing(self, sender, e):
        if (e.CloseReason == System.Windows.Forms.CloseReason.ApplicationExitCall or e.CloseReason == System.Windows.Forms.CloseReason.UserClosing):
            e.Cancel = True
            self.close()

    # ==================================
    # Public methods
    # ==================================

    def show(self):
        Application.EnableVisualStyles();
        Application.Run(self.form)

    def new(self):
        self.compiler.create()
        self.__init_modules()
        self.update_preview()
    def open(self, file):
        self.compiler.open(file)
        self.__init_modules()
        self.update_preview()
    def save(self, file=None):
        self.logger.info("Saving raw...")
        self.compiler.filename = file or self.compiler.filename
        if (not self.compiler.save_raw()):
            self.logger.error("Cannot save raw!")
            return
        self.logger.info("Saved.")

    def close(self, force=False):
        if not (force or (System.Windows.Forms.MessageBox.Show("Are you sure to close and exit? All unsaved changes would be lost.", "Confirm", System.Windows.Forms.MessageBoxButtons.OKCancel, System.Windows.Forms.MessageBoxIcon.Warning, System.Windows.Forms.MessageBoxDefaultButton.Button2) == System.Windows.Forms.DialogResult.OK)):
            return

        self.logger.debug("Closing GUI form...")
        self.form.FormClosing -= self.GeneratorForm_FormClosing
        self.form.Close();

    def compile(self, file=None):
        self.refresh()
        self.logger.info("Saving image...")

        self.compiler.compiled_filename = file or self.compiler.compiled_filename
        if (not self.compiler.save_compiled(forced_width=1080)):
            self.logger.error("Cannot save compiled image!")
            return

        self.logger.info("Saved.")
        self.update_preview()
    def refresh(self):
        self.logger.info("Compiling image...")
        if (not self.compiler.compile()):
            self.logger.error("Cannot compile image!")
            return
        else:
            self.update_preview()
