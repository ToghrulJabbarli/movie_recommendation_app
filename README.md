# movie_recommendation_app
Movie Recommender App based on given dataset.
PyQt5 library is used to create User Interface.
Based on director and genre of selected movie, app recommend 19 similar movies.
Recommender system is working on Content-Based Filtering system logic. Recommendation are given with the help of selected movies content.
To be able to implement the logic behind the system, I converted the sentences to vector and used cosine similarity method find similarities among them.
App interface is below:
![image](https://user-images.githubusercontent.com/56371622/211931373-45e2e284-b218-4d52-a1b9-ddbe4ed84387.png)
When you click the "Recommend Movies" button, app return messageboc with result set as below:

![image](https://user-images.githubusercontent.com/56371622/211932076-dafff429-1079-4e7b-90e2-d778dfdb7353.png)

When you click "Show Cosine Similarities" button scatter plot of vector is shown.
![image](https://user-images.githubusercontent.com/56371622/211932563-9c240e07-c5f1-47af-83f0-11e4352dd1cf.png)
