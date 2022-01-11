# PCST

![PCST-01-01](https://user-images.githubusercontent.com/89359094/149028740-a69c9d8b-ffa8-41ec-b856-42e60ab04983.jpg)
Designer: Kimya

This desktop app provides following features:
- Showing a relative map of your image and ground coordinates
- Clustering your data with K-means, this way you can easily pickout ICPS from your clusters
- Linear Conformal Transformation
- Affine Transformation
- Global Polynomial Transformation
- Multi Quadric Adjustment on GP
- Pointwise Adjustment on GP (You can pickout the number of effective points and the way of choosing them (Picking the nearest or dividing the whole map into four quadrants with the target point as its center and picking from each quadrant) and averaging methods (Weighted distance and moving average)
- Direct linear Transformation (beta)
- Showing the residual vector map, RMSE and MAE

Below you can see some parts of the app's interface, which is simple and the work is mostly focused on the alghorithms

![Screenshot (552)](https://user-images.githubusercontent.com/89359094/149015274-76d63c6a-df50-46b5-bc6b-9c959d9e0d30.png)
                              <p align="center">
   figure1 - apps main interface
</p>

![Screenshot (555)](https://user-images.githubusercontent.com/89359094/149019687-726bb4ea-c5af-49ab-9986-bea4c06fcef8.png)
                              <p align="center">
   figure2 - The maps
</p>

![Screenshot (556)](https://user-images.githubusercontent.com/89359094/149020177-c0afab50-9cbe-4bdd-9052-9a846b885a2f.png)
                             <p align="center">
   figure3 - Residual vector map
</p>




# Some primitive photogrammetric definitions:

**Ground Control Points** 
- Ground control points (GCPs) are places on the ground that have a precise known location associated with them. In photogrammetry, they are used to tie the map down to the Earth—matching the drone location data to the location data measured terrestrially.

**Independent check points**
- Independent check points(ICPs) are used to assess the absolute accuracy of the model. The marks of the checkpoints are used to estimate its 3D position as well as potential errors in the clicks. This way, the relative accuracy of the area of the checkpoints may improve.

# Linear conformal
The simplest 2D mathematical model in analytical photogrammetry is 2D linear conformal or 2D similarity transformation:
This transformation has 4 parameters: 
- 1 scale
- 1 rotation 
- 2 translations 

# Affine Transformation
Slightly more complex than conformal and a popular and widespread 2d transformation model, this model has 6 parameters:
- 2 scales 
- 1 skewity(non-orthogonality) parameter
- 1 rotation
- 2 translation

# Global polynomial
In practice, global polynomial transformations are used widely for rectification purpose, especially where high positional accuracies are not required, e.g. in thematic mapping and in projects where the interpretation of the ground features is the main matter of interest.
Global polynomial interpolation fits a smooth surface that is defined by a mathematical function (a polynomial) to the input sample points. The global polynomial surface changes gradually and captures coarse-scale pattern in the data.
Conceptually, global polynomial interpolation is like taking a piece of paper and fitting it between the raised points (raised to the height of value), the number of bendings in papers would be the order of the model.(Credit: prof. mohammadjavad Valadanzoj's pamphlet on 2d models)

The parameters in this model, depend on the chosen degree , as for n-degree global polynomial would have n+1 parameters, that would appear as the coefficents

# Multiquadric
in order use this feature, you first need to fit a global polynomial on your data and then you can use this adjustment

# Pointwise
in order use this feature, you first need to fit a global polynomial on your data and then you can use this adjustment,
in this part you have to enter three important parameter
- Number of effective points 
- Method of choosing effective points
- averaging method

Check these links to further expand your knowledge

<a href='https://encyclopediaofmath.org/wiki/Distance-weighted_mean'> Weighted distance average </a>

<a href='https://en.wikipedia.org/wiki/Moving_average'>Moving average </a>

Method of choosing the points:

![Screenshot (554)](https://user-images.githubusercontent.com/89359094/149018826-800ecac8-49e0-4e2a-ad22-43302850e986.png)

The image is courtesy of prof. Valadanzoj's pamphlet on 2d transformations



