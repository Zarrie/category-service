from categories.models import Category, CategorySimilarity
from django.db import transaction


def run():
    with transaction.atomic():
        print("Clearing old data...")
        CategorySimilarity.objects.all().delete()
        Category.objects.all().delete()

        print("Creating categories...")

        # Root categories
        food = Category.objects.create(name="Храни", description="Всички основни храни")
        drinks = Category.objects.create(name="Напитки", description="Всички видове напитки")
        household = Category.objects.create(name="Домакинство", description="Продукти за дома")

        # Subcategories
        fruits = Category.objects.create(name="Плодове", parent=food, description="Свежи плодове")
        veggies = Category.objects.create(name="Зеленчуци", parent=food, description="Свежи зеленчуци")
        meat = Category.objects.create(name="Месо и риба", parent=food, description="Прясно месо и риба")
        dairy = Category.objects.create(name="Млечни продукти", parent=food, description="Мляко, сирена, кашкавал")

        soft_drinks = Category.objects.create(name="Безалкохолни", parent=drinks)
        alcoholic = Category.objects.create(name="Алкохол", parent=drinks)

        cleaning = Category.objects.create(name="Почистващи", parent=household)
        paper = Category.objects.create(name="Хартиени продукти", parent=household)

        print("Creating similarities...")

        # Similarities (bidirectional pairs)
        CategorySimilarity.objects.create(cat_left=fruits, cat_right=veggies)
        CategorySimilarity.objects.create(cat_left=fruits, cat_right=dairy)
        CategorySimilarity.objects.create(cat_left=meat, cat_right=dairy)
        CategorySimilarity.objects.create(cat_left=soft_drinks, cat_right=alcoholic)
        CategorySimilarity.objects.create(cat_left=cleaning, cat_right=paper)

        print("Done. Created categories and similarity pairs.")

        print("\nCategory IDs:")
        for c in Category.objects.all():
            print(f"{c.id}: {c.name}")

        print("\nTry endpoints such as:")
        print("  GET /api/categories/")
        print(f"  GET /api/categories/{fruits.id}/similar/")
        print("  python manage.py rabbits")


if __name__ == "__main__":
    run()
