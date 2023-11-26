import argparse

from datetime import datetime
from mongoengine import DoesNotExist

from models_odm import Author, Quote, connect

row_format = "%B %d, %Y"

parser = argparse.ArgumentParser(description="Quotes of great people")
parser.add_argument("--action",
                    help="create_author, read_author, update_author, delete_author, create_quote, read_quote, \
                    update_quote, delete_quote")  # CRUD action
parser.add_argument("--id")
parser.add_argument("--fullname")
parser.add_argument("--born_date")
parser.add_argument("--born_location")
parser.add_argument("--description")
parser.add_argument("--author")
parser.add_argument("--quote")
parser.add_argument("--tags", nargs="+")

arg = vars(parser.parse_args())

action = arg.get("action")
pk = arg.get("id")
fullname = arg.get("fullname")
born_date = arg.get("born_date")
born_location = arg.get("born_location")
description = arg.get("description")
author = arg.get("author")
quote = arg.get("quote")
tags = arg.get("tags")


def create_author(fullname, born_date, born_location, description):
    print('Input date in format "March 01, 2000"')
    date = datetime.strptime(born_date, row_format).date()
    author = Author(fullname=fullname, born_date=date, born_location=born_location, description=description)
    author.save()
    return author


def read_author():
    return Author.objects.all()


def update_author(pk, fullname, born_date, born_location, description):
    author = Author.objects(id=pk).first()
    if author:
        author.update(fullname=fullname, born_date=born_date, born_location=born_location, description=description)
        author.reload()
    return author


def delete_author(pk):
    try:
        author = Author.objects.get(id=pk)
        author.delete()
        return author
    except DoesNotExist:
        return None


def create_quote(tags, author, quote):
    author_quote = Author.objects(fullname=author).first()
    if author_quote:
        quote = Quote(tags=tags, author=author_quote, quote=quote)
        quote.save()
        return quote
    else:
        return f'There is no such author in our database yet.\n First, add information about the author to the database.'


def read_quote():
    return Quote.objects.all()


def update_quote(pk, tags, quote):  # будемо оновлювати цитату, тому автора не будемо чіпати
    quote_update = Quote.objects(id=pk).first()
    if quote_update:
        quote.update(tags=tags, quote=quote)
        quote.reload()
    return quote


def delete_quote(pk):
    try:
        quote = Quote.objects.get(id=pk)
        quote.delete()
        return quote
    except DoesNotExist:
        return None


def main():
    match action:
        case "create_author":
            r = create_author(fullname, born_date, born_location, description)
            print(r.to_mongo().to_dict())
        case "read_author":
            r = read_author()
            print([e.to_mongo().to_dict() for e in r])
        case "update_author":
            r = update_author(pk, fullname, born_date, born_location, description)
            if r:
                print(r.to_mongo().to_dict())
        case "delete_author":
            r = delete_author(pk)
            if r:
                print(r.to_mongo().to_dict())
        case "create_quote":
            r = create_quote(tags, author, quote)
            print(r.to_mongo().to_dict())
        case "read_quote":
            r = read_quote()
            print([e.to_mongo().to_dict() for e in r])
        case "update_quote":
            r = update_quote(pk, tags, quote)
            if r:
                print(r.to_mongo().to_dict())
        case "delete_quote":
            r = delete_quote(pk)
            if r:
                print(r.to_mongo().to_dict())
        case _:
            print("Unknown command")


if __name__ == '__main__':
    main()
