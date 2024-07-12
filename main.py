from flask import Flask, request, render_template, redirect, url_for
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

app = Flask(__name__)

db = sqlalchemy.create_engine("sqlite:///news-books-collection.db")
Session = sessionmaker(bind=db)
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    author: Mapped[str]
    rating: Mapped[int]

Base.metadata.create_all(db)

@app.route("/")
def front_page():
    with Session() as session:
        books = session.query(Book).all()
    return render_template("index.html", the_length=len(books), books=books)

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        with Session() as session:
            session.add(new_book)
            session.commit()
        return redirect(url_for("front_page"))
    return render_template("add_book.html")

@app.route("/edit", methods=["POST"])
def edit_book():
    book_id = request.form["id"]
    with Session() as session:
        book = session.query(Book).filter_by(id=book_id).first()
        if request.form.get("new_rating"):
            book.rating = request.form["new_rating"]
            session.commit()
            return redirect(url_for("front_page"))
        return render_template("editing.html", book=book)
@app.route("/delete", methods=['POST'])
def deleting():
    book_id_to_del = request.form['haha']
    with Session() as session:
        book_to_del=session.query(Book).filter_by(id=book_id_to_del).first()
        session.delete(book_to_del)
        session.commit()
    return redirect(url_for("front_page"))
if __name__ == "__main__":
    app.run(debug=True)

