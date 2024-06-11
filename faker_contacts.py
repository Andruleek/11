import asyncio
from faker import Faker
from datetime import datetime
from src.database.db import sessionmanager
from src.database.models import Contact

fake = Faker()

async def create_fake_contacts(num_contacts: int):
    async with sessionmanager.session() as db:
        for _ in range(num_contacts):
            fake_contact = Contact(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone_number=fake.phone_number(),
                birthday=fake.date_of_birth(minimum_age=18, maximum_age=90),
            )
            db.add(fake_contact)
        await db.commit()

# Вызываем функцию для создания 30 фейковых контактов
if __name__ == "__main__":
    asyncio.run(create_fake_contacts(num_contacts=30))



