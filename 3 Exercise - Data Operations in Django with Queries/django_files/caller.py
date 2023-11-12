import os
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


# Create queries within functions
def create_pet(pet_name: str, pet_species: str):
    Pet.objects.create(
        name=pet_name,
        species=pet_species
    )

    return f"{pet_name} is a very cute {pet_species}!"


# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )
    return f"The artifact {name} is {age} years old!"


def delete_all_artifacts():
    Artifact.objects.all().delete()


# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# delete_all_artifacts()


def show_all_locations():
    print_info = []
    for loc in Location.objects.all().order_by('-id'):
        print_info.append(f"{loc.name} has a population of {loc.population}!")

    return '\n'.join(print_info)


def new_capital():
    x = Location.objects.first()
    x.is_capital = True
    x.save()


def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


# print(show_all_locations())
# print(new_capital())
# print(get_capitals())

def apply_discount():
    for car in Car.objects.all():
        discount = sum(int(x) for x in str(car.year)) / 100
        car.price_with_discount = float(car.price) - (float(car.price) * discount)
        car.save()


# apply_discount()
def get_recent_cars():
    return Car.objects.filter(year__gte=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    unfinished_task = []

    for task in Task.objects.filter(is_finished=False):
        unfinished_task.append(
            f"Task - {task.title} needs to be done until {task.due_date}!")

    return '\n'.join(unfinished_task)


# print(show_unfinished_tasks())


def complete_odd_tasks():
    for task in Task.objects.all():
        if task.id % 2 == 1:
            task.is_finished = True
            task.save()


# complete_odd_tasks()


def encode_and_replace(text: str, task_title: str):
    for task in Task.objects.all():
        if task.title == task_title:
            task.description = ''.join([chr(ord(x) - 3) for x in text])
            task.save()


# encode_and_replace("Zdvk#wkh#glvkhv$", "Simple Task")
# print(Task.objects.get(title='Simple Task').description)


def get_deluxe_rooms():
    rooms_filtered = []
    for room in HotelRoom.objects.filter(room_type='Deluxe'):
        if room.id % 2 == 0:
            rooms_filtered.append(
                f"Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!")

    return '\n'.join(rooms_filtered)


def increase_room_capacity():
    last_room_cap = None

    for room in HotelRoom.objects.all().order_by('id'):
        if not room.is_reserved:
            continue

        if last_room_cap:
            room.capacity += last_room_cap
        else:
            room.capacity += room.id

        last_room_cap = room.capacity
        room.save()


def reserve_first_room():
    target_room = HotelRoom.objects.first()
    target_room.is_reserved = True
    target_room.save()


def delete_last_room():
    if HotelRoom.objects.last().is_reserved:
        HotelRoom.objects.last().delete()


# print(get_deluxe_rooms())
# increase_room_capacity()
# reserve_first_room()
# delete_last_room()

def update_characters():
    Character.objects.filter(class_name='Mage').update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )

    Character.objects.filter(class_name='Warrior').update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )

    Character.objects.filter(class_name__in=['Assassin', 'Scout']).update(
        inventory="The inventory is empty"
    )


def fuse_characters(first_character, second_character):
    new_name = first_character.name + ' ' + second_character.name
    new_class_name = 'Fusion'
    new_level = (first_character.level + second_character.level) // 2
    new_strength = (first_character.strength + second_character.strength) * 1.2
    new_dexterity = (first_character.dexterity + second_character.dexterity) * 1.4
    new_intelligence = (first_character.intelligence + second_character.intelligence) * 1.5
    new_hit_points = first_character.hit_points + second_character.hit_points

    if first_character.class_name in ["Mage", "Scout"]:
        new_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        new_inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=new_name,
        class_name=new_class_name,
        level=new_level,
        strength=new_strength,
        dexterity=new_dexterity,
        intelligence=new_intelligence,
        hit_points=new_hit_points,
        inventory=new_inventory,
    )

    first_character.delete()
    second_character.delete()


def grand_strength():
    Character.objects.all().update(strength=50)


def grand_dexterity():
    Character.objects.all().update(dexterity=30)


def grand_intelligence():
    Character.objects.all().update(intelligence=40)


def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()
