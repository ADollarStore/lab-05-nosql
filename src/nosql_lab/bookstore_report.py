#!/usr/bin/env python3

import os
import logging
import pymongo

#creating the logger
logger = logging.getLogger(__name__)

 # getting MONGODB login credentials from environment variables
MONGOURL = os.getenv('MONGODB_ATLAS_URL')
MONGOUSER = os.getenv('MONGODB_ATLAS_USER')
MONGOPWD = os.getenv('MONGODB_ATLAS_PWD')

def main():
    """Connect to MongoDB Atlas and print each author with their books."""
    # Stop early with a clear message if any credential is missing
    if not all([MONGOURL, MONGOUSER, MONGOPWD]):
        logger.error(
            "Set MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, and MONGODB_ATLAS_PWD "
            "in your environment."
        )
        return
 
    client = None
    try:
        # Connect to Atlas using the URL plus username and password
        client = pymongo.MongoClient(
            MONGOURL,
            username=MONGOUSER,
            password=MONGOPWD,
        )
        logger.info("Connected to MongoDB Atlas")
 
        # Select the database and collections
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]
 
        # Count how many of the authors exist in the collection
        total = authors.count_documents({"_id": {"$in": AUTHOR_IDS}})
        print(f"Authors: {total}")
 
        # Loop over the list so authors print in the order given
        for author_id in AUTHOR_IDS:
            author = authors.find_one({"_id": author_id})
            if author is None:
                logger.warning("No author found with _id %s", author_id)
                continue
 
            print()
            print(author["name"])
 
            # Querying an array field with a single value matches any element,
            # so co-authored books are found for each of their authors
            author_books = list(books.find({"author_ids": author_id}))
            if not author_books:
                print("  (no books found)")
            for book in author_books:
                print(f"  {book['title']} ({book['published_year']})")
    except Exception as e:
        logger.error("MongoDB error: %s", e)
    finally:
        # Always close the client, even if something failed
        if client is not None:
            client.close()
            logger.info("Closed MongoDB connection")
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    main()