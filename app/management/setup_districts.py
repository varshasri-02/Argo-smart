from django.core.management.base import BaseCommand
from app.models import District, Region, SoilLocationDetail

class Command(BaseCommand):
    help = 'Setup districts and basic data'

    def handle(self, *args, **kwargs):
        # Tamil Nadu districts
        districts = [
            'Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore',
            'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kanchipuram',
            'Kanyakumari', 'Karur', 'Krishnagiri', 'Madurai', 'Nagapattinam',
            'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai', 'Ramanathapuram',
            'Ranipet', 'Salem', 'Sivaganga', 'Tenkasi', 'Thanjavur',
            'Theni', 'Thoothukudi', 'Tiruchirappalli', 'Tirunelveli', 'Tirupathur',
            'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Vellore',
            'Viluppuram', 'Virudhunagar'
        ]
        
        for district_name in districts:
            district, created = District.objects.get_or_create(name=district_name)
            if created:
                self.stdout.write(f'✓ Created: {district_name}')
                
                # Add sample regions
                Region.objects.get_or_create(district=district, name=f'{district_name} North')
                Region.objects.get_or_create(district=district, name=f'{district_name} South')
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully added {len(districts)} districts!'))