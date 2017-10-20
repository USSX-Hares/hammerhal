from hammerhal.compilers.compiler_module_base import CompilerModuleBase
from hammerhal.text_drawer import TextDrawer


class HeroDiceSpaceModule(CompilerModuleBase):
    module_name = "dice_space"

    def _compile(self, base):
        dice_section = self.parent.raw.get('diceSpace', "default")
        if (dice_section == "default"):
            dice_section = self.get_from_module_config('defaultDiceSpace')

        total_dices_count = sum(_dice_type['count'] for _dice_type in dice_section)
        dice_width = self.get_from_module_config('diceMaxWidth')
        x1 = dice_width // 2; x2 = self.width - dice_width // 2
        _x = x1; _y = self.height // 2
        _dx = (x2 - x1) // (total_dices_count - 1)

        _h_max = 0
        for _dice_type in dice_section:
            for i in range(_dice_type['count']):
                _, _, _, _h =self.parent.insert_image_centered(base_image=base, position=(_x, _y), image_path=self.parent.sources_directory + _dice_type['image'])
                if (_h > _h_max):
                    _h_max = _h
                _x += _dx
        self.logger.info("Dice space printed")
        return 0