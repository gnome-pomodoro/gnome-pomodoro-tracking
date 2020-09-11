# Build a plugin

Create a folder in `plugins`
```bash
 mkdir -p ./plugins/clockify
```

Create a file `python` 

```bash
touch ./plugins/clockify/clockify.py
```

Create a `class` using the following template

```python

class Clockify:
    
    # Es usado para crear una seccion en el archivo ~./gp-tracking.conf
    GTP_CONFIG = "clockify"
    
    def __init__(self, gptracking):
        self.gptracking = gptracking

    
    def add_time_entry(self, **kwargs):
        """ 
        Method used to register a time entry with the provider
        params:
            description: Description activity
            start: datetime in UTC format %Y-%m-%dT%H:%M:%SZ
            end: datetime in UTC format %Y-%m-%dT%H:%M:%SZ
            minutes: elapsed
        return: True or False
        """
        raise NotImplementedError
 
    def gptparse_args(self, **kwargs):
        """ 
        Method to add optional arguments in command terminal
        params: None
        return: None
        
        e.g
        
        self.gptracking.parse.add_argument('--clockify-workspaces', 
            action='store_const', 
            dest='clockify_workspaces', 
            help='List clockify workspaces',     
            const=True,                
        )
        """
        raise NotImplementedError

    def cli(self):
        """
        Method that interprets command line arguments
        params: None
        return: None

        e.g 

        params = self.gptracking.gptparse_params()
        if params.clockify_workspaces:
            pass
        """
        raise NotImplementedError

    def state(self, **kwargs):
        """
        Method to print the current state of the Pomodoro on the command line
        params: None
        return: None

        e.g 

        _name = self.gptracking.gptconfig_get(self.GTP_CONFIG, "clockify_name")
        self.gptracking.print_cli([{'name': _name }])
        """
        raise NotImplementedError


```


Thanks for contributing