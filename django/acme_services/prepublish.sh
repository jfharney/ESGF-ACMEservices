source /etc/esg.env
export ESGINI=/esg/config/esgcet/esg.ini
#export ESGINI=/usr/local/esgf-services/ESGF-ACMEservices/django/acme_services/esg.ini 
esgpublish --map ./ACME.txt --project ACME --service fileservice
