from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine

# Create all tables
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(models.Location).count() > 0:
            print("Database already seeded.")
            return
        
        # Seed Locations
        phuket = models.Location(
            name="Phuket",
            region="Phuket",
            description="Thailand's largest island known for beautiful beaches, nightlife, and water sports.",
            latitude=7.9519,
            longitude=98.3381
        )
        
        patong = models.Location(
            name="Patong",
            region="Phuket",
            description="Phuket's main tourist resort, known for its beach and nightlife.",
            latitude=7.8965,
            longitude=98.2999
        )
        
        kata = models.Location(
            name="Kata",
            region="Phuket",
            description="A beach resort on Phuket's west coast, popular for surfing.",
            latitude=7.8206,
            longitude=98.2987
        )
        
        karon = models.Location(
            name="Karon",
            region="Phuket",
            description="A long beach with a relaxed atmosphere in Phuket.",
            latitude=7.8492,
            longitude=98.2948
        )
        
        krabi_town = models.Location(
            name="Krabi Town",
            region="Krabi",
            description="The capital of Krabi province, a gateway to nearby islands and beaches.",
            latitude=8.0863,
            longitude=98.9063
        )
        
        ao_nang = models.Location(
            name="Ao Nang",
            region="Krabi",
            description="A resort town in Krabi known for its beaches and limestone cliffs.",
            latitude=8.0419,
            longitude=98.8108
        )
        
        railay = models.Location(
            name="Railay",
            region="Krabi",
            description="A small peninsula accessible only by boat, known for rock climbing and beaches.",
            latitude=8.0119,
            longitude=98.8366
        )
        
        phi_phi = models.Location(
            name="Phi Phi Islands",
            region="Krabi",
            description="A group of islands known for stunning beaches and clear waters.",
            latitude=7.7407,
            longitude=98.7784
        )
        
        db.add_all([phuket, patong, kata, karon, krabi_town, ao_nang, railay, phi_phi])
        db.commit()
        
        # Seed Accommodations
        accommodations = [
            models.Accommodation(
                name="Phuket Marriott Resort & Spa, Merlin Beach",
                type="Resort",
                location_id=patong.id,
                description="Luxury beachfront resort with multiple pools and restaurants.",
                price_per_night=150.0,
                rating=4.5,
                amenities="Swimming Pool, Spa, Restaurant, Free WiFi, Fitness Center",
                image_url="https://example.com/phuket-marriott.jpg"
            ),
            models.Accommodation(
                name="Kata Rocks",
                type="Resort",
                location_id=kata.id,
                description="Luxury oceanfront resort with private infinity pools.",
                price_per_night=300.0,
                rating=4.8,
                amenities="Private Pool, Spa, Restaurant, Free WiFi, Ocean View",
                image_url="https://example.com/kata-rocks.jpg"
            ),
            models.Accommodation(
                name="Hilton Phuket Arcadia Resort & Spa",
                type="Resort",
                location_id=karon.id,
                description="Sprawling resort with tropical gardens and multiple pools.",
                price_per_night=180.0,
                rating=4.3,
                amenities="Swimming Pool, Spa, Restaurant, Free WiFi, Tennis Court",
                image_url="https://example.com/hilton-phuket.jpg"
            ),
            models.Accommodation(
                name="Krabi Resort",
                type="Resort",
                location_id=ao_nang.id,
                description="Beachfront resort with traditional Thai architecture.",
                price_per_night=120.0,
                rating=4.2,
                amenities="Swimming Pool, Restaurant, Free WiFi, Beach Access",
                image_url="https://example.com/krabi-resort.jpg"
            ),
            models.Accommodation(
                name="Railay Princess Resort & Spa",
                type="Resort",
                location_id=railay.id,
                description="Resort surrounded by limestone cliffs with a pool and spa.",
                price_per_night=140.0,
                rating=4.0,
                amenities="Swimming Pool, Spa, Restaurant, Free WiFi",
                image_url="https://example.com/railay-princess.jpg"
            ),
            models.Accommodation(
                name="Phi Phi Island Village Beach Resort",
                type="Resort",
                location_id=phi_phi.id,
                description="Beachfront resort with traditional Thai bungalows.",
                price_per_night=200.0,
                rating=4.6,
                amenities="Swimming Pool, Spa, Restaurant, Free WiFi, Water Sports",
                image_url="https://example.com/phi-phi-village.jpg"
            ),
            models.Accommodation(
                name="The Slate",
                type="Resort",
                location_id=phuket.id,
                description="Unique design resort inspired by Phuket's tin mining past.",
                price_per_night=220.0,
                rating=4.7,
                amenities="Swimming Pool, Spa, Restaurant, Free WiFi, Fitness Center",
                image_url="https://example.com/the-slate.jpg"
            ),
            models.Accommodation(
                name="Dusit Thani Krabi Beach Resort",
                type="Resort",
                location_id=krabi_town.id,
                description="Elegant beachfront resort with extensive facilities.",
                price_per_night=190.0,
                rating=4.4,
                amenities="Swimming Pool, Spa, Restaurant, Free WiFi, Tennis Court",
                image_url="https://example.com/dusit-thani.jpg"
            )
        ]
        
        db.add_all(accommodations)
        db.commit()
        
        # Seed Transfers
        transfers = [
            models.Transfer(
                from_location_id=phuket.id,
                to_location_id=patong.id,
                type="Car",
                duration_minutes=30,
                price=15.0,
                description="Private car transfer from Phuket Airport to Patong Beach."
            ),
            models.Transfer(
                from_location_id=phuket.id,
                to_location_id=kata.id,
                type="Car",
                duration_minutes=45,
                price=20.0,
                description="Private car transfer from Phuket Airport to Kata Beach."
            ),
            models.Transfer(
                from_location_id=phuket.id,
                to_location_id=karon.id,
                type="Car",
                duration_minutes=40,
                price=18.0,
                description="Private car transfer from Phuket Airport to Karon Beach."
            ),
            models.Transfer(
                from_location_id=krabi_town.id,
                to_location_id=ao_nang.id,
                type="Car",
                duration_minutes=30,
                price=12.0,
                description="Private car transfer from Krabi Airport to Ao Nang."
            ),
            models.Transfer(
                from_location_id=ao_nang.id,
                to_location_id=railay.id,
                type="Longtail Boat",
                duration_minutes=15,
                price=10.0,
                description="Traditional longtail boat from Ao Nang to Railay Beach."
            ),
            models.Transfer(
                from_location_id=krabi_town.id,
                to_location_id=phi_phi.id,
                type="Ferry",
                duration_minutes=90,
                price=25.0,
                description="Ferry transfer from Krabi to Phi Phi Islands."
            ),
            models.Transfer(
                from_location_id=phuket.id,
                to_location_id=phi_phi.id,
                type="Speedboat",
                duration_minutes=60,
                price=40.0,
                description="Fast speedboat transfer from Phuket to Phi Phi Islands."
            ),
            models.Transfer(
                from_location_id=phuket.id,
                to_location_id=krabi_town.id,
                type="Car",
                duration_minutes=150,
                price=50.0,
                description="Private car transfer from Phuket to Krabi Town."
            )
        ]
        
        db.add_all(transfers)
        db.commit()
        
        # Seed Activities
        activities = [
            models.Activity(
                name="Phi Phi Islands Tour",
                location_id=phi_phi.id,
                type="Island Hopping",
                description="Full-day tour of the stunning Phi Phi Islands including Maya Bay and Monkey Beach.",
                duration_minutes=480,
                price=80.0,
                rating=4.7,
                image_url="https://example.com/phi-phi-tour.jpg"
            ),
            models.Activity(
                name="Phang Nga Bay Tour",
                location_id=phuket.id,
                type="Boat Tour",
                description="Explore the limestone karsts of Phang Nga Bay, including James Bond Island.",
                duration_minutes=480,
                price=70.0,
                rating=4.5,
                image_url="https://example.com/phang-nga-tour.jpg"
            ),
            models.Activity(
                name="Patong Nightlife Tour",
                location_id=patong.id,
                type="Nightlife",
                description="Experience the vibrant nightlife of Patong Beach, including Bangla Road.",
                duration_minutes=240,
                price=40.0,
                rating=4.0,
                image_url="https://example.com/patong-nightlife.jpg"
            ),
            models.Activity(
                name="Four Islands Tour",
                location_id=ao_nang.id,
                type="Island Hopping",
                description="Visit four beautiful islands around Krabi: Poda, Chicken, Tup, and Phra Nang Cave.",
                duration_minutes=360,
                price=60.0,
                rating=4.6,
                image_url="https://example.com/four-islands.jpg"
            ),
            models.Activity(
                name="Rock Climbing in Railay",
                location_id=railay.id,
                type="Adventure",
                description="Rock climbing experience on the limestone cliffs of Railay Beach.",
                duration_minutes=240,
                price=50.0,
                rating=4.8,
                image_url="https://example.com/railay-climbing.jpg"
            ),
            models.Activity(
                name="Elephant Sanctuary Visit",
                location_id=phuket.id,
                type="Wildlife",
                description="Visit an ethical elephant sanctuary to learn about and interact with rescued elephants.",
                duration_minutes=300,
                price=65.0,
                rating=4.9,
                image_url="https://example.com/elephant-sanctuary.jpg"
            ),
            models.Activity(
                name="Thai Cooking Class",
                location_id=krabi_town.id,
                type="Cultural",
                description="Learn to cook authentic Thai dishes with local ingredients.",
                duration_minutes=180,
                price=45.0,
                rating=4.7,
                image_url="https://example.com/thai-cooking.jpg"
            ),
            models.Activity(
                name="Big Buddha Phuket",
                location_id=phuket.id,
                type="Sightseeing",
                description="Visit the iconic 45-meter tall Big Buddha statue with panoramic views of Phuket.",
                duration_minutes=120,
                price=0.0,  # Free activity
                rating=4.5,
                image_url="https://example.com/big-buddha.jpg"
            ),
            models.Activity(
                name="Tiger Cave Temple",
                location_id=krabi_town.id,
                type="Sightseeing",
                description="Climb 1,237 steps to reach this sacred Buddhist temple with stunning views.",
                duration_minutes=180,
                price=0.0,  # Free activity
                rating=4.6,
                image_url="https://example.com/tiger-cave.jpg"
            ),
            models.Activity(
                name="Similan Islands Snorkeling",
                location_id=phuket.id,
                type="Water Sports",
                description="Full-day snorkeling trip to the pristine Similan Islands.",
                duration_minutes=600,
                price=100.0,
                rating=4.8,
                image_url="https://example.com/similan-snorkeling.jpg"
            )
        ]
        
        db.add_all(activities)
        db.commit()
        
        # Seed Itineraries
        itineraries = []
        
        # 2-night Phuket Itinerary
        phuket_short = models.Itinerary(
            name="Phuket Quick Escape",
            description="A short 2-night getaway to experience the highlights of Phuket.",
            num_nights=2,
            total_price=350.0,
            is_recommended=True,
            regions="Phuket"
        )
        itineraries.append(phuket_short)
        
        # 4-night Phuket Itinerary
        phuket_medium = models.Itinerary(
            name="Phuket Explorer",
            description="A 4-night adventure exploring the best of Phuket and nearby islands.",
            num_nights=4,
            total_price=650.0,
            is_recommended=True,
            regions="Phuket"
        )
        itineraries.append(phuket_medium)
        
        # 3-night Krabi Itinerary
        krabi_short = models.Itinerary(
            name="Krabi Highlights",
            description="A 3-night trip to experience the natural beauty of Krabi.",
            num_nights=3,
            total_price=450.0,
            is_recommended=True,
            regions="Krabi"
        )
        itineraries.append(krabi_short)
        
        # 5-night Krabi Itinerary
        krabi_medium = models.Itinerary(
            name="Krabi Adventure",
            description="A 5-night adventure exploring Krabi and its surrounding islands.",
            num_nights=5,
            total_price=750.0,
            is_recommended=True,
            regions="Krabi"
        )
        itineraries.append(krabi_medium)
        
        # 7-night Phuket & Krabi Itinerary
        phuket_krabi_long = models.Itinerary(
            name="Phuket & Krabi Discovery",
            description="A comprehensive 7-night journey through the best of Phuket and Krabi.",
            num_nights=7,
            total_price=1200.0,
            is_recommended=True,
            regions="Phuket, Krabi"
        )
        itineraries.append(phuket_krabi_long)
        
        # 8-night Ultimate Thailand Itinerary
        ultimate_thailand = models.Itinerary(
            name="Ultimate Thailand Beach Experience",
            description="An 8-night luxury experience of Thailand's most beautiful beaches and islands.",
            num_nights=8,
            total_price=1500.0,
            is_recommended=True,
            regions="Phuket, Krabi, Phi Phi"
        )
        itineraries.append(ultimate_thailand)
        
        db.add_all(itineraries)
        db.commit()
        
        # Add accommodations, transfers, and activities to itineraries
        # This is a simplified version - in a real application, you would add specific day numbers
        
        # Phuket Quick Escape (2 nights)
        db.execute(itinerary_accommodation.insert().values(itinerary_id=phuket_short.id, accommodation_id=1, day_number=1))
        db.execute(itinerary_accommodation.insert().values(itinerary_id=phuket_short.id, accommodation_id=1, day_number=2))
        db.execute(itinerary_transfer.insert().values(itinerary_id=phuket_short.id, transfer_id=1, day_number=1))
        db.execute(itinerary_activity.insert().values(itinerary_id=phuket_short.id, activity_id=3, day_number=1))
        db.execute(itinerary_activity.insert().values(itinerary_id=phuket_short.id, activity_id=8, day_number=2))
        
        # Phuket Explorer (4 nights)
        for day in range(1, 5):
            db.execute(itinerary_accommodation.insert().values(itinerary_id=phuket_medium.id, accommodation_id=1, day_number=day))
        db.execute(itinerary_transfer.insert().values(itinerary_id=phuket_medium.id, transfer_id=1, day_number=1))
        db.execute(itinerary_activity.insert().values(itinerary_id=phuket_medium.id, activity_id=2, day_number=2))
        db.execute(itinerary_activity.insert().values(itinerary_id=phuket_medium.id, activity_id=3, day_number=3))
        db.execute(itinerary_activity.insert().values(itinerary_id=phuket_medium.id, activity_id=6, day_number=4))
        
        # Krabi Highlights (3 nights)
        for day in range(1, 4):
            db.execute(itinerary_accommodation.insert().values(itinerary_id=krabi_short.id, accommodation_id=4, day_number=day))
        db.execute(itinerary_transfer.insert().values(itinerary_id=krabi_short.id, transfer_id=4, day_number=1))
        db.execute(itinerary_activity.insert().values(itinerary_id=krabi_short.id, activity_id=4, day_number=2))
        db.execute(itinerary_activity.insert().values(itinerary_id=krabi_short.id, activity_id=9, day_number=3))
        
        # Add more associations for other itineraries...
        
        db.commit()
        
        print("Database seeded successfully!")
    
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
