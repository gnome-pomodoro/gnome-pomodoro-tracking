# Odoo 

## Modules requied 
* project
* sale_timesheet

## Test 
* ✅ Odoo 13.0 - Community
* ✅ Odoo 13.0 - Enterprise
* ❌ Odoo 12.0 - Community
* ❌ Odoo 12.0 - Enterprise
* ❌ Odoo 11.0 - Community
* ❌ Odoo 11.0 - Enterprise

## CLI

* Credentials

  ```bash
  gnome-pomodoro-tracking --odoo-database DB --odoo-url URL  --odoo-username USER --odoo-password PASS
  ```

* Projects
  
  ```bash
  # List
  gnome-pomodoro-tracking --odoo-projects
  # Set
  gnome-pomodoro-tracking --odoo-projects --set ID
  ```

* Tasks

  ```bash
  # List
  gnome-pomodoro-tracking --odoo-tasks
  # Set
  gnome-pomodoro-tracking --odoo-tasks --set ID
  ```
