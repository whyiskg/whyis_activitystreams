# Whyis Activitystreams Plugin Repo


# Approach for creating a package for Whyis
## Creating a project configuration
To configure the project for publishing to PyPi, create a `pyproject.toml` file. The file should have `setup-tools` required by the build system.
```
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"
```

The project itself should be given a name and other descriptive metadata. Additionally, `whyis` should be added as a dependency.
```
[project]
name='whyis-activitystreams'
version='0.0.4'
description = "A whyis plugin to support the interpretation of activity streams."
dependencies=[
  'whyis',
]
```

The packages to be exported should be specified as tools.
```
[tool.setuptools]
packages=['whyis_activitystreams', 'whyis_activitystreams.activity_agent']
```

The entry points for these packages should also be specified.
```
[project.entry-points.whyis]
whyis_activitystreams = "whyis_activitystreams:ActivityStreamsPlugin"
whyis_activity_agent = "whyis_activitystreams.activity_agent:ActivityAgent"
```

## Initialization
When creating a plugin, a directory should be created with the same name as the package specified in `tool.setuptools`, where names seperated by a period correspond to subdirectories. Within the plugin direction, a python file should be created that contains the main class of the plugin. This class should inherit from the Whyis Plugin class.
```{python}
# plugin.py
from whyis.plugin import Plugin

class ActivityStreamsPlugin(Plugin) :
```

The directory should also contain an initialization file `__init__.py` that specified what content will be imported.
```
from .plugin import *
from .activity_agent import *
```
Note that package subdirectories should also contain their own `__init__.py` file.

## Creating an agent
When creating an agent as an importable package, a python file with the class of that agent and its functionality should be created. That file should import the required packages from Whyis. `rdflib` is typically imported as well to work when working with RDF resources.
```
from whyis.autonomic import UpdateChangeService
from whyis.namespace import NS

from whyis.plugin import Plugin
from flask import current_app

import rdflib
```

The class for the agent is typically defined as either an `UpdateChangeService` or a `GlobalChangeService`. An activity class should be specified as well as a query that triggers the agent.
```
class ActivityAgent(UpdateChangeService):
    activity_class = NS.whyis.ActivityResolving # resolving activities
    
    def get_query(self):
        return '''select distinct ?resource where {
            ?resource rdf:type [ rdfs:subClassOf*  <https://www.w3.org/ns/activitystreams#Object> ] .
        }'''
```

