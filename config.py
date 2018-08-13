# ===== Your specific configuration goes below / please adapt ========

# the HCP account id - trial accounts typically look like p[0-9]*trial
hcp_account_id='s0019626682trial'

# you only need to adapt this part of the URL if you are NOT ON TRIAL but e.g. on PROD
hcp_landscape_host='.hanatrial.ondemand.com'
# hcp_landscape_host='.hana.ondemand.com' # this is used on PROD

# these credentials are used from applications with the "push messages to devices" API
hcp_user_credentials='User:Password'

# the following values need to be taken from the IoT Cockpit
device_id='80083c30-72cb-4c64-9df9-49f8ab2c9a81'
oauth_credentials_for_device='126bc0c1a8b049c0ff4c1cf1fc76dbb'

message_type_id_isOpen='ad4e7827b9eff4f900b7'
message_type_id_Distance='6b931fd09254b5dd3c49'

# ===== nothing to be changed / configured below this line ===========
