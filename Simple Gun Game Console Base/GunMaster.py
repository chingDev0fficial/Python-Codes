import pygame, os, time
from art import *

class Person:

    def __init__(self, name: str) -> None:
        self._name: str = name
        self._health: int = 100
        self._armor: int = 0 # bulletproof
        self._gun_mastery: float = 0.0 # in percentage (%)

    def get_name(self):
        return self._name

    def get_health(self):
        return self._health

    def get_armor(self):
        return self._armor

    def get_gun_mastery(self):
        return self._gun_mastery


class Target(Person):

    def __init__(self, name: str, armor: int) -> None:
        super().__init__(name = name)
        self._armor = armor

        
class Gunner(Person):
    
    def __init__(self, name: str, armor: int, distance_away: int, gun_used: object) -> None:
        super().__init__(name = name)
        self._armor = armor
        self._gun_mastery = 0.70 # Gun mastery is 70%
        
        self._gun_used: object = gun_used
        self._distance_away: int = distance_away

        # Fomula:
        # Final Damage = Base Damage × Accuracy × DHR Probability

        # DRH Probability formula = max(0 , 1-(Distance/Gun Range))
        
        # Distance-to-Range Hit Probability
        DRH_probability = max(0, 1-(self._distance_away/self._gun_used._gun_range))
        self._final_damage = self._gun_used.get_base_damage() * self._gun_used.get_accuracy() * DRH_probability

        # in this case the mastery of the gunner when it comes to gun is 70%
        # formula:
        # New Damage = Final Damage + (Final Damage × Gun Mastery)
        self._final_damage = self._final_damage + (self._final_damage * self._gun_mastery)

    def get_gun_used(self):
        return self._gun_used

    def get_distance(self):
        return self._distance_away

    def get_damage(self):
        return self._final_damage

class Bullet:

    def __init__(
        self, damage: int,
        bullet_id: int
    ) -> None:
        self._damage: float = float(f'0.{damage}')
        self._bullet_id: int = bullet_id

    def get_damage(self):
        return self._damage

    def get_bullet_id(self):
        return self._bullet_id

class Magazine:

    def __init__(self, bullet: object) -> None:
        self._bullets: list[object] = [bullet]

    def get_bullets(self):
        return self._bullets

class Gun: # Parent Class

    def __init__(
        self,
        gun_id: int,
        base_damage: int,
        accuracy: float,
        gun_range: int,
        ammo_capacity: int
    ) -> None:
        self._gun_id: int = gun_id
        self._base_damage: int = base_damage
        self._accuracy: int = accuracy
        self._gun_range: int = gun_range
        self._ammo_capacity: int = ammo_capacity
        self._magazine_well: list[object] = ...

    def trigger(self, damage: float or int) -> float or int:
        try:
            damage = damage + (damage * self._magazine_well[-1].get_damage()) # The final damage for the target
            self._magazine_well.pop()
        except IndexError:
            return 0

        return damage

    def reload(self, magazine: object) -> None:
        self._magazine_well = magazine.get_bullets() * self._ammo_capacity

    def load_mp3(self, file: str) -> None:
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

    def get_gun_id(self):
        return self._gun_id

    def get_base_damage(self):
        return self._base_damage

    def get_accuracy(self):
        return self._accuracy

    def get_gun_range(self):
        return self._gun_range

    def get_ammo_capacity(self):
        return self._ammo_capacity

    def get_magazine_well(self):
        return self._magazine_well

class Pistol(Gun): # Child Class

    def __init__(self) -> None:
        super().__init__(
            gun_id = 1, # unique
            base_damage = 50,
            accuracy = 0.70, # in percentage (70%)
            gun_range = 50, # in meters (50 meters)
            ammo_capacity = 10
        )

    # Polymorphism

    def shoot_sound(self):
        file: str = "sounds/pistol_shoot.mp3"
        self.load_mp3(file)

    def reloading_sound(self):
        file: str = "sounds/pistol_reload.mp3"
        self.load_mp3(file)

    def no_ammo_sound(self): 
        file: str = "sounds/no_ammo.mp3"
        self.load_mp3(file)

class Shotgun(Gun): # Child Class

    def __init__(self) -> None:
        super().__init__(
            gun_id = 2, # unique
            base_damage = 80,
            accuracy = 0.50, # in percentage (50%)
            gun_range = 25, # in meters (25 meters)
            ammo_capacity = 2
        )

    # Polymorphism

    def shoot_sound(self):
        file: str = "sounds/shotgun_shoot.mp3"
        self.load_mp3(file)

    def reloading_sound(self):
        file: str = "sounds/shotgun_reload.mp3"
        self.load_mp3(file)

    def no_ammo_sound(self):
        file: str = "sounds/no_ammo.mp3"
        self.load_mp3(file)

class Sniper(Gun): # Child Class

    def __init__(self) -> None:
        super().__init__(
            gun_id = 3, # unique
            base_damage = 300,
            accuracy = 0.90, # in percentage (90%)
            gun_range = 2000, # in meters (2,000 meters)
            ammo_capacity = 5
        )

    # Polymorphism

    def shoot_sound(self):
        file: str = "sounds/sniper_shoot.mp3"
        self.load_mp3(file)

    def reloading_sound(self):
        file: str = "sounds/sniper_reload.mp3"
        self.load_mp3(file)

    def no_ammo_sound(self):
        file: str = "sounds/no_ammo.mp3"
        self.load_mp3(file)

# Clear the console
def clear_console() -> None:
    os.system('cls')

def big_font(text: str) -> None:
    clear_console()
    ascii_art = text2art(text)
    print(ascii_art)

# Positional Selector
def position(*args) -> object | None:
    def select(pos):
        try:
            return args[pos-1] if pos > 0 else None
        except IndexError:
            return None
    return select

def error_catcher(select, selected, errorType):
    try:
        _select = int(select)
        return selected(_select)
    except errorType:
        return 0

def err_msg(used_item: any) -> any:
    match used_item:
        case None:
            print('Err: Invalid Input :: The selection scope is 1 - 3')
            input('Click Enter to RESELECT')
            return used_item

        case 0:
            print('Err: Invalid Value Input :: Use only int datatype')
            input('Click Enter to RESELECT')
            return None

        case _:
            return used_item

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

    used_gun = error_catcher(
        select = input('Select Gun: '),
        selected = position(pistol, shotgun, sniper),
        errorType = ValueError
    )

    used_gun = err_msg(used_gun)

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

    used_bullet = error_catcher(
        select = input('Select Bullet: '),
        selected = position(hp_bullet, slug_bullet, ap_bullet),
        errorType = ValueError
    )

    used_bullet = err_msg(used_bullet)


    try:
        if used_gun.get_gun_id() != used_bullet.get_bullet_id():
            reselect = input(
                "Unable to reload: Bullet is not for the gun you've used\nClick Enter to reselect")
            used_bullet = None
        else:
            # Magazine Object
            magazine = Magazine(used_bullet)
            used_gun.reloading_sound()
            used_gun.reload(magazine)
            time.sleep(2)
    except AttributeError:
        used_bullet = None
        
    clear_console()

# Object of Target and the Gunner

target = Target(
        'Any Name...',
        100 # Armor
    )

assassinator = Gunner(
        'Any Name...',
        0, # Armor
        10, # The distance away from the target
        used_gun
    )

target_health = target.get_health()
target_armor = target.get_armor()

while target_health > 0:
    ammo: int = len(assassinator.get_gun_used().get_magazine_well()) # Tracks The Number of ammo
    
    print(
            f'''
                           --Killer and Target Information--

Killer      : {assassinator.get_name():<40}Target      : {target.get_name()}
Health      : {assassinator.get_health():<40.2f}Health      : {target_health:.2f}
Armor       : {assassinator.get_armor():<40}Armor       : {target_armor:.2f}
Gun Mastery : {assassinator.get_gun_mastery():<40.2f}Gun Mastery : {target.get_gun_mastery():.2f}
============================================================================================
                                    --Statistics--

Distance from the Target : {assassinator.get_distance()}
Gun Base-Damage          : {used_gun.get_base_damage()}
Gun Accuracy             : {used_gun.get_accuracy()}
Bullet Damage            : {used_bullet.get_damage()}
============================================================================================
                                    --Gun Status--
                                    
ammo : {ammo}/{assassinator.get_gun_used().get_ammo_capacity()}
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

        if ammo < 1: # Check if not enough ammo
            big_font("NO AMMO")
            used_gun.no_ammo_sound()
            time.sleep(2)
        
        if target_armor > 0 and ammo > 0: # Check if the is not fully damaged and if there is still bullets otherwise we don't need to calculate
            #Armor Reduction = Damage * Armor Reduction Percentage
            #Health Damage = Damage - Armor Reduction
            armor_reduction = assassinator.get_damage() * 0.7 # Armor Reduction Percentage is 70%
            health_damage = assassinator.get_damage() - armor_reduction
            
            target_armor -= armor_reduction
            target_armor = 0 if target_armor < 0 else target_armor
                
            target_health -= assassinator.get_gun_used().trigger(health_damage)
        else:
            target_health -= assassinator.get_gun_used().trigger(assassinator.get_damage())

        if ammo > 0:
            clear_console()
            big_font("BANG...")
            used_gun.shoot_sound()
            time.sleep(2)

        # target_health = target_health
        # target_armor = target_armor
    else:
        big_font("RELOADING...")
        used_gun.reloading_sound()
        used_gun.reload(magazine)
        time.sleep(2)

    clear_console()

big_font(f"{target.get_name().upper()}  IS  DEAD!")
time.sleep(2)
big_font("Mission  Success!")
