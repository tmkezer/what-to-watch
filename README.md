# what-to-watch

In this project, we created a content-based movie recommendation system.

![Test Image 1](https://github.com/tmkezer/what-to-watch/blob/master/readme_images/movie-website-header.JPG)

The content-based system worked by comparing the movie the user entered with a number of features of the movie, such as director, actors, genre, etc. and then showing the movies that have the most similarities among the compared features. Fine tuning the system took some practice but we ultimately decided on giving double weight to 'Director' and 'Genre'.

![Test Image 2](https://github.com/tmkezer/what-to-watch/blob/master/readme_images/Movie-weights.JPG)

We used Kaggle and OMDB for data, and used Python, Pandas, machine learning with Scikit-learn, HTML5, JavaScript, CSS, a little D3.js, and jQuery.

Once we had built a usable CSV as input for our system, we then had to intialize the python portion as a Flask app.

![Test Image 3](https://github.com/tmkezer/what-to-watch/blob/master/readme_images/flask-app.JPG)

You can visit and try out our content-based recommendation system at: https://ucb-what-to-watch.herokuapp.com/
