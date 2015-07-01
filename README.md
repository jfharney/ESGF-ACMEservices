ESGF-ACMEservices
=================

The ESGF-ACMEservices project implements miscellaneous services that allows access (read and write) to specific 
components of the ESGF node that are not accessible through other projects (web-fe, cog,search, node-manager, etc)

# Installation

## Prerequisites

This document assumes that python 2.7 and django 1.8 are installed.  It is also recommended that the apache server be used to 
deploy the django application. 

# Configuration

There is a configuration file that must be created called "ACMEservices.cfg" that contains configuration information.  Each service category
contains their own separate parameters, but the LOGGING parameters global to all services, contained in the LOGGERS section.
The repo has an "ACMEservices-sample.cfg" file that has all of the keys needed (just need to substitute values).

## general service parameters

- publication_log_file - the name of the log file that outputs debugging messages
- publication_logger_level - the log level of the debug statements (defunct right now, but may be added later)
- db_log_file
- db_logger_level

## esg ini service parameters

## db service parameters

- populate_groups
- isConnectedToDB
- dbname - name of the db housing the ESGF user info (default is esgcet)
- dbuser - 
- dbpassword
- esgini_location

# Services offered

## ESG_INI CRUD operations

The esg ini crud (create, read, update, delete) operations services provide clients an API for 
remotely changing and accessing configuration information in the esg.ini.  In the alpha version,
the information is facets and their values.

### Configuration options

### GET

The "GET" operation retrieves the facet values given a project name. NOTE: This will only give 
values of ALL the facets.

#### API

http://<hostname>:<port>/acme_services/publishing/facets/<username>?project=<project_name>

<hostname> - The host or ip address of the system running the application
<port> - The port on which the system is running
<username> - Username of the requestor.  NOTE: This must be a user with read access to a specific project
<project_name> - The project name 

#### Example

curl -X GET http://localhost:8081/acme_services/publishing/facets/jfharney 

{
  "realm": [
    "lndice", 
    "all", 
    "atm", 
    "ocn", 
    "ATM", 
    "None", 
    "ice", 
    "lnd"
  ], 
  "data_type": [
    "a", 
    "h", 
    "dd", 
    "h1", 
    "climo", 
    "h0"
  ], 
  "versionnum": [
    "v0_1", 
    "v01", 
    "HIGHRES", 
    "pre-v0"
  ], 
  "project": [
    "ACME"
  ], 
  "range": [
    "all", 
    "10-19"
  ], 
  "experiment": [
    "B1850C5_ne30gx1_tuning", 
    "B1851C5e1_ne30", 
    "B1850C5e1_ne30"
  ], 
  "regridding": [
    "bilinear", 
    "downscaled", 
    "native", 
    "fv257x512"
  ]
}

### POST

#### API

#### Example

### PUT

#### API

#### Example

### DELETE

#### API

#### Example

## ESG_INI CRUD operations

### Configuration options


*This text will be italic*
**This text will be bold**

**Everyone _must_ attend the meeting at 5 o'clock today.**



- Item
- Item
- Item

1. Item 1
  1. A corollary to the above item.
  2. Yet another point to consider.
2. Item 2
  * A corollary that does not need to be ordered.
    * This is indented four spaces, because it's two spaces further than the item above.
    * You might want to consider making a new list.
3. Item 3