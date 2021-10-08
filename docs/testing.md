

# Develop



## Tests

```bash

# 1.- Run with mock values
python -m unittest

# 2.- Run with Third-party response
# Clockify
export GP_TRACKING_CLOCKIFY_TOKEN=Token
# Toggl
export GP_TRACKING_TOGGL_TOKEN=Token
# Odoo
export GP_TRACKING_ODOO_URL=Url
export GP_TRACKING_ODOO_PASSWORD=Password
export GP_TRACKING_ODOO_USERNAME=User
export GP_TRACKING_ODOO_DATABASE=Db

python -m unittest

```