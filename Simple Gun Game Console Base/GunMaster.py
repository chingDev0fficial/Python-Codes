class Person:

    def __init__(
        self,
        name: str,
        armor: int = 0,
        gun_mastery: int = 0
    ) -> None:
        self.name: str = name
        self.health: int = 100
        self.armor: int = armor # bulletproof
        self.gun_mastery: float = float(f'0.{gun_mastery}') # in percentage (%)

class Target(Person):

    def __init__(
        self,
        name: str,
        armor: int
    ) -> None:
        super().__init__(
            name = name,
            armor = armor,
            gun_mastery = 0
        )
        
class Gunner(Person):
    
    def __init__(
        self,
        name: str,
        armor: int,
        distance_away: int, # in meters
        gun_used: object
    ) -> None:
        super().__init__(
            name = name,
            armor = armor,
            gun_mastery = 70 # Gun Mastery = 70%
        )
        self.gun_used: object = gun_used
        self.distance_away: int = distance_away

        # Fomula:
        # Final Damage = Base Damage × Accuracy × DHR Probability

        # DRH Probability formula = max(0 , 1-(Distance/Gun Range))
        
        # Distance-to-Range Hit Probability
        DRH_probability = max(0, 1-(self.distance_away/self.gun_used.gun_range))
        self.final_damage = self.gun_used.base_damage * self.gun_used.accuracy * DRH_probability

        # in this case the mastery of the gunner when it comes to gun is 70%
        # formula:
        # New Damage = Final Damage + (Final Damage × Gun Mastery)
        self.final_damage = self.final_damage + (self.final_damage * self.gun_mastery)

class Bullet:

    def __init__(
        self,
        damage: int,
        bullet_id: int
    ) -> None:
        self.damage: float = float(f'0.{damage}')
        self.bullet_id: int = bullet_id

class Magazine:

    def __init__(self, bullet: object) -> None:
        self.bullets: list[object] = [bullet]

class Gun: # Parent Class

    def __init__(
        self,
        gun_id: int,
        base_damage: int,
        accuracy: float,
        gun_range: int,
        amo_capacity: int
    ) -> None:
        self.gun_id: int = gun_id
        self.base_damage: int = base_damage
        self.accuracy: int = accuracy
        self.gun_range: int = gun_range
        self.amo_capacity: int = amo_capacity
        self.magazine_well: list[object] = ...

    def triger(self, damage: float or int) -> float or int:
        try:
            self.magazine_well.pop()
            damage = damage + (damage * self.magazine_well[0].damage) # This is the final damage for the target
        except IndexError:
            return 0
        
        return damage

    def reload(self, magazine: object) -> None:
        self.magazine_well = magazine.bullets * self.amo_capacity

class Pistol(Gun): # Child Class

    def __init__(self) -> None:
        super().__init__(
            gun_id = 1, # unique
            base_damage = 30,
            accuracy = 0.70, # in percentage (70%)
            gun_range = 50, # in meters (50 meters)
            amo_capacity = 10
        )

class Shotgun(Gun): # Child Class

    def __init__(self) -> None:
        super().__init__(
            gun_id = 2, # unique
            base_damage = 80,
            accuracy = 0.50, # in percentage (50%)
            gun_range = 25, # in meters (25 meters)
            amo_capacity = 2
        )

class Sniper(Gun): # Child Class

    def __init__(self) -> None:
        super().__init__(
            gun_id = 3, # unique
            base_damage = 300,
            accuracy = 0.90, # in percentage (90%)
            gun_range = 2000, # in meters (2,000 meters)
            amo_capacity = 5
        )

import os, time
from art import *

# Clear the console
def clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def big_font(text: str) -> None:
    clear_console()
    ascii_art = text2art(text)
    print(ascii_art)
    time.sleep(2)

# Positional Selector
def position(*args) -> object | None:
    def select(pos):
        try:
            return args[pos-1]
        except IndexError:
            return None
    return select

clear_console() # Clean the console

# Objects of bullets

# Hollow Point (HP) bullet damage: 40%
hp_bullet = Bullet(40, 1) #: bullet for pistol
# Slug bullet damage: 80%
slug_bullet = Bullet(80, 2) #: bullet for shotgun
# Armor-Piercing (AP) bullet damage: 90%
ap_bullet = Bullet(90, 3) #: bullet for sniper

# Objects of guns
pistol = Pistol()
shotgun = Shotgun()
sniper = Sniper()

used_gun: object or None = ...
used_bullet: object or None = ...

while used_gun == ... or used_gun is None:
    
    print(
        '''
                    --Select a Gun--

            [ 1 ] - Pistol      [ 2 ] - Shotgun
            
                    [ 3 ] - Sniper

    =====================================================
        '''
        )
    select: int = int(input('Select Gun: '))
    used_gun = position(pistol, shotgun, sniper)(select)
    clear_console()

while used_bullet == ... or used_bullet == None:

    print(
        '''
                    --Select a Bullet--

            [ 1 ] - HP Bullet   [ 2 ] - Slug Bullet
            
                    [ 3 ] - AP Bullet

    =====================================================
        '''
        )
    select: int = int(input('Select Bullet: '))
    used_bullet = position(hp_bullet, slug_bullet, ap_bullet)(select)

    # Magazine Object
    magazine = Magazine(used_bullet)
    try:
        if used_gun.gun_id != magazine.bullets[0].bullet_id:
            reselect = input('Unable to reload: Bullet is not for the gun you used\nClick Enter to reselect')
            used_bullet = None
        else:
            used_gun.reload(magazine)
    except AttributeError:
        used_bullet = None
        
    clear_console()

# Object of Target and the Gunner

target = Target(
        'Any name...',
        100 # Armor
    )

assassinator = Gunner(
        'Any name...',
        0, # Armor
        10, # The distance away from the target
        used_gun
    )

target_health = target.health
target_armor = target.armor

while target_health > 0:
    amo: int = len(assassinator.gun_used.magazine_well)
    
    print(
            f'''
                           --Killer and Target Information--

Killer      : {assassinator.name:<40}Target      : {target.name}
Health      : {assassinator.health:<40.2f}Health      : {target_health:.2f}
Armor       : {assassinator.armor:<40}Armor       : {target_armor:.2f}
Gun Mastery : {assassinator.gun_mastery:<40.2f}Gun Mastery : {target.gun_mastery:.2f}
============================================================================================
                                    --Statistics--

Distance from the Target : {assassinator.distance_away}
Gun Base-Damage          : {used_gun.base_damage}
Gun Accuracy             : {used_gun.accuracy}
Bullet Damage            : {used_bullet.damage}
============================================================================================
                                    --Gun Status--
                                    
Amo : {amo}/{assassinator.gun_used.amo_capacity}
            '''
        )
    
    print(
            '''
Click Enter To Triger the Gun
Click R then Enter to Reload
            '''
        )

    action = input(':: ')
    
    if action.upper() != 'R':

        if amo < 1:
            big_font("NO AMO")
        
        if target.armor > 0 and amo > 0:
            #Armor Reduction = Damage * Armor Reduction Percentage
            #Health Damage = Damage - Armor Reduction
            armor_reduction = assassinator.final_damage * 0.7 # Armor Reduction Percentage is 70%
            health_damage = assassinator.final_damage - armor_reduction
            
            target.armor -= armor_reduction
            target_armor = 0 if target.armor < 0 else target.armor
                
            target.health -= assassinator.gun_used.triger(health_damage)
        else:
            target.health -= assassinator.gun_used.triger(assassinator.final_damage)

        if amo > 0:
            clear_console()
            big_font("BANG...")

        target_health = target.health
    else:
        big_font("RELOADING...")
        used_gun.reload(magazine)

    clear_console()

big_font(f"{target.name.upper()}  IS  DEAD!")
big_font("Mission  Success!")



