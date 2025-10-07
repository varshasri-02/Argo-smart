from django.core.management.base import BaseCommand
from app.models import District, Region

class Command(BaseCommand):
    help = 'Setup districts and regions (taluks) for Tamil Nadu'

    def handle(self, *args, **kwargs):
        # Tamil Nadu districts with their taluks
        districts_data = {
            'Madurai': ['Madurai North', 'Madurai South', 'Madurai East', 'Madurai West', 'Melur', 'Peraiyur', 'Thirumangalam', 'Usilampatti', 'Vadipatti'],
            'Coimbatore': ['Coimbatore North', 'Coimbatore South', 'Anamalai', 'Annur', 'Kinathukadavu', 'Madukkarai', 'Mettupalayam', 'Perur', 'Pollachi', 'Sulur', 'Valparai'],
            'Chennai': ['Alandur', 'Ambattur', 'Aminjikarai', 'Ayanavaram', 'Egmore', 'Guindy', 'Madhavaram', 'Madhuravoyal', 'Mambalam', 'Mylapore', 'Perambur', 'Purasawalkam', 'Sholinganallur', 'Thiruvottiyur', 'Tondiarpet'],
            'Salem': ['Attur', 'Edappadi', 'Gangavalli', 'Kadayampatti', 'Mettur', 'Omalur', 'Pethanaickenpalayam', 'Salem', 'Sankagiri', 'Vazhapadi', 'Yercaud'],
            'Tiruchirappalli': ['Lalgudi', 'Manachanallur', 'Manapparai', 'Marungapuri', 'Musiri', 'Srirangam', 'Thottiyam', 'Thuraiyur', 'Tiruchirappalli', 'Tiruverumbur'],
            'Tirunelveli': ['Ambasamudram', 'Cheranmahadevi', 'Manur', 'Nanguneri', 'Palayamkottai', 'Radhapuram', 'Thisayanvilai', 'Tirunelveli'],
            'Erode': ['Anthiyur', 'Bhavani', 'Erode', 'Gobichettipalayam', 'Kodumudi', 'Modakurichi', 'Nambiyur', 'Perundurai', 'Sathyamangalam', 'Thalavadi'],
            'Vellore': ['Aanikattu', 'Gudiyatham', 'Katpadi', 'K.V.Kuppam', 'Pernambut', 'Vellore'],
            'Thanjavur': ['Budalur', 'Kumbakonam', 'Orathanadu', 'Papanasam', 'Pattukottai', 'Peravurani', 'Thanjavur', 'Thiruvaiyaru', 'Thiruvidaimarudur'],
            'Dindigul': ['Athoor', 'Dindigul East', 'Dindigul West', 'Guziliyamparai', 'Kodaikanal', 'Natham', 'Nilakottai', 'Oddanchatram', 'Palani', 'Vedasandur'],
            'Kanyakumari': ['Agasteeswaram', 'Kalkulam', 'Killiyoor', 'Thovalai', 'Vilavancode'],
            'Cuddalore': ['Cuddalore', 'Bhuvanagiri', 'Chidambaram', 'Kattumannarkoil', 'Kurinjipadi', 'Panruti', 'Tittakudi', 'Veppur', 'Virudhachalam'],
            'Dharmapuri': ['Dharmapuri', 'Harur', 'Karimangalam', 'Nallampalli', 'Palacode', 'Pappireddipatti', 'Pennagaram'],
            'Nagapattinam': ['Nagapattinam', 'Kilvelur', 'Thirukkuvalai', 'Vedaranyam', 'Mayiladuthurai', 'Sirkazhi', 'Tharangambadi'],
            'Viluppuram': ['Viluppuram', 'Gingee', 'Kandachipuram', 'Marakkanam', 'Melmalaiyanur', 'Thirukoilur', 'Tindivanam', 'Vanur', 'Vikravandi'],
            'Krishnagiri': ['Krishnagiri', 'Bargur', 'Denkanikottai', 'Hosur', 'Pochampalli', 'Shoolagiri', 'Uthangarai', 'Veppanahalli'],
            'Namakkal': ['Namakkal', 'Kolli Hills', 'Mohanur', 'Paramathi Velur', 'Rasipuram', 'Senthamangalam', 'Tiruchengode'],
            'Karur': ['Karur', 'Aravakurichi', 'Kadavur', 'Krishnarayapuram', 'Kulithalai', 'Manmangalam'],
            'Ariyalur': ['Ariyalur', 'Andimadam', 'Sendurai', 'Udayarpalayam'],
            'Perambalur': ['Perambalur', 'Alathur', 'Kunnam', 'Veppanthattai'],
            'Pudukkottai': ['Pudukkottai', 'Alangudi', 'Aranthangi', 'Avudaiyarkoil', 'Gandarvakottai', 'Iluppur', 'Karambakudi', 'Kulathur', 'Manamelkudi', 'Ponnamaravathi', 'Thirumayam', 'Viralimalai'],
            'Ramanathapuram': ['Ramanathapuram', 'Kadaladi', 'Kamuthi', 'Kilakarai', 'Mudukulathur', 'Paramakudi', 'Rajasingamangalam', 'Rameswaram', 'Tiruvadanai'],
            'Sivaganga': ['Sivaganga', 'Devakottai', 'Ilayankudi', 'Kalaiyarkovil', 'Karaikudi', 'Manamadurai', 'Singampunari', 'Thirupathur', 'Tirupuvanam'],
            'Theni': ['Theni', 'Aandipatti', 'Bodinayakanur', 'Periyakulam', 'Uthamapalayam'],
            'Virudhunagar': ['Virudhunagar', 'Aruppukkottai', 'Kariyapatti', 'Rajapalayam', 'Sathur', 'Sivakasi', 'Srivilliputhur', 'Tiruchuli', 'Vembakottai', 'Watrap'],
            'Thoothukudi': ['Thoothukudi', 'Eral', 'Ettayapuram', 'Kayathar', 'Kovilpatti', 'Ottapidaram', 'Sathankulam', 'Srivaikundam', 'Tiruchendur', 'Vilathikulam'],
            'Tiruvarur': ['Tiruvarur', 'Koothanallur', 'Kudavasal', 'Mannargudi', 'Nannilam', 'Needamangalam', 'Thiruthuraipoondi', 'Valangaiman'],
            'Kanchipuram': ['Kanchipuram', 'Kundrathur', 'Sriperumbudur', 'Uthiramerur', 'Walajabad'],
            'Tiruvannamalai': ['Tiruvannamalai', 'Arani', 'Arni', 'Chengam', 'Chetpet', 'Cheyyar', 'Jamunamarathur', 'Kalasapakkam', 'Kilpennathur', 'Polur', 'Thandrampattu', 'Thandrampet', 'Vandavasi', 'Vembakkam'],
            'Tiruvallur': ['Tiruvallur', 'Avadi', 'Gummidipoondi', 'Pallipattu', 'Ponneri', 'Poonamallee', 'R.K. Pet', 'Tiruttani', 'Uthukottai'],
            'Nilgiris': ['Udhagamandalam', 'Coonoor', 'Gudalur', 'Kotagiri', 'Kundah', 'Panthalur'],
            'Tenkasi': ['Tenkasi', 'Alangulam', 'Kadayanallur', 'Sankarankovil', 'Shencottai', 'Sivagiri', 'Veerakeralampudur'],
            'Tiruppur': ['Tiruppur North', 'Tiruppur South', 'Avinashi', 'Dharapuram', 'Kangayam', 'Madathukulam', 'Palladam', 'Udumalpet', 'Uthukuli'],
            'Ranipet': ['Ranipet', 'Arakkonam', 'Arcot', 'Sholinghur', 'Walajah'],
            'Tirupathur': ['Tirupathur', 'Ambur', 'Natrampalli', 'Vaniyambadi'],
            'Kallakurichi': ['Kallakurichi', 'Chinnaselam', 'Kalvarayan Hills', 'Sankarapuram', 'Tirukoilur', 'Ulundurpet'],
            'Chengalpattu': ['Chengalpattu', 'Cheyyur', 'Maduranthakam', 'Pallavaram', 'Tambaram', 'Thiruporur', 'Vandalur'],
        }
        
        total_districts = 0
        total_regions = 0
        
        for district_name, taluks in districts_data.items():
            district, created = District.objects.get_or_create(name=district_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created District: {district_name}'))
                total_districts += 1
            else:
                self.stdout.write(f'  District already exists: {district_name}')
            
            # Add taluks/regions
            for taluk_name in taluks:
                region, created = Region.objects.get_or_create(
                    district=district, 
                    name=taluk_name
                )
                if created:
                    self.stdout.write(f'    ✓ Added Taluk: {taluk_name}')
                    total_regions += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n========================================'))
        self.stdout.write(self.style.SUCCESS(f'✓ Setup Complete!'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total Districts: {len(districts_data)}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Total Regions/Taluks: {sum(len(v) for v in districts_data.values())}'))
        self.stdout.write(self.style.SUCCESS(f'========================================'))