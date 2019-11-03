This is a project for [HackRPI 2019](hackrpi.com)

## Inspiration
The hill RPI sits on is geologically unique. Bedrock is very close to the surface, which means that when it rains, water stays close to the surface and can cause flooding. In fact, this exact thing happened right before classes started this year and tore out plenty of infrastructure on campus.

![Flood-2](https://scontent-lga3-1.xx.fbcdn.net/v/t1.0-9/69574858_2442637009346580_92520613532401664_o.jpg?_nc_cat=108&_nc_oc=AQl0DG21HQeXYDHVUxNiH3eQVwhxDO0eah01uAvRdcP3qCr0CP9AR1Gz4TNUpcPxzTc&_nc_ht=scontent-lga3-1.xx&oh=38a9768a25e8f9632e39590fcdca258b&oe=5E5C74CD)

I wanted to find a way to programmatically identify places on campus where flooding would be an issue during other precipitation events. This will become an even greater issue in the future as climate change results in stronger storms.

Also, fun fact, the rocks exposed on the hill near DCC are over 100 million years old!!

## What it does
Typically, a homeowner has to pay their local municipality or insurance adjuster to determine if their home is in a hazardous flood area. Waterspout calculates upslope contributing area, an important dataset for calculating flood risk, using public elevation models and open-source GIS utilities. After clicking on their home in a Google Maps window, homeowners can quickly see how much precipitation will flow to their home during a precipitation event.

## How I built it
Waterspout uses a 1-meter resolution digital elevation model (DEM) from the [New York state GIS Clearinghouse](https://gis.ny.gov/elevation/) centered on Troy, NY. A mosaic of several DEMs was stitched together and preprocessed with the sink-filling algorithm of Wang and Liu. A pour point is identified from a form in the application, and a contributing area raster is generated using Freeman's distributed flow algorithm. This raster is passed to a classifier that identifies all cells which contribute a meaningful amount of their flow to produce a raster of contributing/noncontributing cells. A polygon is delineated from contributing points, simplified, and then reprojected from the NY stateplane coordiante system into latitude/longitude for display in the Maps window.

## Challenges I ran into
My initial plan was to represent contributing area as an image. However, dynamically hosting an image every time the API was called proved difficult. This led me to represent contributing area as a polygon.

Another issue was building an interface for Python to communicate with SAGA GIS. SAGA is built in C and is a nearly 20 year-old piece of software. Calling specific modules on the command line was often temperamental and required a lot of digging through SAGA's documentation. There were many moments where I thought I wouldn't finish because a certain DLL wasn't installed right or my Python environment was out of wack.

## Accomplishments that I'm proud of
I'm really proud of completing this project entirely on my own. I had never used JS or the Maps API before this hackathon and I'm very happy with the result. Being able to make a project about RPI that combines my passion for conservation and CS is also very rewarding!

## What I learned
I learned how GIS utilities can do more than just local analysis and that mapping APIs make for useful visualizations. I also learned how JS, Python, and HTML can get along together in a Flask environment. On the hydrology side of things, I have a much better understanding of how flow algorithms work after trying out several for this project.

## What's next for Waterspout
Upslope contributing area is a strong first step for determining flood risk, but there's a lot more analysis that can be done. Weighting contributing area by elevation above the pour point is a good measure of flow energy, local slope is positively correlated with flow power, etc. For refining the initial DEM, there's a lot more that can be done with permability and drainage features datasets.