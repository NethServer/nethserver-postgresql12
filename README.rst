=======================
nethserver-postgresql12
=======================

PostgreSQL 12.0 comes from SCL: https://www.softwarecollections.org/en/scls/rhscl/rh-postgresql12/

To avoid conflicts with nethserver-postgresql,
the default instance of PostgreSQL 12.0 uses port **55434**.

Access policy
=============

From localhost:

* the *postgres* user can access without password
* all other users must use password authentication

Form any other network:

* all users must use password authentication

Example for accessing with postgres user: ::

   su - postgres
   psql --port=55434


Access PostgreSQL 12.0: ::

  su - postgres -c "scl enable rh-postgresql12 -- psql --port=55434"

Backup
======

Backup and restore is not implemented system-wide: every application
should provide its own scripts.

Backup actions must be linked inside the ``pre-backup-data`` event.
Example of backup action: ::

  #!/bin/bash

  su - postgres -c "scl enable rh-postgresql12 -- pg_dump --port=55434 myapp > /var/lib/nethserver/myapp/myapp.sql"


Restore actions must be linked inside the ``post-restore-data`` event.
Example of restore action: ::

  #!/bin/bash

  if [ -f /var/lib/nethserver/myapp/myapp.sql ]; then
    drop_sql=`mktemp`
    chown postgres:postgres $drop_sql
    # drop all existing connections to the db and block new ones
    echo "UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'myapp';" >> $drop_sql
    echo "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'myapp';" >> $drop_sql
    # drop the db, then recreate it
    echo "DROP DATABASE myapp;" >> $drop_sql
    password=`perl -e "use NethServer::Password; print NethServer::Password::store('myapp');"`
    echo "CREATE database myapp; CREATE USER sonicle WITH PASSWORD '$password'; GRANT ALL PRIVILEGES ON DATABASE myapp to myuser;" >> $drop_sql 
    # allow new connections to db
    echo "UPDATE pg_database SET datallowconn = 'true' WHERE datname = 'myapp';" >> $drop_sql
    su - postgres -c "scl enable rh-postgresql12 -- psql --port=55434 < $drop_sql"
    su - postgres -c "scl enable rh-postgresql12 -- psql --port=55434 myapp < /var/lib/nethserver/myapp/myapp.sql"
    rm -f $drop_sql
  fi


