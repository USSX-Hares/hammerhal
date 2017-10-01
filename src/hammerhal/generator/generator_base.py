import json
import threading
import time
from io import BytesIO

from hammerhal.compilers import CompilerBase, CompilerError
import PIL
from PIL import Image, ImageTk
from logging import getLogger

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

    logger = None

    def __init__(self):
        self.__init_compiler()

        _logger_name = "hammerhal.generator.{type}_generator".format \
        (
            type = self.generator_type,
        )
        self.logger = getLogger(_logger_name)

        self.__init_form()
        self.__init_modules()
        self.update_preview()



    def __init_compiler(self):
        self.compiler = self.attached_class()
        print(self.compiler)
        # self.compiler = CompilerBase()
        self.compiler.open('chaos-sorcerer-lord')


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
        this.SplitterControl.Location = System.Drawing.Point(0, 0)
        this.SplitterControl.Name = "SplitterControl"

        #
        # SplitterControl.Panel1
        #
        this.SplitterControl.Panel1.Controls.Add(this.previewPictureBox)
        this.SplitterControl.Panel1.Controls.Add(this.previewLabel)

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
        this.previewPictureBox.Anchor = \
            System.Windows.Forms.AnchorStyles.Top \
            | System.Windows.Forms.AnchorStyles.Bottom \
            | System.Windows.Forms.AnchorStyles.Left \
            | System.Windows.Forms.AnchorStyles.Right;
        this.previewPictureBox.Location = System.Drawing.Point(3, 35)
        this.previewPictureBox.Name = "previewPictureBox"
        this.previewPictureBox.Size = System.Drawing.Size(431, 460)
        this.previewPictureBox.TabIndex = 1
        this.previewPictureBox.TabStop = False
        this.previewPictureBox.Resize += System.EventHandler(this.previewPictureBox_Resize);

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
        this.SplitterControl.Panel1.ResumeLayout(False)
        this.SplitterControl.Panel2.ResumeLayout(False)
        ((System.ComponentModel.ISupportInitialize)(this.SplitterControl)).EndInit()
        this.SplitterControl.ResumeLayout(False)
        ((System.ComponentModel.ISupportInitialize)(this.previewPictureBox)).EndInit()
        this.moduleSelectorTabControl.ResumeLayout(False)
        this.form.ResumeLayout(False)

    def __init_modules(self):
        self.compiler.compile()

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

        self.logger.debug("Updating image")

        imagefile = BytesIO()
        if not (self.compiler.compiled):
            self.logger.warning("Compile unsuccessful, cannot update preview")
            return
        _w, _h = self.compiler.compiled.size
        _scale = min(self.previewPictureBox.Width / _w, self.previewPictureBox.Height / _h)
        _image = self.compiler.compiled.resize((int(_w * _scale), int(_h * _scale)), PIL.Image.ANTIALIAS)
        _image.save(imagefile, format='PNG')
        _bytes = imagefile.getvalue()
        _bytearr = System.Array[System.Byte](_bytes)
        mstr = System.IO.MemoryStream(_bytearr);
        self.previewPictureBox.Image = System.Drawing.Image.FromStream(mstr);

        thr = threading.Thread(target=self.__delayed_update, args=(), kwargs={ })
        thr.start()

    def __delayed_update(self):
        time.sleep(self.update_timeout)

        self.__update_on_cooldown = False
        if (self.__update_requested):
            self.__update_command()
            self.__update_requested = False



    def previewPictureBox_Resize(self, sender, e):
        self.update_preview()

    def show(self):
        Application.Run(self.form)
