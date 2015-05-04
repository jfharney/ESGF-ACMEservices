source /etc/esg.env
export ESGINI=/esg/config/esgcet/esg.ini
#export ESGINI=/usr/local/esgf-services/ESGF-ACMEservices/django/acme_services/esg.ini 
esgscan_directory --project ACME -o ACME.txt /data/acme/projects/ACME
