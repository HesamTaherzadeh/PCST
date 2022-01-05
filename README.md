# PCST
Photogrammetric Coordinate System Transformer, in short PCST, is a python based GUI program, that intends to help photogrammetrist and computer vision analyst, rapidly pick the best model and it's parameter on their data

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

