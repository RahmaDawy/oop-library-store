# 🛒 OOP-Based Online Store in Python

This is a Python project built with Object-Oriented Programming (OOP) concepts that simulates an online bookstore for **Books**, **Magazines**, and **DVDs**.

It includes user registration, secure password validation, item search (by title, author, director, or genre), and cart management with checkout functionality.

---

## 🚀 Features

✅ Abstract base class `Item` using `abc`  
✅ Subclasses: `Book`, `Magazine`, `DVD`  
✅ User class with a secure cart system  
✅ Multiple dispatch using `multipledispatch`  
✅ Password validation using rules (length, case, digits, symbols)  
✅ Inventory system with search by:
- Title
- Author (for books & magazines)
- Genre (for books & DVDs)
- Director (for DVDs)  

✅ Checkout & stock update after purchase

---

## 🧰 Technologies Used

- Python 3.8+
- `multipledispatch`
- Standard libraries: `abc`, `string`

---

## 📦 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/oop-library-store.git
   cd oop-library-store
