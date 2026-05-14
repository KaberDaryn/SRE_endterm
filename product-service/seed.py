from application import create_app, db
from application.models import Product

app = create_app()

with app.app_context():
    db.create_all()  # ensure tables exist
    if Product.query.count() == 0:
        products = [
            Product(name='Laptop',  slug='laptop',  price=1200, image='product1.jpg'),
            Product(name='Phone',   slug='phone',   price=800,  image='product2.jpg'),
            Product(name='Camera',  slug='camera',  price=500,  image='sample.jpg'),
        ]
        db.session.add_all(products)
        db.session.commit()
        print("Seeded 3 products OK")
    else:
        print(f"Already has {Product.query.count()} products - skipping")
