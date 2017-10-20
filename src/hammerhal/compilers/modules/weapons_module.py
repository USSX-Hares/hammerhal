from hammerhal.compilers.compiler_module_base import CompilerModuleBase
from hammerhal.text_drawer import TextDrawer

from hammerhal import generator
if (generator.generator_supported):
    import System
    from System import Decimal as decimal
    from hammerhal.generator import InputControl


class WeaponsModule(CompilerModuleBase):
    module_name = "weapons"

    weapon_stats = None
    def initialize(self, **kwargs):
        self.weapon_stats = self.get_from_module_config("stats")
        self.__last_weapons_count = len(self.parent.raw.get('weapons', ''))
        super().initialize(**kwargs)

    def get_size(self):
        width = self.get_from_module_config("width")

        _cell_height = self.get_from_module_config("cellHeight")
        _weapons_count = len(self.parent.raw.get("weapons", ''))
        _body_row_interval = self.get_from_module_config("rowIntervalByCount")[_weapons_count]
        _header_row_interval = self.get_from_module_config("headerRowInterval")
        height = _cell_height * (_weapons_count + 1) + _header_row_interval + _body_row_interval * (_weapons_count - 1)

        return width, height

    def _compile(self, base):
        td = self.get_text_drawer(base)

        if (not self.parent.raw.get('weapons')):
            return 0

        total_height = self.parent.insert_table \
        (
            vertical_columns = self.get_from_module_config("verticalColumns"),
            top = 0,
            cell_height = self.get_from_module_config("cellHeight"),
            data = self.parent.raw.get('weapons'),

            body_row_template = self.get_from_module_config("bodyRowTemplate"),
            body_text_drawer = td,
            body_row_interval = self.get_from_module_config("rowIntervalByCount")[len(self.parent.raw['weapons'])],
            body_capitalization = TextDrawer.CapitalizationModes.Capitalize,

            header_row = self.get_from_module_config("headerRow"),
            header_text_drawer = td,
            header_row_interval = self.get_from_module_config("headerRowInterval"),
            header_capitalization = TextDrawer.CapitalizationModes.Normal,
        )
        self.logger.info("Weapon table printed")

        return total_height

    ### =======================================
    ###   WinForms module generator
    ### =======================================


    weaponsModulePanel = None
    weaponsListListbox = None
    weaponsListLabel = None
    weaponsSelectedGroupBox = None
    weaponsRemoveButton = None
    weaponsAddButton = None
    weaponsSelectedNameTextBox = None
    weaponsSelectedNameLabel = None

    weaponsSelectedStatsLabels = None
    weaponsSelectedStatsValueControls = None

    __last_weapons_count = None

    def _on_update(self):
        new_weapons_count = len(self.parent.raw['weapons'])
        self.logger.debug("New weapons count: {new}; old: {old}".format(new=new_weapons_count, old=self.__last_weapons_count))
        if (self.__last_weapons_count != new_weapons_count):
            self.__last_weapons_count = new_weapons_count
            self.logger.debug("Updating base")
            _base = self.parent.prepare_base()
            if (_base):
                self.logger.debug("Base updated")
                self.parent.base = _base

    def _create_generator_tab_content(self):
        # raise NotImplementedError("Section under construction")

        _w = 10000
        _y = 0
        _tab_index = 0
        _group_y = 0
        _group_tab_index = 0

        self.weaponsModulePanel = System.Windows.Forms.Panel();
        self.weaponsListLabel = System.Windows.Forms.Label();
        self.weaponsListListbox = System.Windows.Forms.ListBox();
        self.weaponsAddButton = System.Windows.Forms.Button();
        self.weaponsRemoveButton = System.Windows.Forms.Button();
        self.weaponsSelectedGroupBox = System.Windows.Forms.GroupBox();
        self.weaponsSelectedNameTextBox = System.Windows.Forms.TextBox();
        self.weaponsSelectedNameLabel = System.Windows.Forms.Label();
        self.weaponsSelectedStatLabels = dict();
        self.weaponsSelectedStatsValueControls = dict();

        #
        # weaponsModulePanel
        #
        self.weaponsModulePanel.Anchor = \
            System.Windows.Forms.AnchorStyles.Left \
            | System.Windows.Forms.AnchorStyles.Right \
            | System.Windows.Forms.AnchorStyles.Top;
        self.weaponsModulePanel.Controls.Add(self.weaponsSelectedGroupBox);
        self.weaponsModulePanel.Controls.Add(self.weaponsRemoveButton);
        self.weaponsModulePanel.Controls.Add(self.weaponsAddButton);
        self.weaponsModulePanel.Controls.Add(self.weaponsListListbox);
        self.weaponsModulePanel.Controls.Add(self.weaponsListLabel);
        self.weaponsModulePanel.Location = System.Drawing.Point(0, 0);
        self.weaponsModulePanel.Name = "weaponsModulePanel";
        self.weaponsModulePanel.Size = System.Drawing.Size(222, 421);
        self.weaponsModulePanel.TabIndex = 0;

        #
        # weaponsListLabel
        #
        _top = 3
        self.weaponsListLabel.AutoSize = True;
        self.weaponsListLabel.Location = System.Drawing.Point(3, _y + _top);
        self.weaponsListLabel.Name = "weaponsListLabel";
        self.weaponsListLabel.Size = System.Drawing.Size(56, 13);
        self.weaponsListLabel.TabIndex = _tab_index;
        self.weaponsListLabel.Text = "Weapons:";
        _tab_index += 1
        _y += self.weaponsListLabel.Height + _top

        #
        # weaponsListListbox
        #
        _top = 3
        self.weaponsListListbox.Anchor = \
            System.Windows.Forms.AnchorStyles.Left \
            | System.Windows.Forms.AnchorStyles.Right \
            | System.Windows.Forms.AnchorStyles.Top;
        self.weaponsListListbox.FormattingEnabled = True;
        self.weaponsListListbox.Location = System.Drawing.Point(3, _y + _top);
        self.weaponsListListbox.Name = "weaponsListListbox";
        self.weaponsListListbox.Size = System.Drawing.Size(213, 134);
        self.weaponsListListbox.TabIndex = _tab_index;
        self.weaponsListListbox.SelectedIndexChanged += System.EventHandler(self.weaponsListListbox_SelectedIndexChanged);
        _tab_index += 1
        _y += self.weaponsListListbox.Height + _top

        #
        # weaponsAddButton
        #
        _top = 6
        self.weaponsAddButton.Location = System.Drawing.Point(3, _y + _top);
        self.weaponsAddButton.Name = "weaponsAddButton";
        self.weaponsAddButton.Size = System.Drawing.Size(75, 23);
        self.weaponsAddButton.TabIndex = _tab_index;
        self.weaponsAddButton.Text = "Add";
        self.weaponsAddButton.UseVisualStyleBackColor = True;
        self.weaponsAddButton.Click += System.EventHandler(self.weaponsAddButton_Click);
        # _y += self.weaponsAddButton.Height + _top

        #
        # weaponsRemoveButton
        #
        _top = 6
        self.weaponsRemoveButton.Enabled = False;
        self.weaponsRemoveButton.Location = System.Drawing.Point(84, _y + _top);
        self.weaponsRemoveButton.Name = "weaponsRemoveButton";
        self.weaponsRemoveButton.Size = System.Drawing.Size(75, 23);
        self.weaponsRemoveButton.TabIndex = _tab_index;
        self.weaponsRemoveButton.Text = "Remove";
        self.weaponsRemoveButton.UseVisualStyleBackColor = True;
        self.weaponsRemoveButton.Click += System.EventHandler(self.weaponsRemoveButton_Click);
        _y += self.weaponsRemoveButton.Height + _top

        #
        # weaponsSelectedGroupBox
        #
        _top = 9
        self.weaponsSelectedGroupBox.Anchor = \
            System.Windows.Forms.AnchorStyles.Left \
            | System.Windows.Forms.AnchorStyles.Right \
            | System.Windows.Forms.AnchorStyles.Top;
        self.weaponsSelectedGroupBox.Controls.Add(self.weaponsSelectedNameTextBox);
        self.weaponsSelectedGroupBox.Controls.Add(self.weaponsSelectedNameLabel);
        self.weaponsSelectedGroupBox.Enabled = False;
        self.weaponsSelectedGroupBox.Location = System.Drawing.Point(3, _y + _top);
        self.weaponsSelectedGroupBox.Name = "weaponsSelectedGroupBox";
        self.weaponsSelectedGroupBox.Size = System.Drawing.Size(213, 221);
        self.weaponsSelectedGroupBox.TabIndex = _tab_index;
        self.weaponsSelectedGroupBox.TabStop = False;
        self.weaponsSelectedGroupBox.Text = "{selected";
        _y += self.weaponsSelectedGroupBox.Height + _top

        #
        # weaponsSelectedNameLabel
        #
        _top = 16
        self.weaponsSelectedNameLabel.AutoSize = True;
        self.weaponsSelectedNameLabel.Location = System.Drawing.Point(6, _group_y + _top);
        self.weaponsSelectedNameLabel.Name = "weaponsSelectedNameLabel";
        self.weaponsSelectedNameLabel.Size = System.Drawing.Size(38, 13);
        self.weaponsSelectedNameLabel.TabIndex = _group_tab_index;
        self.weaponsSelectedNameLabel.Text = "Name:";
        _group_tab_index += 1
        # _group_y += self.weaponsSelectedNameLabel.Height + _top

        #
        # weaponsSelectedNameTextBox
        #
        _top = 14
        self.weaponsSelectedNameTextBox.Location = System.Drawing.Point(64, _group_y + _top);
        self.weaponsSelectedNameTextBox.Name = "weaponsSelectedNameTextBox";
        self.weaponsSelectedNameTextBox.Size = System.Drawing.Size(92, 21);
        self.weaponsSelectedNameTextBox.TabIndex = _tab_index;
        self.weaponsSelectedNameTextBox.TextChanged += System.EventHandler(self.weaponsSelectedNameTextBox_TextChanged);
        _group_tab_index += 1
        _group_y += self.weaponsSelectedNameTextBox.Height + _top

        _weapons = self.parent.raw.get('weapons', [])
        for weapon in _weapons:
            self.weaponsListListbox.Items.Add(weapon['name']);

        for stat_name, stat_type in self.weapon_stats.items():
            weaponStatsStatLabel = System.Windows.Forms.Label();
            weaponStatsStatValueControl = InputControl.create_input_control_of_value_type \
            (
                name_prefix="weaponsSelected{stat}StatValue".format(stat=stat_name),
                value_type=stat_type,
                callback=self.setStat,
            )

            #
            # weaponStatsStatLabel
            #
            _top = 8
            weaponStatsStatLabel.AutoSize = True;
            weaponStatsStatLabel.Location = System.Drawing.Point(6, _group_y + _top);
            weaponStatsStatLabel.Name = "weaponsSelected{stat}StatLabel".format(stat=stat_name.capitalize());
            weaponStatsStatLabel.Size = System.Drawing.Size(35, 13);
            weaponStatsStatLabel.TabIndex = _group_tab_index;
            weaponStatsStatLabel.Text = "{stat}:".format(stat=stat_name.capitalize());
            _group_tab_index += 1

            #
            # weaponStatsStatValueControl
            #
            _top = 6
            weaponStatsStatValueControl.Location = System.Drawing.Point(64, _group_y + _top);
            weaponStatsStatValueControl.Size = System.Drawing.Size(92, 21);
            weaponStatsStatValueControl.TabIndex = _group_tab_index;
            weaponStatsStatValueControl.Tag = stat_name;
            _group_tab_index += 1

            self.weaponsSelectedGroupBox.Controls.Add(weaponStatsStatLabel);
            self.weaponsSelectedGroupBox.Controls.Add(weaponStatsStatValueControl);
            self.weaponsSelectedStatLabels[stat_name] = weaponStatsStatLabel
            self.weaponsSelectedStatsValueControls[stat_name] = weaponStatsStatValueControl
            _group_y += weaponStatsStatValueControl.Height + _top

        self.weaponsSelectedGroupBox.MinimumSize.Width = self.weaponsSelectedGroupBox.PreferredSize.Width
        self.weaponsSelectedGroupBox.Height = self.weaponsSelectedGroupBox.PreferredSize.Height

        return self.weaponsModulePanel;


    __prevent_events = False
    def weaponsListListbox_SelectedIndexChanged(self, sender, e):
        self.selectWeapon(sender.SelectedIndex)

    def weaponsAddButton_Click(self, sender, e):
        index = self.addWeapon()
        self.selectWeapon(index)

    def weaponsRemoveButton_Click(self, sender, e):
        self.removeWeapon(index=self.weaponsListListbox.SelectedIndex)
        self.selectWeapon(-1)

    def weaponsSelectedNameTextBox_TextChanged(self, sender, e):
        self.setName(sender.Text)

    def selectWeapon(self, index):
        if (self.__prevent_events):
            return;

        self.__prevent_events = True;
        self.weaponsListListbox.SelectedIndex = index

        if (index == -1):
            self.weaponsRemoveButton.Enabled = False;
            self.weaponsSelectedGroupBox.Enabled = False;
            self.weaponsSelectedGroupBox.Text = "Select weapon";

        else:
            selected_weapon = self.parent.raw['weapons'][index]

            self.weaponsSelectedGroupBox.Text = self.weaponsListListbox.SelectedItem;
            self.weaponsSelectedNameTextBox.Text = self.weaponsListListbox.SelectedItem;
            self.weaponsRemoveButton.Enabled = True;
            self.weaponsSelectedGroupBox.Enabled = True;

            for stat_name, stat_type in self.weapon_stats.items():
                InputControl.set_input_control_value(self.weaponsSelectedStatsValueControls[stat_name], stat_type, selected_weapon[stat_name])

        self.__prevent_events = False;

    def addWeapon(self):
        new_weapon = { "name": "New Weapon" }

        for stat_name, stat_type in self.weapon_stats.items():
            new_weapon[stat_name] = InputControl.get_default_value_of_type(stat_type)

        index = self.weaponsListListbox.Items.Add(new_weapon['name']);
        self.parent.raw['weapons'] = self.parent.raw.get('weapons', list())
        self.parent.raw['weapons'].append(new_weapon)
        self.update();
        return index

    def removeWeapon(self, index):
        self.weaponsListListbox.Items.RemoveAt(index);
        del self.parent.raw['weapons'][index]
        self.update();

    def setName(self, value):
        if (self.__prevent_events):
            return;

        index = self.weaponsListListbox.SelectedIndex;
        self.__prevent_events = True;
        self.weaponsSelectedGroupBox.Text = self.weaponsSelectedNameTextBox.Text;
        self.weaponsListListbox.Items[index] = self.weaponsSelectedNameTextBox.Text;
        self.__prevent_events = False;
        self.setStat('name', value);

    def setStat(self, stat, value):
        if (self.__prevent_events):
            return;

        index = self.weaponsListListbox.SelectedIndex;
        self.parent.raw['weapons'][index][stat] = value;
        self.update();
