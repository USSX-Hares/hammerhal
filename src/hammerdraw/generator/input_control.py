import clr
clr.AddReference("System.Windows.Forms")
import System
from System import Decimal as decimal

class InputControl:

    __defaults = \
    {
        "string": "",
        "integer": 0,
        "dice": 1,
    }

    @classmethod
    def get_default_value_of_type(cls, value_type):
        if (isinstance(value_type, list)):
            return value_type[0]
        elif (value_type in InputControl.__defaults):
            return InputControl.__defaults[value_type]
        else:
            raise TypeError("Value type {type} not supported".format(type=value_type))

    @classmethod
    def set_input_control_value(cls, control, value_type, value):
        if (isinstance(value_type, list)):
            control.SelectedIndex = value_type.index(value)
        elif (value_type == "integer"):
            control.Value = decimal(value)
        elif (value_type == "dice"):
            control.Value = decimal(value)
        elif (value_type == "string"):
            control.Text = value
        else:
            raise TypeError("Value type {type} not supported".format(type=value_type))


    @classmethod
    def create_input_control_of_value_type(cls, name_prefix, value_type, value=None, callback=None):

        if (isinstance(value_type, list)):
            result = System.Windows.Forms.ComboBox();

            result.Name = name_prefix + "ComboBox";
            result.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            result.FormattingEnabled = True;
            for _stat_value in value_type:
                result.Items.Add(_stat_value);
            if (callback):
                result.SelectedIndexChanged += System.EventHandler(lambda sender, event_args: callback(sender.Tag, sender.SelectedItem));

        elif (value_type == "integer"):
            result = System.Windows.Forms.NumericUpDown();

            result.Name = name_prefix + "UpDown";
            result.Increment = decimal(1);
            result.Minimum = decimal(0);
            result.Maximum = decimal(100);
            if (value):
                result.Value = decimal(value)
            else:
                result.Value = decimal(InputControl.__defaults[value_type])
            if (callback):
                result.ValueChanged += System.EventHandler(lambda sender, event_args: callback(sender.Tag, System.Convert.ToInt32(sender.Value)));

        elif (value_type == "dice"):
            result = System.Windows.Forms.NumericUpDown();

            result.Name = name_prefix + "UpDown";
            result.Increment = decimal(1);
            result.Minimum = decimal(1);
            result.Maximum = decimal(6);
            if (value):
                result.Value = decimal(value)
            else:
                result.Value = decimal(InputControl.__defaults[value_type])
            if (callback):
                result.ValueChanged += System.EventHandler(lambda sender, event_args: callback(sender.Tag, System.Convert.ToInt32(sender.Value)));

        elif (value_type == "string"):
            result = System.Windows.Forms.TextBox();

            result.Name = name_prefix + "TextBox";
            if (value):
                result.Text = value
            else:
                result.Text = InputControl.__defaults[value_type]
            if (callback):
                result.TextChanged += System.EventHandler(lambda sender, event_args: callback(sender.Tag, sender.Text));

        else:
            raise TypeError("Value type {type} not implemented for input control".format(type=value_type))

        return result
