""" chart_gen.py

Created by 
    name: Callum Johnson
    mail: callum.johnson.aafc@gmail.com

This is a tool created for generating elevate graduation pack visualisations.
When run, the tool will ask for a set of initial score results, followed by
the set of post diagnostic results.
Upon providing these, two rose charts with score scales will be generated
(one for pre and one for post) as well as a column diagram detailing the
% changes for this student. These images will be saved to the source file
location.

"""

import numpy as np
import matplotlib.pyplot as plt