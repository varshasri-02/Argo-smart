from django.core.management.base import BaseCommand
from app.models import District, Region, SoilLocationDetail, Soil, SoilDetail, RainfallDetail, Year
import random

class Command(BaseCommand):
    help = 'Populate comprehensive soil data, rainfall data, and soil details'

    def handle(self, *args, **kwargs):
        # Step 1: Add Soil Types
        self.stdout.write('\n--- Adding Soil Types ---')
        soil_types = {
            'Red Soil': {
                'detail': 'Red soil is rich in iron and is suitable for crops like groundnut, pulses, and millets. It has good drainage but low water retention capacity.',
                'crop': 'Groundnut, Cotton, Wheat, Pulses, Millets, Tobacco'
            },
            'Black Soil': {
                'detail': 'Black soil is rich in calcium, magnesium, and iron. It has excellent water retention capacity and is ideal for cotton cultivation.',
                'crop': 'Cotton, Wheat, Jowar, Linseed, Sunflower, Millets'
            },
            'Alluvial Soil': {
                'detail': 'Alluvial soil is highly fertile and suitable for a wide variety of crops. It is rich in potash but poor in phosphorus.',
                'crop': 'Rice, Wheat, Sugarcane, Maize, Cotton, Jute, Vegetables'
            },
            'Laterite Soil': {
                'detail': 'Laterite soil is acidic and has low fertility. With proper treatment and irrigation, it can be used for tea, coffee, and cashew cultivation.',
                'crop': 'Tea, Coffee, Cashew, Rubber, Coconut'
            },
            'Sandy Soil': {
                'detail': 'Sandy soil has large particles with good drainage but poor water and nutrient retention. Suitable for drought-resistant crops.',
                'crop': 'Millets, Groundnut, Castor, Watermelon, Muskmelon'
            },
            'Clay Soil': {
                'detail': 'Clay soil has very fine particles with excellent water retention but poor drainage. Rich in nutrients and suitable for rice cultivation.',
                'crop': 'Rice, Wheat, Sugarcane, Cotton, Pulses'
            },
            'Loamy Soil': {
                'detail': 'Loamy soil is a balanced mixture of sand, silt, and clay. It has good water retention, drainage, and fertility.',
                'crop': 'Vegetables, Fruits, Wheat, Sugarcane, Cotton, Maize'
            }
        }
        
        for soil_name, info in soil_types.items():
            soil, created = Soil.objects.get_or_create(name=soil_name)
            if created:
                self.stdout.write(f'Created soil type: {soil_name}')
            
            # Add or update soil detail
            SoilDetail.objects.update_or_create(
                soil=soil,
                defaults={
                    'detail': info['detail'],
                    'crop': info['crop']
                }
            )
            self.stdout.write(f'  Added/Updated details for: {soil_name}')
        
        # Step 2: Add Years
        self.stdout.write('\n--- Adding Years ---')
        years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
        for year_num in years:
            Year.objects.get_or_create(name=year_num)
        self.stdout.write(f'Added {len(years)} years')
        
        # Step 3: Add Comprehensive Soil Location Data for ALL Districts
        self.stdout.write('\n--- Adding Soil Location Data ---')
        
        # Get ALL districts
        districts = District.objects.all()
        
        # Soil parameter ranges for different soil types
        soil_params = {
            'Red Soil': {'oc': (0.4, 0.7), 'p': (30, 50), 'k': (200, 300), 'mn': (6, 10), 's': (8, 15), 'ph': (6.0, 7.5)},
            'Black Soil': {'oc': (0.6, 1.0), 'p': (40, 70), 'k': (300, 500), 'mn': (8, 15), 's': (12, 25), 'ph': (7.0, 8.5)},
            'Alluvial Soil': {'oc': (0.5, 0.9), 'p': (35, 60), 'k': (250, 400), 'mn': (7, 12), 's': (10, 20), 'ph': (6.5, 8.0)},
            'Laterite Soil': {'oc': (0.3, 0.6), 'p': (20, 40), 'k': (150, 250), 'mn': (5, 9), 's': (5, 12), 'ph': (5.0, 6.5)},
            'Sandy Soil': {'oc': (0.2, 0.5), 'p': (15, 35), 'k': (100, 200), 'mn': (3, 7), 's': (4, 10), 'ph': (6.0, 7.5)},
            'Clay Soil': {'oc': (0.7, 1.2), 'p': (45, 80), 'k': (350, 550), 'mn': (10, 18), 's': (15, 30), 'ph': (6.5, 8.0)},
            'Loamy Soil': {'oc': (0.6, 1.0), 'p': (40, 65), 'k': (280, 450), 'mn': (8, 14), 's': (12, 22), 'ph': (6.5, 7.5)},
        }
        
        count = 0
        for district in districts:
            # Get regions for this district
            regions = Region.objects.filter(district=district)
            
            if not regions.exists():
                # Create default regions if none exist
                Region.objects.create(district=district, name=f'{district.name} North')
                Region.objects.create(district=district, name=f'{district.name} South')
                regions = Region.objects.filter(district=district)
            
            # Assign 1-2 soil types per region
            soil_types_list = list(soil_params.keys())
            
            for region in regions:
                # Randomly select 1-2 soil types for this region
                num_soils = random.randint(1, 2)
                selected_soils = random.sample(soil_types_list, num_soils)
                
                for soil_name in selected_soils:
                    params = soil_params[soil_name]
                    
                    # Generate random values within the range for each parameter
                    data = {
                        'oc': round(random.uniform(*params['oc']), 2),
                        'p': round(random.uniform(*params['p']), 1),
                        'k': round(random.uniform(*params['k']), 1),
                        'mn': round(random.uniform(*params['mn']), 1),
                        's': round(random.uniform(*params['s']), 1),
                        'ph': round(random.uniform(*params['ph']), 1),
                    }
                    
                    soil_detail, created = SoilLocationDetail.objects.update_or_create(
                        district=district,
                        region=region,
                        defaults={
                            'organic_carbon': data['oc'],
                            'phosphorous': data['p'],
                            'potassium': data['k'],
                            'manganese': data['mn'],
                            'sulphur': data['s'],
                            'ph_value': data['ph'],
                            'status': True
                        }
                    )
                    if created:
                        count += 1
                        self.stdout.write(f'Added soil data for {district.name} - {region.name}')
        
        self.stdout.write(f'Total soil location records: {count}')
        
        # Step 4: Add Comprehensive Rainfall Data for ALL Districts
        self.stdout.write('\n--- Adding Rainfall Data ---')
        
        # Tamil Nadu districts with realistic rainfall patterns (in cm per year)
        # Districts with higher rainfall (coastal and hilly areas)
        high_rainfall_districts = ['Chennai', 'Kanyakumari', 'Nilgiris', 'Thanjavur', 'Nagapattinam', 
                                   'Tiruvarur', 'Cuddalore', 'Villupuram']
        
        # Districts with moderate rainfall
        moderate_rainfall_districts = ['Coimbatore', 'Salem', 'Tiruchirappalli', 'Madurai', 'Vellore',
                                      'Tiruvannamalai', 'Dindigul', 'Theni']
        
        # Districts with lower rainfall
        low_rainfall_districts = ['Ramanathapuram', 'Sivaganga', 'Virudhunagar', 'Thoothukudi',
                                 'Tirunelveli', 'Erode', 'Karur']
        
        rainfall_count = 0
        for district in districts:
            district_name = district.name
            
            # Determine base rainfall based on district category
            if district_name in high_rainfall_districts:
                base_rainfall = random.randint(110, 160)
            elif district_name in moderate_rainfall_districts:
                base_rainfall = random.randint(75, 110)
            else:
                base_rainfall = random.randint(50, 75)
            
            # Generate rainfall data for each year with some variation
            for year_num in years:
                year = Year.objects.get(name=year_num)
                
                # Add random variation (+/- 15%)
                variation = random.uniform(0.85, 1.15)
                rainfall = round(base_rainfall * variation, 1)
                
                RainfallDetail.objects.update_or_create(
                    district=district,
                    year=year,
                    defaults={'rainfall': rainfall}
                )
                rainfall_count += 1
            
            self.stdout.write(f'Added rainfall data for {district_name}')
        
        self.stdout.write(f'Total rainfall records: {rainfall_count}')
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(f'Soil Types: {Soil.objects.count()}')
        self.stdout.write(f'Soil Details: {SoilDetail.objects.count()}')
        self.stdout.write(f'Districts: {District.objects.count()}')
        self.stdout.write(f'Regions: {Region.objects.count()}')
        self.stdout.write(f'Soil Location Data: {SoilLocationDetail.objects.count()}')
        self.stdout.write(f'Rainfall Records: {RainfallDetail.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\n✓ Database populated successfully with comprehensive data!'))