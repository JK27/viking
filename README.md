# VIKING GYM

This is the website for Viking Gym, where users can choose a membership to join the gym giving them access to all the fitness facilities and classes. The personal details the user uses during the sign up process will be save to their user profile where can be reviewed and edited, alongside a summary of their membership subscription and any orders they may have done from the shop.

Users can also purcchase products from a catalogue of fitness clothing and accessories. The selected items are stored in a shopping bag until the user checks out purchasing the items and placing an order for them, or until the browser session is closed.

## UX

![Responsive views](/media/responsive.png)

The website is focused to those looking to either join the gym or wanting to purchase any of the products listed on the shop.

### User stories

* A user that wants to join the gym wants to see what different membership options are available for them, before making the decission of signing up or not.

* A user wants to look around the shop and search for the products they want in order to compare different options of the item they are looking for, especially how the product looks like and its description.

* A member wants to store their personal details so they are available as default for future orders from the shop. 

* A member wants to review their membership to double check what is included and the date they joined in to keep track on when the next payment will be.

* A member wants to check what items they have purchased from the shop in previous orders and have a summary of all of them.

## Features

### *Existing feature*

### Signing up

1. Users that are looking for joining the gym but they are not sure of what type of membership is better for them and what the prices are, can can check them out before signing up, viewing all the available memberships at the start of the process and even filtering by one of the three categories available depending on their needs. Before choosing their desire membership, they can view more in detail all what is included in each one of them so they can compare them to make sure they select the one that fits better to their needs.

2. Once they have selected their desire membership, first they user will give the email address they want to use, create an username and password that they will need for logging in to the system in future visits to the website in order to access to their user profile.

5. Gym members can store their personal details in their user profile, which is link to their membership subscription. This saved details are the default for when purchasing items in the shop and will automatically fill the corresponding fields in the checkout form. These details can be updated from the profile page.

6. Members can also review the details of their membership subscription directly from the profile profile page. They can also check what orders they have done in the past also from their profile page.

### Shop

1. A user, authenticated or not, can peruse the different products available at the shop. They can search for items using the search bar, filter their search selecting any of the categories and subcategories narrowing down the options to those they are looking for, and also sort the items by category, price, product name or brand name. 

2. Users can view more details of the desire item by clicking on the prodcut image or on the details button shown below the image only for the products that require the selection of a size before the purchase.

3. Once the user has chosen their desire size, when applicable, and number of items wanted, they can add then to the shopping bag. After doing so, they can either go back to the shop to look for other products, or review the items they have in their shopping bag before procceding to the checkout page. User can update the number of items or remove the items completely directly from the shopping bag.

4. If they user is happy with the items in their bag, they can finish the purchase filling up the checkout form, inclusive of some personal details to be included in the order and the credit or debit card they want to use for the payment. Once the payment is accepted, they can see a summary of their order. At this same time, an email is sent to the email address provided.

### Logging in

1. Members that have finished the sign up process can log in from the home page using either their email address or username selected during the registration and their password. If they have forgotten the password, they can reset this by clicking the link on the log in page.

2. After a successful log in, the user is redirected to their profile page, where they can review their personal details, their membership subscription and any previous orders from the shop, if any. 

3. The member can update their personal details directly from the link on the profile page, which will display a form pre-filled with their current information.

### *Features planned to be implemented*

* In order to improve the quality of the service provided to all members, it is intended to implement a booking system for all the classes available at the gym so members can do this directly from the website.

* Another feature will be the addition of more filtering and sorting options for the products in the shop such as being able to search for products of a specific brand, colour or gender. All of this linked to the inclusion of a wider range of items and categories to the shop.

* An info page where users will be able to see images and videos of the facilities and have more details of what it is on offer for them.

## Technologies used

* HTML for the structure of the project and its different applications.
* CSS for styling
* Python 3 for build control and management of applications (https://www.python.org/)
* Django framework for app construction, user authentication and content administration (https://www.djangoproject.com/)
* jQuery JavaScript library for event handling and animations (https://jquery.com/)
* Bootstrap 4 framework for responsiveness and structure of the application (https://getbootstrap.com/)
* Git for version control (https://git-scm.com/)
* GitHub for hosting the repository (https://github.com/)
* Heroku app for deployment (https://www.heroku.com/)
* Stripe for payment processing (https://stripe.com/)
* Font Awesome for all icons in the project (https://fontawesome.com/)
* Werkzeug Web Server Gateway Interface for debugging and structured error logs.

## Testing

All functionalities of the application have been regularly tested during the building process, after each function was written, and after adding every piece of code, this was tested again on the browser using Google Chrome Developer tools and Werkzeug Web Server Gateway Interface for debugging.

The application has also been regularly tested on different browsers (Google Chrome, Mozilla Firefox and Internet Explorer/Microsoft Edge) and also on different devices (computer, laptop and mobile phones).


## Deployment

The application is hosted as an app in Heroku, sourced via GitHub repository. It can be seen using the following link on the web browser of your preference: https://viking-gym.herokuapp.com/

The deployment process was as follows:

- Host a git repository on GitHub
- Create an app in Heroku
- On the app settings in Heroku, connect the app to the GitHub repository and enable the automatic deploys from the chosen branch so all commits pushed to GitHub will automatically feed through to the Heroku app.
- Once everything is connected to the app, use the domain URL given or click on the "Open app" button to see the app on the browser.

## Credits

The main structure of the website has been built following the video lessons of the Boutique Ado e-commerce project from the Code Institue hosted in (https://github.com/ckz8780/boutique_ado_v1)

The home page design is inspired on the carousel example on Boostrap's own website (https://getbootstrap.com/docs/4.5/examples/carousel/)

The images used in the carousel were downloaded from https://www.pexels.com/ using images from users Lukas and Pixabay.

The shop database, including product images and descriptions it's a reduced version of the Fashion Product Image Dataset uploaded by Param Aggarwal (https://www.kaggle.com/paramaggarwal/fashion-product-images-dataset)

In addition to thanking Lukas, Pixabay and Param Aggarwal for their contributions to the project, I would like to take the opportunity to thank my mentor Seun Owonikoko and the team of tutors at the Code Institute for their inspiration, support and patience provided to help put this project together.

