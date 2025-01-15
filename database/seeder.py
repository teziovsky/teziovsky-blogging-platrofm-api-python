from faker import Faker
from sqlalchemy.orm import Session

from .config import SessionLocal
from .models import Post

fake = Faker()


def seed_posts(db: Session, num_posts: int = 50):
    """Seed the database with fake blog posts."""
    posts = []
    categories = ["Technology", "Travel", "Food", "Lifestyle", "Programming"]

    for _ in range(num_posts):
        post = Post(
            title=fake.sentence(),
            content=fake.text(max_nb_chars=2000),
            category=fake.random_element(categories),
            tags=[fake.word() for _ in range(fake.random_int(min=1, max=5))],
        )
        posts.append(post)

    db.add_all(posts)
    db.commit()
    return posts


def run_seeds():
    """Run all seeders."""
    db = SessionLocal()
    try:
        seed_posts(db)
    finally:
        db.close()


if __name__ == "__main__":
    run_seeds()
