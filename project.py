from abc import ABC, abstractmethod
from string import ascii_letters, digits, punctuation
from multipledispatch import dispatch

class Item(ABC):
    def __init__(self, title, author, price, stock):
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock

    @abstractmethod
    def get_detail(self):
        pass

    def update_detail(self, title, author, price):
        self.title = title
        self.author = author
        while True:
            try:
                self.price = float(price)
                break
            except (ValueError, OverflowError):
                print("ERROR: Invalid price.")
                price = input("Please enter a valid price: ")

class Book(Item):
    def __init__(self, title, author, price, ISBN, genre, numberofpages, stock):
        super().__init__(title, author, price, stock)
        self.ISBN = ISBN
        self.genre = genre
        self.numberofpages = numberofpages

    def get_detail(self):
        return f"Book title: {self.title} | Book author: {self.author} | Book price: {self.price} EGP\n" \
               f"ISBN: {self.ISBN} | Genre: {self.genre} | Number of pages: {self.numberofpages}"

class Magazine(Item):
    def __init__(self, title, author, price, issue_number, publication_date, editor, stock):
        super().__init__(title, author, price, stock)
        self.issue_number = issue_number
        self.publication_date = publication_date
        self.editor = editor

    def get_detail(self):
        return f"Magazine title: {self.title} | Magazine author: {self.author} | Magazine price: {self.price} EGP\n" \
               f"Issue number: {self.issue_number} | Publication date: {self.publication_date} | Editor: {self.editor}"

class DVD(Item):
    def __init__(self, title, price, director, duration, genre, stock):
        super().__init__(title, '', price, stock)
        self.director = director
        self.duration = duration
        self.genre = genre

    def get_detail(self):
        return f"DVD title: {self.title}| DVD director: {self.director} | DVD price: {self.price} EGP\n" \
               f"Duration: {self.duration} | Genre: {self.genre}"

class Cart:
    def __init__(self):
        self.items = []

    def add_to_cart(self, item):
        if item.stock > 0:
            self.items.append(item)
            item.stock -= 1
        else:
            print(item.title, "is out of stock")

    def remove_from_cart(self, item):
        self.items.remove(item)
        item.stock += 1
        print(item.title, "removed from cart")

    def view_cart(self):
        if not self.items:
            print("Your cart is empty.")
        else:
            print(">>Your Items: ")
            print("**" * 20)
            for item in self.items:
                print(item.get_detail())
                print("************")

class User:
    def __init__(self, name, email,password):
        self.__name = name
        self.__email = email
        self.__password = password
        self.cart = Cart()
    
    def get_detail(self):
        print(f"User: {self.__name} | Email: {self.__email} | Password: ********")
    
    @dispatch(Book)
    def add_to_cart(self, item):
        self.cart.add_to_cart(item)
        return self
    @dispatch(Magazine)
    def add_to_cart(self, item):
        self.cart.add_to_cart(item)
        return self
    @dispatch(DVD)
    def add_to_cart(self, item):
        self.cart.add_to_cart(item)
        return self
    def remove_from_cart(self, item):
        self.cart.remove_from_cart(item)

    def view_cart(self):
        self.cart.view_cart()

    def check_out(self):
        if not self.cart.items:
            print("Nothing to check out.")
        else:
            total_price = sum(item.price for item in self.cart.items)
            print("Total price:", total_price, "EGP")
            for item in self.cart.items:
                item.stock -= 1
            self.cart.items = []

class Inventory:
    def __init__(self):
        self.book_inventory = []
        self.magazine_inventory = []
        self.dvd_inventory = []

    def add_to_bookinventory(self, item):
        self.book_inventory.append(item)

    def add_to_magazineinventory(self, item):
        self.magazine_inventory.append(item)

    def add_to_dvdinventory(self, item):
        self.dvd_inventory.append(item)

    def remove_from_inventory(self, item):
        removed = False
        for inventory in [self.book_inventory, self.magazine_inventory, self.dvd_inventory]:
            if item in inventory:
                inventory.remove(item)
                removed = True
                break
        if not removed:
            raise Exception("Item not found in inventory")

    def search_by_title(self, title):
        found_items = []
        for inventory in [self.book_inventory, self.magazine_inventory, self.dvd_inventory]:
            for item in inventory:
                if item.title.lower() == title.lower():
                    found_items.append(item)
        return found_items

    def search_by_author(self, author):
        found_items = []
        for inventory in [self.book_inventory, self.magazine_inventory]:
            for item in inventory:
                if isinstance(item, (Book, Magazine)) and item.author.lower() == author.lower():
                    found_items.append(item)
        return found_items
    
    def search_by_director(self, director):
        found_items = []
        for item in self.dvd_inventory:
            if isinstance(item, DVD) and item.director.lower() == director.lower():
                found_items.append(item)
        return found_items

    def search_by_genre(self, genre):
        found_items = []
        for inventory in [self.book_inventory, self.dvd_inventory]:
            for item in inventory:
                if isinstance(item, Book) and item.genre.lower() == genre.lower():
                    found_items.append(item)
                elif isinstance(item, DVD) and item.genre.lower() == genre.lower():
                    found_items.append(item)
        return found_items

    def view_inventory(self, book_item, magazine_item, dvd_item):
        while True:
            lib = input("Do you want to view our inventory? (yes/no): ").lower()
            if lib == "no":
                break
            elif lib not in ["yes", "no"]:
                print("Invalid input. Please enter (yes/no).")
                continue
            elif lib == "yes":
                print("==" * 20)
                print("\t\tThe Books available: ")
                for book_item in self.book_inventory:
                    print(">>", book_item.title)
                print("==" * 20)
                print("\t\tThe Magazines available: ")
                for magazine_item in self.magazine_inventory:
                    print(">>", magazine_item.title)
                print("==" * 20)
                print("\t\tThe DVDs available: ")
                for dvd_item in self.dvd_inventory:
                    print(">>", dvd_item.title)
                print("==" * 20)
                break

'''Functions that are used in the main function section'''
def add_to_cart(user, inventory, item_type):
    item_inventory = {
        "book": inventory.book_inventory,
        "magazine": inventory.magazine_inventory,
        "dvd": inventory.dvd_inventory
    }
    search_title = input("Enter the title of the item you want to add to cart: ")
    for item in item_inventory[item_type]:
        if item.title.lower() == search_title.lower():
            if item.stock > 0:
                user.add_to_cart(item)
                print(item.title, "added to cart successfully.")
                break
            elif item.stock == 0:
                print(item.title, "is out of stock.")
    else:
        print("Item not found.")

def validate_password(password):
    # Minimum length of the password
    if len(password) < 8:
        return False
    # At least one uppercase letter
    if not any(char.isupper() for char in password):
        return False
    # At least one lowercase letter
    if not any(char.islower() for char in password):
        return False
    # At least one digit
    if not any(char.isdigit() for char in password):
        return False
    # At least one special character
    if not any(char in punctuation for char in password):
        return False
    return True

def get_valid_password():
    while True:
        password = input("Enter your password (at least 8 characters with at least one uppercase letter, one lowercase letter, one digit, and one special character): ")
        if validate_password(password):
            confirm_password = input("Confirm your password: ")
            if password == confirm_password:
                return password
            else:
                print("Passwords do not match. Please try again.")
        else:
            print("Password does not meet the requirements. Please try again.")
def main():
    try:
        inventory = Inventory()
        books = [
            Book("To Kill a Mockingbird", "Harper Lee", 157.30, "978-0061120084", "Fiction", 336, 10),
            Book("The Great Gatsby", "F. Scott Fitzgerald", 188.80, "978-0743273565", "Classic", 180, 2),
            Book("Pride and Prejudice", "Jane Austen", 157.30, "978-0141439518", "Romance", 416, 4),
            Book("The Hobbit", "J.R.R. Tolkien", 173.10, "978-0345534835", "Fantasy", 332, 6),
            Book("1984", "George Orwell", 120.50, "978-0451524935", "Dystopian", 328, 100),
            Book("The Catcher in the Rye", "J.D. Salinger", 99.99, "978-0316769488", "Fiction", 224, 5),
            Book("Harry Potter and the Philosopher's Stone", "J.K. Rowling", 150.25, "978-0747532743",
                 "Fantasy", 336, 22),
            Book("The Lord of the Rings", "J.R.R. Tolkien", 180.75, "978-0618645619", "Fantasy", 1178, 100),
            Book("The Chronicles of Narnia: The Lion, the Witch and the Wardrobe", "C.S. Lewis", 85.00,
                 "978-0064404990", "Fantasy", 208, 33),
            Book("Moby-Dick", "Herman Melville", 180.20, "978-0553213119", "Adventure", 624, 1)
        ]
        for book in books:
            inventory.add_to_bookinventory(book)

        magazines = [
            Magazine("National Geographic", "National Geographic Society", 78.50, 123, "April 2024", "John Doe", 2),
            Magazine("Time Magazine", "Time Magazine Editors", 62.90, 456, "April 2024", "Jane Smith", 100),
            Magazine("Vogue", "Vogue Editors", 94.40, 789, "April 2024", "Alice Johnson", 10),
            Magazine("The New Yorker", "The New Yorker Staff Writers", 110.00, 1011, "April 2024", "Michael Brown",
                     3),
            Magazine("Forbes", "Forbes Contributors", 55.00, 567, "April 2024", "William Smith", 5),
            Magazine("Scientific American", "Scientific American Editors", 50.00, 345, "April 2024", "Emily Johnson",
                     100)
        ]
        for magazine in magazines:
            inventory.add_to_magazineinventory(magazine)

        dvds = [
            DVD("Inception", 244.70, "Christopher Nolan", "2h 28min", "Science Fiction", 1000),
            DVD("Schindler's List", 157.30, "Steven Spielberg", "3h 15min", "Drama", 1000),
            DVD("The Godfather", 196.70, "Francis Ford Coppola", "2h 55min", "Crime", 1000),
            DVD("Forrest Gump", 149.00, "Robert Zemeckis", "2h 22min", "Drama", 2),
            DVD("Arrival", 200.80, "Denis Villeneuve", "1h 56min", "Science Fiction", 10010),
            DVD("The Shawshank Redemption", 200.00, "Frank Darabont", "2h 22min", "Drama", 19),
            DVD("The Dark Knight", 189.50, "Christopher Nolan", "2h 32min", "Action", 20),
            DVD("The Matrix", 99.99, "The Wachowskis", "2h 16min", "Action", 4),
            DVD("Interstellar", 179.75, "Christopher Nolan", "2h 49min", "Science Fiction", 100)
        ]
        for dvd in dvds:
            inventory.add_to_dvdinventory(dvd)
        '''Starting of the program(will start from here asking the user to interact with the program)'''
        print("**********************************************************************************************")
        print("\t\t\tWelcome to my online bookstore!")
        print("Let's create your account.")
        name = input("Enter your name: ")
        
        while True:
            email = input("Enter your email: ")
            if "@gmail.com" in email:
                break
            else:
                print("Invalid email. Please enter a valid Gmail.")
        password=get_valid_password()
        user = User(name, email, password)
        print("Your account has been created successfully.\n")
        print("****************************************************************************************\n")
        print("Your account details are : ")
        user.get_detail()
        print("****************************************************************************************\n")

        inventory.view_inventory(books, magazines, dvds)

        print(" \t\t\tWelcome to our online store ", name.title(), "!")
        z = input("Want to search for items in our store? (yes/no): ")
        while True:
            if z.lower() == "no":
                break
            elif z.lower() not in ["yes", "no"]:
                print("Invalid input. Please enter(yes/no).")
                z = input("Want to search for items in our store? (yes/no): ")
                continue
            elif z.lower() == "yes":
                while True:
                    print("Choose the search type:")
                    print("Enter (1) for Title")
                    print("Enter (2) for Author (for books and magazines)")
                    print("Enter (3) for Genre (for books and DVDs)")
                    print("Enter (4) for Director (for DVDs)")
                    print("Enter 'Done' to exit")
                    search_choice = input("Enter your choice: ")
                    if search_choice == "1":
                        search_title = input("Enter title: ")
                        found_items = inventory.search_by_title(search_title)
                        if found_items:
                            print("The following items were found:")
                            print("**"*20)
                            for item in found_items:
                                print(item.get_detail())
                                print("**"*20)
                        else:
                            print("No items found.")
                        break
                    elif search_choice == "2":
                        search_author = input("Enter author: ")
                        found_items = inventory.search_by_author(search_author)
                        if found_items:
                            print("The following items were found:")
                            print("**"*20)
                            for item in found_items:
                                print(item.get_detail())
                                print("**"*20)
                        else:
                            print("No items found.")
                        break
                    elif search_choice == "3":
                        search_genre = input("Enter genre: ")
                        found_items = inventory.search_by_genre(search_genre)
                        if found_items:
                            print("The following items were found:")
                            print("**"*20)
                            for item in found_items:
                                print(item.get_detail())
                                print("**"*20)
                        else:
                            print("No items found.")
                        break
                    elif search_choice == "4":
                        search_director = input("Enter director: ")
                        found_items = inventory.search_by_director(search_director)
                        if found_items:
                            print("The following items were found:")
                            print("**"*20)
                            for item in found_items:
                                print(item.get_detail())
                                print("**"*20)
                        else:
                            print("No items found.")
                        break
                    elif search_choice.lower() == "done":
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 4.")
                z = input("Want to search for more items in our store? (yes/no): ")
                if z.lower() == "no":
                    break
                elif z.lower() not in ["yes", "no"]:
                    continue
                elif z.lower() == "yes":
                    continue
        print("\n============================================================================================")
        print("Welcome to your cart: ",name.title(),"!")
        choix = input("Would you like to add items to your cart? (yes/no): ")
        while True:
            if choix.lower() == "no":
               print("*" * 20)
               print("Items added to cart successfully.", name.title(), "!")
               break
            elif choix.lower() not in ["yes", "no"]:
               print("Invalid choice. Please try again Enter (yes/no).")
               choix = input("Would you like to add items to your cart? (yes/no):  ")
               continue
            elif choix.lower() == "yes":
               while True:
                  print("Choose the item type you want to add to your cart:")
                  print("1. Book")
                  print("2. Magazine")
                  print("3. DVD")
                  print("Enter 'Done' to finish.")
                  choice = input("Enter your choice: ")

                  if choice.lower() == "done":
                      print("-" * 20)
                      print("Items added to cart successfully.", name.title(), "!")
                      break
                  elif choice in ["1", "2", "3"]:
                      add_to_cart(user, inventory, "book" if choice == "1" else "magazine" if choice == "2" else "dvd")
                  else:
                      print("Invalid choice. Please enter a number between 1 and 3.\n")
               choix = input("Do you want to keep adding items to your cart? (yes/no):  ")
               if choix.lower()=="no":
                   print("*" * 20)
                   print("Proceeding to ckeckout.", name.title(), "!")
                   break
               elif choix.lower() not in ["yes", "no"]:
                  print("Invalid choice. Please try again Enter (yes/no).")
                  choix = input("Would you like to add items to your cart? (yes/no):  ")
                  continue
               elif choix.lower()=="yes":
                   continue
        
        while True:
            check = input("Do you want to check out? (yes/no): ").lower()
            if check == "yes":
                print("\n==========================================")
                print("Viewing your cart: ", name.title(), "!")
                user.view_cart()
                print("Thank you for shopping with us,", name.title(), "!","Your items will be delivered soon.")
                user.check_out()
                break
            elif check not in ["yes", "no"]:
                print("Invalid choice. Please try again.")
            elif check == "no":
                while True:
                    x = input("Do you want to edit your purchase? (yes/no): ").lower()
                    if x == "yes":
                        y = input("Do you want to add another item or remove an item from your cart? (add/remove): ").lower()
                        if y == "add":
                            print("Choose the type of item you want to add to your cart:")
                            print("1. Book")
                            print("2. Magazine")
                            print("3. DVD")
                            print("Enter 'Done' to finish.")
                            choice = input("Enter your choice: ")
                            if choice.lower() == "done":
                                print("Thank you for shopping with us,", name.title(), "!")
                                break
                            elif choice not in ["1", "2", "3"]:
                                print("Invalid choice. Please enter a number between 1 and 3.")
                            elif choice == "1":
                                add_to_cart(user, inventory, "book")
                            elif choice == "2":
                                add_to_cart(user, inventory, "magazine")
                            elif choice == "3":
                                add_to_cart(user, inventory, "dvd")
                        elif y == "remove":
                            user.view_cart()
                            if user.cart.items:
                                item_to_remove = input("Enter the title of the item you want to remove from the cart: ")
                                for item in user.cart.items:
                                    if item.title.lower() == item_to_remove.lower():
                                        user.remove_from_cart(item)
                                        break
                                else:
                                    print("Item not found in cart.")
                        else:
                            print("Invalid choice. Please enter (add/remove).")
                    elif x == "no":
                        print("Thank you for visiting our store . Come back soon,", name.title(), "!")
                        break
                    else:
                        print("Invalid choice. Please enter (yes/no).")
            else:
                break
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
