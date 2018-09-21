from hammerdraw.compilers.compiler_module_base import CompilerModuleBase
from hammerdraw.config_loader import ConfigLoader
import os

from hammerdraw import generator
if (generator.generator_supported):
    import System
    import threading
    import datetime, time
    from io import BytesIO
    from shutil import copyfile
    from tkinter import Tk, filedialog
    from PIL import Image, ImageDraw

class ImageModule(CompilerModuleBase):
    module_name = "image"
    image_path = None

    def initialize(self, **kwargs):
        self.image_path = None
        super().initialize(**kwargs)

    def _compile(self, base):
        if (not self.parent.raw.get('image')):
            self.image_path = None
            return 0

        filename = self.parent.raw['image']
        if (not os.path.isfile(filename)):
            filename = "{directory}{name}".format\
            (
                directory=ConfigLoader.get_from_config('rawDirectoryRoot'),
                name=self.parent.raw['image'],
            )
            if (not os.path.isfile(filename)):
                self.logger.error("Cannot load {type} image by path: '{path}' - no such file".format(type=self.parent.compiler_type, path=self.parent.raw['image']))
                self.image_path = None
                return 0

        self.image_path = filename
        self.logger.info("Image verified")
        return 0

    def insert(self, parent_base):
        if (not self.image_path):
            return

        _x, _y = self.get_position()
        self.parent.insert_image_scaled(base_image=parent_base, region=(_x, _y, self.width, self.height), image_path=self.image_path)
        self.logger.info("Image inserted")


    ### =======================================
    ###   WinForms module generator
    ### =======================================

    imageModulePanel = None;
    imagePathBrowseButton = None;
    imagePathTextBox = None;
    imagePathLabel = None;
    imageDisabledCheckBox = None;
    imageCopyButton = None;
    imageUpdateButton = None;
    imagePreviewPictureBox = None;

    __error_state = True
    __update_preview_on_cooldown = False
    __update_requested = False
    update_preview_timeout = 0


    def _on_update(self):
        if (not self.imageModulePanel):
            return
        if (not self.image_path):
            self.setErrorState(not self.imageDisabledCheckBox.Checked)
            return

        self.setErrorState(False)
        self.update_preview()

    def update_preview(self):
        if (self.__update_preview_on_cooldown):
            self.logger.debug("Update on cooldown")

            if (not self.__update_requested):
                self.logger.debug("Update scheduled")
                self.__update_requested = True
            else:
                self.logger.debug("Update already scheduled")

        else:
            thr = threading.Thread(target=self.__update_command, args=(), kwargs={ })
            thr.start()

    def __get_preview(self, size):

        _image = Image.open(self.image_path)
        _base = Image.new("RGBA", size, 0x00ffffff)
        _base = self.parent.insert_image_scaled(base_image=_base, region=(0, 0) + size, image_path=_image, scale_func=min)

        return _base


    def __update_command(self):
        self.__update_preview_on_cooldown = True
        self.imageUpdateButton.Enabled = False

        _start = datetime.datetime.now()

        self.logger.debug("Image preview update: starting")

        imagefile = BytesIO()
        if not (self.image_path):
            self.logger.warning("Image preview update: no image to update")
        else:
            self.logger.debug("Image preview update: creating preview")
            _size = (self.imagePreviewPictureBox.Width, self.imagePreviewPictureBox.Height)
            _image = self.__get_preview(_size)
            _image.save(imagefile, format='PNG')
            _bytes = imagefile.getvalue()
            _bytearr = System.Array[System.Byte](_bytes)
            self.logger.debug("Image preview update: sending bytes to the picture box")
            mstr = System.IO.MemoryStream(_bytearr);
            self.imagePreviewPictureBox.Image = System.Drawing.Image.FromStream(mstr);

            _time = datetime.datetime.now()
            self.logger.debug("Image preview update: done. Time spent: {0}ms".format((_time - _start).total_seconds() * 1000))

        thr = threading.Thread(target=self.__delayed_update, args=(), kwargs={ })
        thr.start()

    def __delayed_update(self):
        time.sleep(self.update_preview_timeout)

        self.__update_preview_on_cooldown = False
        self.imageUpdateButton.Enabled = True
        if (self.__update_requested):
            self.__update_command()
            self.__update_requested = False


    def _create_generator_tab_content(self):
        _y = 0
        _tab_index = 0

        self.imageModulePanel = System.Windows.Forms.Panel();
        self.imagePathTextBox = System.Windows.Forms.TextBox();
        self.imagePathLabel = System.Windows.Forms.Label();
        self.imagePathBrowseButton = System.Windows.Forms.Button();
        self.imageDisabledCheckBox = System.Windows.Forms.CheckBox();
        self.imageUpdateButton = System.Windows.Forms.Button();
        self.imageCopyButton = System.Windows.Forms.Button();
        self.imagePreviewPictureBox = System.Windows.Forms.PictureBox();

        #
        # imageModulePanel
        #
        self.imageModulePanel.Anchor = \
            System.Windows.Forms.AnchorStyles.Left \
            | System.Windows.Forms.AnchorStyles.Right \
            | System.Windows.Forms.AnchorStyles.Top \
            | System.Windows.Forms.AnchorStyles.Bottom;
        self.imageModulePanel.Controls.Add(self.imagePreviewPictureBox);
        self.imageModulePanel.Controls.Add(self.imageCopyButton);
        self.imageModulePanel.Controls.Add(self.imageUpdateButton);
        self.imageModulePanel.Controls.Add(self.imageDisabledCheckBox);
        self.imageModulePanel.Controls.Add(self.imagePathBrowseButton);
        self.imageModulePanel.Controls.Add(self.imagePathTextBox);
        self.imageModulePanel.Controls.Add(self.imagePathLabel);
        self.imageModulePanel.Location = System.Drawing.Point(0, 0);
        self.imageModulePanel.Name = "imageModulePanel";
        self.imageModulePanel.Size = System.Drawing.Size(222, 429);
        self.imageModulePanel.TabIndex = 4;

        #
        # imageDisabledCheckBox
        #
        _top = 8
        self.imageDisabledCheckBox.AutoSize = True;
        self.imageDisabledCheckBox.Location = System.Drawing.Point(8, _y + _top);
        self.imageDisabledCheckBox.Name = "imageDisabledCheckBox";
        self.imageDisabledCheckBox.Size = System.Drawing.Size(71, 17);
        self.imageDisabledCheckBox.TabIndex = _tab_index;
        self.imageDisabledCheckBox.Text = "No image";
        self.imageDisabledCheckBox.UseVisualStyleBackColor = True;
        self.imageDisabledCheckBox.CheckedChanged += System.EventHandler(self.imageDisabledCheckBox_CheckedChanged);
        self.imageDisabledCheckBox.Checked = self.parent.raw.get('image', None) is None
        _y += self.imageDisabledCheckBox.Height + _top
        _tab_index += 1


        #
        # imagePathLabel
        #
        _top = 24
        self.imagePathLabel.AutoSize = True;
        self.imagePathLabel.Location = System.Drawing.Point(6, _y + _top);
        self.imagePathLabel.Name = "imagePathLabel";
        self.imagePathLabel.Size = System.Drawing.Size(32, 13);
        self.imagePathLabel.TabIndex = _tab_index;
        self.imagePathLabel.Text = "Path:";
        _y += self.imagePathLabel.Height + _top
        _tab_index += 1

        #
        # imagePathTextBox
        #
        _top = 3
        self.imagePathTextBox.Anchor = \
            System.Windows.Forms.AnchorStyles.Left \
            | System.Windows.Forms.AnchorStyles.Right \
            | System.Windows.Forms.AnchorStyles.Top;
        self.imagePathTextBox.Location = System.Drawing.Point(8, _y + _top);
        self.imagePathTextBox.Name = "imagePathTextBox";
        self.imagePathTextBox.Size = System.Drawing.Size(168, 20);
        self.imagePathTextBox.TabIndex = _tab_index;
        self.imagePathTextBox.Text = self.parent.raw.get('image', None) or ''
        # _y += self.imagePathTextBox.Height + _top
        _tab_index += 1

        #
        # imagePathBrowseButton
        #
        _top = 3
        self.imagePathBrowseButton.Anchor = \
            System.Windows.Forms.AnchorStyles.Right \
            | System.Windows.Forms.AnchorStyles.Top;
        self.imagePathBrowseButton.Location = System.Drawing.Point(184, _y + _top);
        self.imagePathBrowseButton.Name = "imagePathBrowseButton";
        self.imagePathBrowseButton.Size = System.Drawing.Size(27, 20);
        self.imagePathBrowseButton.TabIndex = _tab_index;
        self.imagePathBrowseButton.Text = "...";
        self.imagePathBrowseButton.UseVisualStyleBackColor = True;
        self.imagePathBrowseButton.Click += System.EventHandler(self.imagePathBrowseButton_Click);
        _y += self.imagePathBrowseButton.Height + _top
        _tab_index += 1

        #
        # imageUpdateButton
        #
        _top = 8
        self.imageUpdateButton.Location = System.Drawing.Point(8, _y + _top);
        self.imageUpdateButton.Name = "imageUpdateButton";
        self.imageUpdateButton.Size = System.Drawing.Size(88, 23);
        self.imageUpdateButton.TabIndex = _tab_index;
        self.imageUpdateButton.Text = "Update";
        self.imageUpdateButton.UseVisualStyleBackColor = True;
        self.imageUpdateButton.Click += System.EventHandler(self.imageUpdateButton_Click);
        # _y += self.imageUpdateButton.Height + _top
        _tab_index += 1

        #
        # imageCopyButton
        #
        _top = 8
        self.imageCopyButton.Enabled = False;
        self.imageCopyButton.Location = System.Drawing.Point(112, _y + _top);
        self.imageCopyButton.Name = "imageCopyButton";
        self.imageCopyButton.Size = System.Drawing.Size(88, 23);
        self.imageCopyButton.TabIndex = _tab_index;
        self.imageCopyButton.Text = "Copy...";
        self.imageCopyButton.UseVisualStyleBackColor = True;
        self.imageCopyButton.Click += System.EventHandler(self.imageCopyButton_Click);
        _y += self.imageCopyButton.Height + _top
        _tab_index += 1

        #
        # imagePreviewPictureBox
        #
        _top = 33
        self.imagePreviewPictureBox.Anchor = \
            System.Windows.Forms.AnchorStyles.Left \
            | System.Windows.Forms.AnchorStyles.Right \
            | System.Windows.Forms.AnchorStyles.Top \
            | System.Windows.Forms.AnchorStyles.Bottom;
        self.imagePreviewPictureBox.Location = System.Drawing.Point(8, _y + _top);
        self.imagePreviewPictureBox.Name = "imagePreviewPictureBox";
        self.imagePreviewPictureBox.Size = System.Drawing.Size(200, 248);
        self.imagePreviewPictureBox.TabIndex = _tab_index;
        self.imagePreviewPictureBox.TabStop = False;
        _y += self.imagePreviewPictureBox.Height + _top
        _tab_index += 1

        return self.imageModulePanel;

    def imageDisabledCheckBox_CheckedChanged(self, sender, e):
        self.setImageEnabled(not sender.Checked);

    def imagePathBrowseButton_Click(self, sender, e):
        root = Tk()
        root.withdraw()
        file = filedialog.askopenfilename(initialdir=self.parent.raw_directory + "../images/", defaultextension=".jpg", filetypes=(("Supported Image Files", "*.jpg *.jpeg *.png"), ("JPEG Images", "*.jpg *.jpeg"), ("PNG Images", "*.png"), ("All Files", "*.*")))
        root.destroy()
        if (not file):
            return

        self.imagePathTextBox.Text = file
        self.imageDisabledCheckBox.Checked = False
        self.setImage()

    def imageUpdateButton_Click(self, sender, e):
        self.setImage()

    def imageCopyButton_Click(self, sender, e):
        if (not self.image_path):
            return

        root = Tk()
        root.withdraw()
        extension = "*" + self.image_path[self.image_path.rfind('.'):]
        filename = self.parent.raw.get('name', '').lower().replace('\'', '').replace(' ', '-')
        file = filedialog.asksaveasfilename(initialfile=filename, initialdir=self.parent.raw_directory + "../images/", defaultextension=extension, filetypes=(("Image Files", extension), ("All Files", "*.*")))
        if (not file):
            return

        root.destroy()
        _file = file.replace('\\', '/')
        try:
            _file = _file[_file.rfind("images/"):]
        except:
            pass
        else:
            raw_root = ConfigLoader.get_from_config('rawDirectoryRoot')
            self.logger.debug("Copying the image {old} to the {root}{new}".format(old=self.image_path, root=raw_root, new=_file))
            copyfile(self.image_path, raw_root + _file)
            self.imagePathTextBox.Text = _file
            self.imageDisabledCheckBox.Checked = False
            self.setImage()


    def setImageEnabled(self, enabled):
        self.imageCopyButton.Enabled = enabled;
        self.imagePathBrowseButton.Enabled = enabled;
        self.imagePathTextBox.Enabled = enabled;

    def setImage(self, value="##DEFAULT##"):
        self.parent.raw['image'] = (None if (self.imageDisabledCheckBox.Checked) else self.imagePathTextBox.Text) if (value == "##DEFAULT##") else value
        self.update();

    def setErrorState(self, is_error=True):
        if (not self.imageModulePanel):
            return
        if (self.__error_state == is_error):
            return

        if (is_error):
            self.logger.debug("Setting input color to red due to warning on compilation.")
            self.__error_state = True
            self.imageCopyButton.Enabled = False
            self.imagePreviewPictureBox.Visible = False
            self.imagePathTextBox.ForeColor = System.Drawing.Color.Red;

        else:
            self.logger.debug("Warnings fixed, returning to normal state.")
            self.__error_state = False
            self.imageCopyButton.Enabled = not self.imageDisabledCheckBox.Checked
            self.imagePreviewPictureBox.Visible = not self.imageDisabledCheckBox.Checked
            self.imagePathTextBox.ForeColor = System.Drawing.SystemColors.WindowText;
