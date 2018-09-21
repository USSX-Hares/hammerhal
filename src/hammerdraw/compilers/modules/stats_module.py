from hammerdraw.compilers.compiler_module_base import CompilerModuleBase

from hammerdraw import generator
if (generator.generator_supported):
    import System
    from System import Decimal as decimal
    from hammerdraw.generator import InputControl


class StatsModule(CompilerModuleBase):
    module_name = "stats"

    def _compile(self, base):
        td = self.get_text_drawer(base)

        _stats = self.get_from_module_config('stats')
        for stat_name in _stats:
            _x = _stats[stat_name]['x']
            _y = _stats[stat_name]['y']
            _text_template = "{{{statName}}}{plusSymbol}".format(statName=stat_name, plusSymbol='+' if _stats[stat_name]['type'] == 'dice' else '')
            _text = _text_template.format(**self.parent.raw['stats'])
            td.print_line((_x, _y), _text)

        self.logger.info("Stats printed")
        return 0

    ### =======================================
    ###   WinForms module generator
    ### =======================================


    statsModulePanel = None
    statsStatLabels = None
    statsStatValueUpDowns = None


    def _create_generator_tab_content(self):
        _y = 0
        _tab_index = 0

        self.statsModulePanel = System.Windows.Forms.Panel();
        self.statsStatLabels = dict()
        self.statsStatValueUpDowns = dict()


        #
        # statsModulePanel
        #
        self.statsModulePanel.Anchor = \
            System.Windows.Forms.AnchorStyles.Left \
            | System.Windows.Forms.AnchorStyles.Right \
            | System.Windows.Forms.AnchorStyles.Top;
        self.statsModulePanel.Location = System.Drawing.Point(0, 0);
        self.statsModulePanel.Name = "statsModulePanel";
        self.statsModulePanel.Size = System.Drawing.Size(222, 429);
        self.statsModulePanel.TabIndex = 0;

        _stats = self.get_from_module_config('stats')
        for stat_name in _stats:
            statsStatLabel = System.Windows.Forms.Label();
            statsStatValueControl = InputControl.create_input_control_of_value_type \
            (
                name_prefix="stats{stat}StatValue".format(stat=stat_name),
                value_type=_stats[stat_name]['type'],
                value=self.parent.raw['stats'][stat_name],
                callback=self.setStat,
            )

            #
            # statsStatLabel
            #
            _top = 8
            statsStatLabel.AutoSize = True;
            statsStatLabel.Location = System.Drawing.Point(6, _y + _top);
            statsStatLabel.Name = "stats{stat}StatLabel".format(stat=stat_name.capitalize());
            statsStatLabel.Size = System.Drawing.Size(35, 13);
            statsStatLabel.TabIndex = _tab_index;
            statsStatLabel.Text = "{stat}:".format(stat=stat_name.capitalize());
            _tab_index += 1

            #
            # statsStatValueControl
            #
            _top = 6
            statsStatValueControl.Location = System.Drawing.Point(64, _y + _top);
            statsStatValueControl.Size = System.Drawing.Size(92, 21);
            statsStatValueControl.TabIndex = _tab_index;
            statsStatValueControl.Tag = stat_name;
            _tab_index += 1

            self.statsModulePanel.Controls.Add(statsStatLabel);
            self.statsModulePanel.Controls.Add(statsStatValueControl);
            self.statsStatLabels[stat_name] = statsStatLabel
            self.statsStatValueUpDowns[stat_name] = statsStatValueControl
            _y += statsStatValueControl.Height + _top


        return self.statsModulePanel;


    def setStat(self, stat, value):
        self.parent.raw['stats'][stat] = System.Convert.ToInt32(value)
        self.update()
