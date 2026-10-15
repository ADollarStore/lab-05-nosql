//Step 2:
//use bookstore
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

//step 5: list authors and books
db.authors.find()
db.books.find()

//step 6: insert 2 books
db.books.insertOne({title: "Cry the Beloved Country", published_year: 1948, author_ids: ["author_004"]}) 
db.books.insertOne({title: "The Color Purple", published_year: 1982, author_ids: ["author_005"]})

//step 7: add missing authors
db.authors.insertOne(
{_id:'author_004', 
name:'Alan Paton', 
nationality:'South African', 
bio:{
short:'South African author known for Cry the Beloved Country', 
long:'Alan Paton was a South African novelist known for his political and social commentary in works such as Cry the Beloved Country'
}
}
)
db.authors.insertOne(
{_id:'author_005', 
name:'Alice Walker', 
nationality:'American', 
bio: {
short:'American novelist known for works during the civil rights era', 
long: 'Alice Walker is an American novelist, short story writer, poet, and social activist. In 1982, she became the first African-American woman to win the Pulitzer Prize for Fiction, which she was awarded for her novel The Color Purple.'
}
}
)

//step 8: filter books by a list of authors
db.books.find({ author_ids: { $in: ["author_001", "author_004"] } })
