=====
About
=====

A Smart Library System Built for Raspberry Pi. The system can be used to facilitate everyday operations of a library.
For the system to work, two Raspberry Pi's are required with one being the Master Pi and the other being the Reception Pi.

The Reception Pi handles user registration and user login, while the Master Pi handles main functions,
such as Search, Borrow, and Return a book.

To login to the system, the user can either choose to manually type in the credentials ro to use
facial recognition provided they have had their faces scanned beforehand.

Once logged in, the user can search for books to borrow. The user can either type in the search query
or use the voice recognition to search. When returning a borrowed book, the user can choose to manually
enter the book ID or scan the QR code of the book.

For library admin, the system also provides a web app that allows the admin to add new books and to delete
books. Besides, the admin can also view the borrow & return statistics for a specific time period.