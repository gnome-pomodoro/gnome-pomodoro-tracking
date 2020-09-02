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

*  Credentials
  ```bash
  gp-tracking --odoo-database DB --odoo-url URL  --odoo-username USER --odoo-password PASS
  ```

* Projects
  * List
    ```bash
    gp-tracking --odoo-projects
    ```

  * Set
    ```bash
    gp-tracking --odoo-projects --set ID
    ```

* Tasks
  * List
    ```bash
    gp-tracking --odoo-tasks
    ```

  * Set
    ```bash
    gp-tracking --odoo-tasks --set ID
    ```