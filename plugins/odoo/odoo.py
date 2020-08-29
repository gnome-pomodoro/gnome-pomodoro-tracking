import xmlrpc.client
from urllib.parse import urlparse
import configparser
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Odoo:

    GTP_CONFIG = "odoo"
    
    def __init__(self, gptracking):
        self.gptracking = gptracking
        self.uid = None
        self.setup_config()
    
    # Odoo operations 
    version = lambda self: self.common().version().get('server_version')

    common = lambda self: xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
  
    def is_auth(self):
        return self.uid

    def models(self, model, method, domain, options=False):
        if not self.uid:
            return False
        x = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        return x.execute_kw(self.database, self.uid, self.password, model, method, domain, options)
    
    def auth(self, **args):    
        
        up = urlparse(args.get('url',))
        url = '{}://{}'.format( up.scheme or 'https', up.netloc)

        self.username = args.get('username')
        self.password = args.get('password')
        self.database = args.get('database')
        self.url = url
        self.uid = self.common().authenticate(self.database, self.username, self.password, {})
        return self.uid
    
    def projects(self):
        projects = self.models('project.project', 'search_read',[[['active','=',True]]],{'fields': ['id', 'name']})
        return projects

    def tasks(self, project_id=None):
        if project_id:
            domain = [[['active','=', True], ['project_id','=',int(project_id)]]]
        else: 
            domain = [[['active','=', True]]]
        tasks = self.models('project.task', 'search_read',domain,{'fields': ['id', 'name', 'project_id' ]})
        return tasks

    def add_time_entry(self, **kwargs):
        # Overwrite
        description = kwargs.get('description')
        dt_start = kwargs.get('start')
        dt_end = kwargs.get('end')
        minutes = float(kwargs.get('minutes', 0))
        name = "%s - DTS:%s DTE:%s" % (description, dt_start, dt_end)
        try:
            project_id = int(self.gptracking.gptconfig_get(self.GTP_CONFIG, "project_id"))
            if project_id > 0 :
                task_id = int(self.gptracking.gptconfig_get(self.GTP_CONFIG, "project_id")) or False

                id = self.models('account.analytic.line','create', [{
                    'date':datetime.now().strftime("%Y-%m-%d"), # Required
                    'name': name, # Required
                    'project_id': project_id, # Required 
                    'task_id': task_id, 
                    'unit_amount': minutes/60,
                }])    
                return id 
            else:
                raise Exception ("First select the project  --odoo-projects --set ID")
        except Exception as e:
            logger.error(str(e))
        return False
        
    # Check setup config & params 
    def setup_config(self):
        try:
            self.auth(
                username = self.gptracking.gptconfig_get(self.GTP_CONFIG, "username"),
                password = self.gptracking.gptconfig_get(self.GTP_CONFIG, "password"),
                url = self.gptracking.gptconfig_get(self.GTP_CONFIG, "url"),
                database = self.gptracking.gptconfig_get(self.GTP_CONFIG, "database"),
            )
            if not self.is_auth():
                raise Exception("Fail auth check credentials")
        except configparser.NoSectionError as e:
            #logger.error(e)
            self.gptracking.gptconfig_set_section(self.GTP_CONFIG)
            self.setup_params()
        except configparser.NoOptionError as e:            
            #logger.error(e)
            self.setup_params()
            params = self.gptracking.gptparse_params()
            try:
                self.auth(
                    username = params.odoo_username,
                    password = params.odoo_password,
                    url =  params.odoo_url,
                    database = params.odoo_database
                )
                if self.is_auth():
                    for p in ['username', 'password', 'url', 'database']:
                        self.gptracking.gptconfig_set(
                            self.GTP_CONFIG, p,
                            getattr(params, 'odoo_'+p)
                        )
            except Exception as e:
                logger.error(str(e))
                exit(0)
        except Exception as e :
            logger.error(str(e))
        #    self.setup_params()

    def setup_params(self):
    
        self.gptracking.parse.add_argument('--odoo-username',
            action='store', 
            dest='odoo_username',
            required=True
        )
        self.gptracking.parse.add_argument('--odoo-password',
            action='store', 
            dest='odoo_password',
            required=True
        )
        self.gptracking.parse.add_argument('--odoo-url',
            action='store', 
            dest='odoo_url',
            required=True
        )        
        self.gptracking.parse.add_argument('--odoo-database',
            action='store', 
            dest='odoo_database',
            required=True
        )

    ## Optional params
    def gptparse_args(self, **kwargs):
        # Overwrite
        self.gptracking.parse.add_argument('--odoo-projects',
            action='store_const', 
            dest='odoo_projects', 
            help='Odoo projects',     
            const=True,                
        )
        self.gptracking.parse.add_argument('--odoo-tasks',
            action='store_const', 
            dest='odoo_tasks', 
            help='Odoo projects/tasks',     
            const=True,
        )

    def cli(self, **kwargs):
        # Overwrite
        params = self.gptracking.gptparse_params()
        
        def findbyid(rows, id):
            for row in rows:
                for k in row.keys():
                    if k == 'id' and row.get(k) == id:
                        return row
            return None

        if params.odoo_projects:
            title="Odoo Projects"
            try:
                rows = self.projects()
                if params.set:
                    row = findbyid(rows, int(params.set))
                    if row: 
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "project_id",row.get('id'))
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "project_name",row.get('name'))
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "task_id","")
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "task_name","")
                        self.gptracking.print_cli([], title= 'the project was added successfully')
                    else:
                        self.gptracking.print_cli([], title= 'the project id was not found')
                else:
                    self.gptracking.print_cli(rows, title=title)
            except Exception as e:
                logger.error(e)
        elif params.odoo_tasks:
            title="Odoo Tasks"
            try:
                rows = self.tasks()
                if params.set:
                    row = findbyid(rows, int(params.set))
                    if row: 
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "task_id",row.get('id'))
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "task_name",row.get('name'))
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "project_id",row.get('project_id')[0])
                        self.gptracking.gptconfig_set(self.GTP_CONFIG, "project_name",row.get('project_id')[1])
                        self.gptracking.print_cli([], title= 'the task was added successfully')
                    else:
                        self.gptracking.print_cli([], title= 'the task id was not found')
                else:
                    self.gptracking.print_cli(rows, title=title)
            except Exception as e:
                logger.error(e)

    ## Optional params
    def state(self, **kwargs):
        # Overwrite
        items = []
        def getstate(param):
            try:
                id = self.gptracking.gptconfig_get(self.GTP_CONFIG, param+"_id")
                name =self.gptracking.gptconfig_get(self.GTP_CONFIG, param+"_name")
                if len(id) and len(name):
                    items.append({'name': "%s: %s - %s " % (str(param).title(), id, name)})
            except:
                pass
        getstate('task')
        getstate('project')
        self.gptracking.print_cli(items)
