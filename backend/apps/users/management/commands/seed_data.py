"""
Comprehensive seed data for StayFinder Coimbatore.
Generates 100+ properties across 20 Coimbatore areas with Tamil names,
realistic pricing, amenities, rooms, reviews, and user accounts.
"""
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.properties.models import Property, Room, PropertyImage, Amenity
from apps.users.models import OwnerProfile
from apps.reviews.models import Review
from apps.bookings.models import Booking

User = get_user_model()

# ============================================================
# Coimbatore Area Data with real coordinates
# ============================================================
AREAS = {
    'Peelamedu':        {'lat': 11.0247, 'lng': 77.0028, 'pin': '641004', 'bus': ['Peelamedu Bus Stop', 'PSG Signal Stop', 'Fun Mall Stop']},
    'Gandhipuram':      {'lat': 11.0168, 'lng': 76.9558, 'pin': '641012', 'bus': ['Gandhipuram Bus Stand', 'Town Hall Stop', 'Cross Cut Road Stop']},
    'RS Puram':         {'lat': 11.0060, 'lng': 76.9550, 'pin': '641002', 'bus': ['RS Puram Bus Stop', 'DB Road Stop', 'Ramanathapuram Stop']},
    'Singanallur':      {'lat': 11.0040, 'lng': 77.0270, 'pin': '641005', 'bus': ['Singanallur Bus Stop', 'Airport Signal Stop', 'Trichy Road Stop']},
    'Saravanampatti':   {'lat': 11.0690, 'lng': 76.9990, 'pin': '641035', 'bus': ['Saravanampatti Bus Stop', 'Kalapatti Signal Stop', 'IT Park Stop']},
    'Ganapathy':        {'lat': 11.0310, 'lng': 76.9630, 'pin': '641006', 'bus': ['Ganapathy Bus Stop', 'VOC Park Stop', 'Katoor Road Stop']},
    'Saibaba Colony':   {'lat': 11.0200, 'lng': 76.9650, 'pin': '641011', 'bus': ['Saibaba Colony Stop', 'Nehru Nagar Stop', 'Goldwins Stop']},
    'Kuniyamuthur':     {'lat': 10.9700, 'lng': 76.9500, 'pin': '641008', 'bus': ['Kuniyamuthur Bus Stop', 'Marudhamalai Road Stop', 'GCT Stop']},
    'Ukkadam':          {'lat': 10.9950, 'lng': 76.9610, 'pin': '641001', 'bus': ['Ukkadam Bus Stand', 'Big Bazaar Street Stop', 'Aathupalam Stop']},
    'Hope College':     {'lat': 11.0130, 'lng': 76.9680, 'pin': '641018', 'bus': ['Hope College Stop', 'Race Course Stop', 'Nava India Stop']},
    'Podanur':          {'lat': 10.9580, 'lng': 76.9880, 'pin': '641023', 'bus': ['Podanur Railway Station Stop', 'Podanur Bus Stop', 'Eachanari Stop']},
    'Sundarapuram':     {'lat': 10.9870, 'lng': 76.9330, 'pin': '641024', 'bus': ['Sundarapuram Bus Stop', 'Perur Road Stop', 'Sungam Stop']},
    'Kalapatti':        {'lat': 11.0530, 'lng': 77.0150, 'pin': '641048', 'bus': ['Kalapatti Bus Stop', 'Avinashi Road Stop', 'LOTTE Mart Stop']},
    'Perur':            {'lat': 10.9720, 'lng': 76.9150, 'pin': '641010', 'bus': ['Perur Bus Stop', 'Perur Temple Stop', 'Madukkarai Road Stop']},
    'Kovaipudur':       {'lat': 10.9530, 'lng': 76.9350, 'pin': '641042', 'bus': ['Kovaipudur Bus Stop', 'Vellalore Stop', 'Kovaipudur Signal Stop']},
    'Sulur':            {'lat': 11.0370, 'lng': 77.1230, 'pin': '641402', 'bus': ['Sulur Bus Stand', 'Air Force Station Stop', 'Sulur Market Stop']},
    'Mettupalayam':     {'lat': 11.2990, 'lng': 76.9400, 'pin': '641301', 'bus': ['Mettupalayam Bus Stand', 'Karamadai Stop', 'Mettupalayam Market Stop']},
    'Pollachi':         {'lat': 10.6600, 'lng': 77.0080, 'pin': '642001', 'bus': ['Pollachi Bus Stand', 'Pollachi Market Stop', 'Aaliyar Road Stop']},
    'Kinathukadavu':    {'lat': 10.8230, 'lng': 76.9860, 'pin': '642109', 'bus': ['Kinathukadavu Bus Stop', 'Madukkarai Road Stop']},
    'Madukkarai':       {'lat': 10.9060, 'lng': 76.9600, 'pin': '641105', 'bus': ['Madukkarai Bus Stop', 'Walayar Stop']},
}

# College → nearby areas mapping
COLLEGE_AREAS = {
    'PSG College of Technology':    ['Peelamedu', 'Saravanampatti', 'Kalapatti'],
    'PSG College of Arts & Science':['Peelamedu', 'Ganapathy', 'Saibaba Colony'],
    'Rathinam College':             ['Kalapatti', 'Saravanampatti', 'Sulur'],
    'Sri Krishna College':          ['Kuniyamuthur', 'Sundarapuram', 'Perur'],
    'Kumaraguru College':           ['Saravanampatti', 'Kalapatti', 'Peelamedu'],
    'Karunya University':           ['Kuniyamuthur', 'Kovaipudur', 'Perur'],
    'SNS College':                  ['Saravanampatti', 'Kalapatti', 'Peelamedu'],
    'NGP College':                  ['Kalapatti', 'Saravanampatti'],
    'Hindusthan College':           ['Peelamedu', 'Singanallur', 'Kalapatti'],
    'CIT':                          ['Peelamedu', 'Singanallur'],
    'Government Arts College':      ['Ukkadam', 'RS Puram', 'Hope College'],
    'Amrita University':            ['Kalapatti', 'Saravanampatti', 'Peelamedu'],
}

def get_nearby_colleges(area):
    """Return list of colleges near a given area."""
    return [college for college, areas in COLLEGE_AREAS.items() if area in areas]

# ============================================================
# Tamil Owner Data
# ============================================================
OWNERS = [
    {'username': 'selvaraj_owner',   'first_name': 'Selvaraj',   'last_name': 'Gounder',   'email': 'selvaraj@stayfinder.in',   'phone': '9876543001', 'business': 'Selvaraj Stays'},
    {'username': 'murugan_owner',    'first_name': 'Murugan',    'last_name': 'Pillai',    'email': 'murugan@stayfinder.in',    'phone': '9876543002', 'business': 'Murugan Residencies'},
    {'username': 'palanisamy_owner', 'first_name': 'Palanisamy', 'last_name': 'Nadar',     'email': 'palanisamy@stayfinder.in', 'phone': '9876543003', 'business': 'Palanisamy PG Homes'},
    {'username': 'muthusamy_owner',  'first_name': 'Muthusamy',  'last_name': 'Thevar',    'email': 'muthusamy@stayfinder.in',  'phone': '9876543004', 'business': 'Muthusamy Hostels'},
    {'username': 'lakshmi_owner',    'first_name': 'Lakshmi',    'last_name': 'Devi',      'email': 'lakshmi@stayfinder.in',    'phone': '9876543005', 'business': 'Lakshmi Women\'s Homes'},
    {'username': 'meenakshi_owner',  'first_name': 'Meenakshi',  'last_name': 'Ammal',     'email': 'meenakshi@stayfinder.in',  'phone': '9876543006', 'business': 'Meenakshi Ladies PG'},
    {'username': 'revathi_owner',    'first_name': 'Revathi',    'last_name': 'Sundaram',  'email': 'revathi@stayfinder.in',    'phone': '9876543007', 'business': 'Revathi Comfort Stays'},
]

# ============================================================
# Tamil Student Data
# ============================================================
STUDENTS = [
    {'username': 'tamilselvi_s',  'first_name': 'Tamilselvi',  'last_name': 'M',      'email': 'tamilselvi@stayfinder.in',  'gender': 'female', 'college': 'PSG College of Technology'},
    {'username': 'kavya_s',       'first_name': 'Kavya',       'last_name': 'R',      'email': 'kavya@stayfinder.in',       'gender': 'female', 'college': 'Kumaraguru College'},
    {'username': 'nandhini_s',    'first_name': 'Nandhini',    'last_name': 'S',      'email': 'nandhini@stayfinder.in',    'gender': 'female', 'college': 'Rathinam College'},
    {'username': 'priya_s',       'first_name': 'Priya',       'last_name': 'K',      'email': 'priya@stayfinder.in',       'gender': 'female', 'college': 'SNS College'},
    {'username': 'arunkumar_s',   'first_name': 'Arun Kumar',  'last_name': 'V',      'email': 'arunkumar@stayfinder.in',   'gender': 'male',   'college': 'PSG College of Technology'},
    {'username': 'karthik_s',     'first_name': 'Karthik',     'last_name': 'P',      'email': 'karthik@stayfinder.in',     'gender': 'male',   'college': 'CIT'},
    {'username': 'vignesh_s',     'first_name': 'Vignesh',     'last_name': 'T',      'email': 'vignesh@stayfinder.in',     'gender': 'male',   'college': 'Karunya University'},
    {'username': 'sathish_s',     'first_name': 'Sathish',     'last_name': 'B',      'email': 'sathish@stayfinder.in',     'gender': 'male',   'college': 'Sri Krishna College'},
    {'username': 'harish_s',      'first_name': 'Harish',      'last_name': 'N',      'email': 'harish@stayfinder.in',      'gender': 'male',   'college': 'Hindusthan College'},
    {'username': 'deepika_s',     'first_name': 'Deepika',     'last_name': 'L',      'email': 'deepika@stayfinder.in',     'gender': 'female', 'college': 'Amrita University'},
    {'username': 'surya_s',       'first_name': 'Surya',       'last_name': 'G',      'email': 'surya@stayfinder.in',       'gender': 'male',   'college': 'NGP College'},
    {'username': 'anitha_s',      'first_name': 'Anitha',      'last_name': 'D',      'email': 'anitha@stayfinder.in',      'gender': 'female', 'college': 'Government Arts College'},
]

# ============================================================
# Property Name Templates (Tamil / Coimbatore style)
# ============================================================
BOYS_HOSTEL_NAMES = [
    'Murugan Boys Hostel', 'Selvam Boys Hostel', 'Kongu Residency', 'Sri Sakthi Hostel',
    'Annamalai Boys PG', 'Vel Boys Hostel', 'Thamarai Boys PG', 'Kumaran Boys Hostel',
    'Aravind Boys PG', 'Surya Boys Hostel', 'Ganesh Boys PG', 'Karthik Residency',
    'Siva Boys Hostel', 'Pandian PG for Men', 'Nila Boys Hostel', 'Kaveri Boys PG',
    'Senthil Boys Hostel', 'Kovai Boys Home', 'Mani Boys Hostel', 'Rajan PG for Men',
    'Mahalakshmi Boys PG', 'Ponni Boys Hostel', 'Arul Boys PG', 'Durai Boys Hostel',
    'Bharathi Boys Hostel', 'Vaigai Boys PG', 'Sundaram Boys PG',
]

GIRLS_HOSTEL_NAMES = [
    'Tamilselvi Ladies Hostel', 'Amman Ladies PG', 'Lakshmi Women\'s Hostel',
    'Meenakshi Ladies PG', 'Sri Devi Ladies Hostel', 'Kavitha Women\'s PG',
    'Revathi Ladies Hostel', 'Annapurna Women\'s PG', 'Gowri Ladies Hostel',
    'Kamakshi Ladies PG', 'Saraswathi Women\'s Hostel', 'Parvathi Ladies PG',
    'Sowmya Ladies Hostel', 'Vijaya Women\'s PG', 'Mangai Ladies Hostel',
    'Padma Women\'s PG', 'Thulasi Ladies Hostel', 'Vasantham Women\'s PG',
    'Nirmala Ladies Hostel', 'Rathna Women\'s PG', 'Abirami Ladies PG',
    'Preethi Ladies Hostel', 'Selvi Women\'s PG', 'Janaki Ladies Hostel',
    'Chitra Women\'s PG', 'Mythili Ladies Hostel',
]

COLIVING_NAMES = [
    'Kovai Residency', 'Kongunadu Co-Living', 'Coimbatore Comfort Stay',
    'Noyyal Co-Living', 'Prozone Co-Living', 'Urban Nest Coimbatore',
    'Green Valley Co-Living', 'Coimbatore Heights', 'City Nest PG',
    'Kovai Heritage Stay', 'Sri Andal Co-Living', 'Marutham Co-Living',
    'Kovaipudur Heights', 'Tamil Nadu Comfort PG',
]

# ============================================================
# Review Templates
# ============================================================
POSITIVE_REVIEWS = [
    "Very clean rooms and good food. The warden is very friendly and helpful.",
    "Best hostel near my college. The WiFi speed is great and food is tasty.",
    "Excellent facilities at affordable price. Hot water and power backup always available.",
    "I have been staying here for 2 years. Very safe and secure environment with CCTV.",
    "Good vegetarian food. The study hall is well maintained and quiet.",
    "Rooms are spacious and well ventilated. Location is very convenient for college.",
    "The owner aunty is very caring. She makes sure we get homely food daily.",
    "Near bus stop, easy transport to college. Laundry facility is a big plus.",
    "RO water, clean bathrooms. Value for money PG in Coimbatore.",
    "Peaceful environment for studying. Mess food is really good, feels like home.",
    "Safe area for girls. The security is very good with separate entry for visitors.",
    "Good hostel with friendly co-residents. Weekend special meals are amazing.",
    "Attached bathroom and balcony. Best single room hostel near PSG Tech.",
    "WiFi is stable, power backup is reliable. Great for online classes and projects.",
    "Walking distance to bus stand and college. Very convenient location in Peelamedu.",
    "Clean, affordable and the food is decent. The geyser in bathroom is very useful.",
    "Study room with AC is a highlight. Very helpful for exam preparation.",
    "I shifted from another PG to here. Much better facilities and food quality.",
    "The rooms are cleaned every day. Very hygienic and well-maintained hostel.",
    "Good for working professionals too. Parking space for two-wheelers is available.",
]

MIXED_REVIEWS = [
    "Decent place. Food is average but rooms are clean. WiFi goes off sometimes.",
    "Good hostel but slightly far from bus stop. Auto-rickshaw costs extra.",
    "Rooms are okay. Food could be better. But the price is very reasonable.",
    "Nice place overall. Hot water is available only in the morning.",
    "Affordable PG. WiFi speed is slow during peak hours. Otherwise good.",
]

# Property image placeholders for realistic look
def get_property_images(prop_id, gender):
    """Return placeholder image URLs for properties."""
    # Use picsum.photos with seed for consistency
    base_ids = {
        'boys': [1029, 1031, 1048, 1052, 1054, 1057, 1060, 1067],
        'girls': [1005, 1010, 1015, 1018, 1021, 1025, 1028, 1033],
        'coliving': [1040, 1044, 1047, 1050, 1055, 1058, 1061, 1064],
    }
    seed_ids = base_ids.get(gender, base_ids['coliving'])
    offset = (prop_id * 3) % len(seed_ids)
    return [
        f'https://picsum.photos/seed/{seed_ids[(offset + i) % len(seed_ids)]}/800/600'
        for i in range(random.randint(3, 5))
    ]

# ============================================================
# Amenity definitions
# ============================================================
AMENITY_DEFS = [
    {'name': 'WiFi',               'icon': 'wifi',            'category': 'Basic'},
    {'name': 'AC',                 'icon': 'snowflake',       'category': 'Comfort'},
    {'name': 'Food Included',      'icon': 'utensils',        'category': 'Basic'},
    {'name': 'Laundry',            'icon': 'washing-machine', 'category': 'Facilities'},
    {'name': 'Parking',            'icon': 'car',             'category': 'Facilities'},
    {'name': 'CCTV',               'icon': 'camera',          'category': 'Security'},
    {'name': 'Power Backup',       'icon': 'zap',             'category': 'Basic'},
    {'name': 'RO Water',           'icon': 'droplets',        'category': 'Basic'},
    {'name': 'Study Hall',         'icon': 'book-open',       'category': 'Facilities'},
    {'name': 'Gym',                'icon': 'dumbbell',        'category': 'Premium'},
    {'name': 'Hot Water',          'icon': 'flame',           'category': 'Basic'},
    {'name': 'Geyser',             'icon': 'thermometer',     'category': 'Basic'},
    {'name': 'Attached Bathroom',  'icon': 'bath',            'category': 'Comfort'},
    {'name': 'TV Room',            'icon': 'tv',              'category': 'Facilities'},
    {'name': 'Two-Wheeler Parking','icon': 'bike',            'category': 'Facilities'},
]

# ============================================================
# House Rules Templates
# ============================================================
HOUSE_RULES = [
    'No smoking inside the premises',
    'Visitors allowed only in common area between 10 AM - 8 PM',
    'Gate closes at 10:00 PM',
    'Maintain silence after 10:30 PM',
    'No alcohol or drugs allowed',
    'Keep rooms and common areas clean',
    'Inform warden before going on leave',
    'ID proof mandatory at the time of admission',
    'One month notice before vacating',
    'Rent to be paid before 5th of every month',
    'No cooking allowed in rooms',
    'Separate entry for male and female visitors',
]


class Command(BaseCommand):
    help = 'Seeds the database with 100+ realistic Coimbatore properties'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('[START] Starting StayFinder Coimbatore seed...'))

        self._create_amenities()
        self._create_admin()
        owner_users = self._create_owners()
        student_users = self._create_students()
        properties = self._create_properties(owner_users)
        self._create_reviews(student_users, properties)

        self.stdout.write(self.style.SUCCESS(
            f'[DONE] Seeded: {len(owner_users)} owners, {len(student_users)} students, '
            f'{len(properties)} properties, {Review.objects.count()} reviews'
        ))

    def _create_amenities(self):
        self.stdout.write('  [+] Creating amenities...')
        for a in AMENITY_DEFS:
            Amenity.objects.get_or_create(name=a['name'], defaults=a)

    def _create_admin(self):
        self.stdout.write('  [+] Creating admin user...')
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@stayfinder.in',
                'role': 'admin',
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'is_verified': True,
                'is_superuser': True,
                'is_staff': True,
                'city': 'Coimbatore',
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(f'    [OK] Admin: admin@stayfinder.in / admin123')

    def _create_owners(self):
        self.stdout.write('  [+] Creating owner accounts...')
        owner_users = []
        for data in OWNERS:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'role': 'owner',
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'phone': data['phone'],
                    'is_verified': True,
                    'city': 'Coimbatore',
                }
            )
            if created:
                user.set_password('owner123')
                user.save()
                OwnerProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'business_name': data['business'],
                        'business_address': 'Coimbatore, Tamil Nadu',
                        'is_verified_owner': True,
                    }
                )
                self.stdout.write(f'    [OK] Owner: {data["email"]} / owner123')
            owner_users.append(user)
        return owner_users

    def _create_students(self):
        self.stdout.write('  [+] Creating student accounts...')
        student_users = []
        for data in STUDENTS:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'role': 'student',
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'gender': data['gender'],
                    'is_verified': True,
                    'city': 'Coimbatore',
                    'college': data['college'],
                }
            )
            if created:
                user.set_password('student123')
                user.save()
            student_users.append(user)
        self.stdout.write(f'    [OK] {len(student_users)} students (password: student123)')
        return student_users

    def _create_properties(self, owner_users):
        self.stdout.write('  [+] Creating 100+ properties...')
        if Property.objects.count() >= 80:
            self.stdout.write('    [SKIP] Properties already seeded, skipping.')
            return list(Property.objects.all())

        all_amenities = list(Amenity.objects.all())
        properties = []
        prop_counter = 0
        area_names = list(AREAS.keys())

        # Create ~5 properties per area = 100 total
        for area_name in area_names:
            area_data = AREAS[area_name]
            nearby_colleges = get_nearby_colleges(area_name)
            count_per_area = random.choice([4, 5, 6])

            for i in range(count_per_area):
                prop_counter += 1

                # Determine gender and pick name
                gender_roll = random.random()
                if gender_roll < 0.40:
                    gender = 'boys'
                    name = random.choice(BOYS_HOSTEL_NAMES)
                elif gender_roll < 0.80:
                    gender = 'girls'
                    name = random.choice(GIRLS_HOSTEL_NAMES)
                else:
                    gender = 'coliving'
                    name = random.choice(COLIVING_NAMES)

                # Add area name to prevent duplicate names
                display_name = f'{name} - {area_name}'

                # Property type
                ptype = random.choices(
                    ['pg', 'hostel', 'coliving', 'flat'],
                    weights=[45, 35, 15, 5],
                    k=1
                )[0]

                # Pricing based on area (premium areas cost more)
                premium_areas = ['RS Puram', 'Saibaba Colony', 'Peelamedu', 'Gandhipuram']
                base_min = random.randint(4000, 6000) if area_name in premium_areas else random.randint(3000, 5000)
                base_max = base_min + random.randint(1500, 4000)

                # Random offset for coordinates
                lat = float(area_data['lat']) + random.uniform(-0.008, 0.008)
                lng = float(area_data['lng']) + random.uniform(-0.008, 0.008)

                # Select amenities
                num_amenities = random.randint(5, 10)
                selected_amenities = random.sample(all_amenities, min(num_amenities, len(all_amenities)))
                amenity_names = [a.name for a in selected_amenities]

                # Food
                food_included = 'Food Included' in amenity_names or random.random() > 0.3
                food_type = random.choice(['Veg', 'Non-Veg', 'Veg & Non-Veg']) if food_included else ''

                total_beds = random.randint(20, 80)
                available_beds = random.randint(2, min(15, total_beds))

                # House rules
                rules = random.sample(HOUSE_RULES, random.randint(4, 7))

                owner = random.choice(owner_users)

                prop = Property.objects.create(
                    owner=owner,
                    name=display_name,
                    description=self._generate_description(display_name, area_name, nearby_colleges, gender, food_included, amenity_names),
                    property_type=ptype,
                    gender=gender,
                    address=f'{random.randint(1, 500)}, {random.choice(["Main Road", "Cross Street", "Layout", "Nagar", "Colony", "Bazaar Street"])}, {area_name}',
                    city='Coimbatore',
                    area=area_name,
                    state='Tamil Nadu',
                    pincode=area_data['pin'],
                    latitude=Decimal(str(round(lat, 7))),
                    longitude=Decimal(str(round(lng, 7))),
                    nearby_colleges=nearby_colleges if nearby_colleges else [random.choice(list(COLLEGE_AREAS.keys()))],
                    nearby_bus_stops=area_data['bus'],
                    nearby_railway_station='Coimbatore Junction' if area_name in ['Ukkadam', 'Gandhipuram', 'RS Puram', 'Hope College'] else 'Podanur Junction',
                    rent_min=Decimal(str(base_min)),
                    rent_max=Decimal(str(base_max)),
                    deposit=Decimal(str(base_min * 2)),
                    total_beds=total_beds,
                    available_beds=available_beds,
                    amenities_list=amenity_names,
                    house_rules=rules,
                    food_included=food_included,
                    food_type=food_type,
                    contact_phone=owner.phone,
                    contact_email=owner.email,
                    is_verified=random.random() > 0.15,  # 85% verified
                    is_active=True,
                    is_featured=prop_counter <= 12,  # First 12 are featured
                )

                # Add M2M amenities
                prop.amenities.add(*selected_amenities)

                # Create rooms
                self._create_rooms(prop, base_min, base_max)

                # Create images
                self._create_images(prop, gender)

                properties.append(prop)

        self.stdout.write(f'    [OK] Created {len(properties)} properties')
        return properties

    def _generate_description(self, name, area, colleges, gender, food, amenities):
        gender_text = {'boys': 'boys/men', 'girls': 'girls/women', 'coliving': 'boys and girls'}
        college_text = f' Conveniently located near {", ".join(colleges[:2])}.' if colleges else ''
        food_text = ' Homely food (breakfast, lunch, dinner) included in the rent.' if food else ''
        amenity_text = f' Facilities include {", ".join(amenities[:5])}.' if amenities else ''

        return (
            f'{name} is a well-maintained accommodation for {gender_text.get(gender, "all")} '
            f'in the heart of {area}, Coimbatore.{college_text}{food_text}{amenity_text} '
            f'We provide a safe, clean, and comfortable environment with 24/7 security. '
            f'Bus stops and essential shops are within walking distance. '
            f'Ideal for students and working professionals looking for affordable stays in Coimbatore.'
        )

    def _create_rooms(self, prop, rent_min, rent_max):
        room_configs = [
            ('single',    rent_max, True,  random.choice([True, False])),
            ('double',    int(rent_min + (rent_max - rent_min) * 0.5), random.choice([True, False]), False),
            ('triple',    rent_min, False, False),
        ]
        if random.random() > 0.5:
            room_configs.append(('dormitory', int(rent_min * 0.8), False, False))

        for rtype, rent, bathroom, ac in room_configs:
            total = random.randint(3, 15)
            Room.objects.create(
                property=prop,
                room_type=rtype,
                rent=Decimal(str(rent)),
                deposit=Decimal(str(rent * 2)),
                total_beds=total,
                available_beds=random.randint(0, min(5, total)),
                has_attached_bathroom=bathroom,
                has_ac=ac,
                has_balcony=random.random() > 0.7,
            )

    def _create_images(self, prop, gender):
        image_urls = get_property_images(prop.id, gender)
        for idx, url in enumerate(image_urls):
            PropertyImage.objects.create(
                property=prop,
                image_url=url,
                caption=f'View {idx + 1} of {prop.name}',
                is_primary=(idx == 0),
                order=idx,
            )

    def _create_reviews(self, students, properties):
        self.stdout.write('  [+] Creating reviews...')
        if Review.objects.count() >= 50:
            self.stdout.write('    [SKIP] Reviews already exist, skipping.')
            return

        review_count = 0
        for prop in properties:
            # 2-4 reviews per property
            num_reviews = random.randint(1, 4)
            reviewers = random.sample(students, min(num_reviews, len(students)))

            for student in reviewers:
                # Skip if review already exists
                if Review.objects.filter(user=student, property=prop).exists():
                    continue

                rating = random.choices([3, 4, 5], weights=[15, 40, 45], k=1)[0]
                if rating >= 4:
                    comment = random.choice(POSITIVE_REVIEWS)
                else:
                    comment = random.choice(MIXED_REVIEWS)

                Review.objects.create(
                    user=student,
                    property=prop,
                    rating=rating,
                    comment=comment,
                )
                review_count += 1

        self.stdout.write(f'    [OK] Created {review_count} reviews')
