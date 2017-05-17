import log
import actions
import config


def cast_heal(player, amount=config.HEALING_POTION_AMOUNT):
    if player.fighter.hp == player.fighter.max_hp:
        log.add_message('Already at full health')
        return 'cancelled'

    log.add_message('You feel much better!')
    actions.heal(player.fighter, amount)
