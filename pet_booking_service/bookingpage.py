class Pet:
    def __init__(self, name, animal_type, age):
        self.name = name
        self.animal_type = animal_type
        self.age = age

    def __str__(self):
        return f"{self.name} ({self.animal_type}), Age: {self.age}"


class Service:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def __str__(self):
        return f"{self.name}: {self.description} - ${self.price:.2f}"


class Booking:
    def __init__(self, pet, service, date):
        self.pet = pet
        self.service = service
        self.date = date

    def __str__(self):
        return f"Booking for {self.pet.name} ({self.pet.animal_type}): {self.service.name} on {self.date}"

# Example usage:

# Create some pets
pet1 = Pet("Buddy", "Dog", 5)
pet2 = Pet("Whiskers", "Cat", 3)

# Create some services
service1 = Service("Dog Grooming", "Full grooming session for dogs", 50.00)
service2 = Service("Cat Boarding", "Boarding services for cats", 30.00)

# Bookings
booking1 = Booking(pet1, service1, "2024-04-25")
booking2 = Booking(pet2, service2, "2024-05-01")

# Display information
print("Pets:")
print(pet1)
print(pet2)
print("\nServices:")
print(service1)
print(service2)
print("\nBookings:")
print(booking1)
print(booking2)
